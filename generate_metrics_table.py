import sqlite3
import json
import statistics

# Conectar ao banco de dados
DB_PATH = "cvrp_analysis.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Carregar dados de tempo reais
with open('times_data.json', 'r') as f:
    TIMES_DATA = json.load(f)

# Melhores soluções conhecidas
BEST_KNOWN = {
    'X-n101-k25': 27591, 'X-n106-k14': 26362, 'X-n110-k13': 14971, 'X-n115-k10': 12747,
    'X-n120-k6': 13332, 'X-n125-k30': 55539, 'X-n129-k18': 28940, 'X-n134-k13': 10916,
    'X-n139-k10': 13590, 'X-n143-k7': 15700, 'X-n148-k46': 43448, 'X-n153-k22': 21220,
    'X-n157-k13': 16876, 'X-n162-k11': 14138, 'X-n167-k10': 20557, 'X-n172-k51': 45607,
    'X-n176-k26': 47812, 'X-n181-k23': 25569, 'X-n186-k15': 24145, 'X-n190-k8': 16980,
    'X-n195-k51': 44225, 'X-n200-k36': 58578, 'X-n204-k19': 19565, 'X-n209-k16': 30656,
    'X-n214-k11': 10856, 'X-n219-k73': 117595, 'X-n223-k34': 40437, 'X-n228-k23': 25742,
    'X-n233-k16': 19230, 'X-n237-k14': 27042, 'X-n242-k48': 82751, 'X-n247-k50': 37274,
    'X-n251-k28': 38684, 'X-n256-k16': 18839, 'X-n261-k13': 26558, 'X-n266-k58': 75478,
    'X-n270-k35': 35291, 'X-n275-k28': 21245, 'X-n280-k17': 33503, 'X-n284-k15': 20215,
    'X-n289-k60': 95151, 'X-n294-k50': 47161, 'X-n298-k31': 34231, 'X-n303-k21': 21736,
    'X-n308-k13': 25859, 'X-n313-k71': 94043, 'X-n317-k53': 78355, 'X-n322-k28': 29834,
    'X-n327-k20': 27532, 'X-n331-k15': 31102, 'X-n336-k84': 139111, 'X-n344-k43': 42050,
    'X-n351-k40': 25896, 'X-n359-k29': 51505, 'X-n367-k17': 22814, 'X-n376-k94': 147713,
    'X-n384-k52': 65928, 'X-n393-k38': 38260, 'X-n401-k29': 66154, 'X-n411-k19': 19712,
    'X-n420-k130': 107798, 'X-n429-k61': 65449, 'X-n439-k37': 36391, 'X-n449-k29': 55233,
    'X-n459-k26': 24139, 'X-n469-k138': 221824, 'X-n480-k70': 89449, 'X-n491-k59': 66483,
    'X-n502-k39': 69226, 'X-n513-k21': 24201, 'X-n524-k153': 154593, 'X-n536-k96': 94846,
    'X-n548-k50': 86700, 'X-n561-k42': 42717, 'X-n573-k30': 50673, 'X-n586-k159': 190316,
    'X-n599-k92': 108451, 'X-n613-k62': 59535, 'X-n627-k43': 62164, 'X-n641-k35': 63682,
    'X-n655-k131': 106780, 'X-n670-k130': 146332, 'X-n685-k75': 68205, 'X-n701-k44': 81923,
    'X-n716-k35': 43373, 'X-n733-k159': 136187, 'X-n749-k98': 77269, 'X-n766-k71': 114417,
    'X-n783-k48': 72386, 'X-n801-k40': 73305, 'X-n819-k171': 158121, 'X-n837-k142': 193737,
    'X-n856-k95': 88965, 'X-n876-k59': 99299, 'X-n895-k37': 53860, 'X-n916-k207': 329179,
    'X-n936-k151': 132715, 'X-n957-k87': 85465, 'X-n979-k58': 118976, 'X-n1001-k43': 72355,
}

def get_best_result(instance_name, method):
    """Obtém o melhor resultado encontrado"""
    cursor.execute("""
        SELECT MIN(cost) as best_cost
        FROM solutions
        WHERE instance_name = ? AND method = ?
    """, (instance_name, method))

    result = cursor.fetchone()
    if result and result[0] is not None:
        return result[0]
    return None

def calculate_gap(best_known, found_value):
    """Calcula o GAP percentual"""
    if best_known == 0:
        return 0
    return ((found_value - best_known) / best_known) * 100

# Calcular GAPs e tempos para cada método
def calculate_metrics(method):
    """Calcula métricas para um método"""
    gaps = []
    times = []

    for instance, best_known in BEST_KNOWN.items():
        # GAP
        best_result = get_best_result(instance, method)
        if best_result:
            gap = calculate_gap(best_known, best_result)
            gaps.append(gap)

        # Tempo
        if instance in TIMES_DATA and method in TIMES_DATA[instance]:
            times.append(TIMES_DATA[instance][method])

    return gaps, times

# Calcular para ILS com 2-Opt e Swap*
print("=" * 70)
print("CALCULANDO MÉTRICAS PARA ILS")
print("=" * 70)

ils_gaps, ils_times = calculate_metrics('ILS')
ils_swap_gaps, ils_swap_times = calculate_metrics('ILS-Swap')

print(f"\nILS (2-Opt):")
print(f"  GAPs calculados: {len(ils_gaps)} instâncias")
print(f"  Melhor GAP: {min(ils_gaps):.2f}%")
print(f"  GAP médio: {statistics.mean(ils_gaps):.2f}%")
print(f"  Pior GAP: {max(ils_gaps):.2f}%")
print(f"  Tempos: {len(ils_times)} instâncias")
print(f"  Melhor tempo: {min(ils_times):.2f}s")
print(f"  Tempo médio: {statistics.mean(ils_times):.2f}s")
print(f"  Pior tempo: {max(ils_times):.2f}s")

print(f"\nILS (Swap*):")
print(f"  GAPs calculados: {len(ils_swap_gaps)} instâncias")
print(f"  Melhor GAP: {min(ils_swap_gaps):.2f}%")
print(f"  GAP médio: {statistics.mean(ils_swap_gaps):.2f}%")
print(f"  Pior GAP: {max(ils_swap_gaps):.2f}%")
print(f"  Tempos: {len(ils_swap_times)} instâncias")
print(f"  Melhor tempo: {min(ils_swap_times):.2f}s")
print(f"  Tempo médio: {statistics.mean(ils_swap_times):.2f}s")
print(f"  Pior tempo: {max(ils_swap_times):.2f}s")

# Calcular para GRASP
print("\n" + "=" * 70)
print("CALCULANDO MÉTRICAS PARA GRASP")
print("=" * 70)

grasp_gaps, grasp_times = calculate_metrics('GRASP')
grasp_swap_gaps, grasp_swap_times = calculate_metrics('GRASP-Swap')

print(f"\nGRASP (2-Opt):")
print(f"  GAPs calculados: {len(grasp_gaps)} instâncias")
print(f"  Melhor GAP: {min(grasp_gaps):.2f}%")
print(f"  GAP médio: {statistics.mean(grasp_gaps):.2f}%")
print(f"  Pior GAP: {max(grasp_gaps):.2f}%")
print(f"  Tempos: {len(grasp_times)} instâncias")
print(f"  Melhor tempo: {min(grasp_times):.2f}s")
print(f"  Tempo médio: {statistics.mean(grasp_times):.2f}s")
print(f"  Pior tempo: {max(grasp_times):.2f}s")

print(f"\nGRASP (Swap*):")
print(f"  GAPs calculados: {len(grasp_swap_gaps)} instâncias")
print(f"  Melhor GAP: {min(grasp_swap_gaps):.2f}%")
print(f"  GAP médio: {statistics.mean(grasp_swap_gaps):.2f}%")
print(f"  Pior GAP: {max(grasp_swap_gaps):.2f}%")
print(f"  Tempos: {len(grasp_swap_times)} instâncias")
print(f"  Melhor tempo: {min(grasp_swap_times):.2f}s")
print(f"  Tempo médio: {statistics.mean(grasp_swap_times):.2f}s")
print(f"  Pior tempo: {max(grasp_swap_times):.2f}s")

# Calcular tempos em percentual relativo ao ILS (ILS = 100%, GRASP = quanto % mais lento)
# Para 2-Opt
ils_time_pct = {
    'min': 100.00,  # ILS é a baseline
    'avg': 100.00,
    'max': 100.00
}
grasp_time_pct = {
    'min': (min(grasp_times) / min(ils_times)) * 100,
    'avg': (statistics.mean(grasp_times) / statistics.mean(ils_times)) * 100,
    'max': (max(grasp_times) / max(ils_times)) * 100
}

# Para Swap*
ils_swap_time_pct = {
    'min': 100.00,  # ILS é a baseline
    'avg': 100.00,
    'max': 100.00
}
grasp_swap_time_pct = {
    'min': (min(grasp_swap_times) / min(ils_swap_times)) * 100,
    'avg': (statistics.mean(grasp_swap_times) / statistics.mean(ils_swap_times)) * 100,
    'max': (max(grasp_swap_times) / max(ils_swap_times)) * 100
}

# Gerar tabela LaTeX
print("\n" + "=" * 70)
print("TABELA LATEX - ILS (2-Opt) vs GRASP (2-Opt)")
print("=" * 70)

latex_2opt = f"""
\\begin{{tabular}}{{lcccccc}}
    \\toprule
    & \\multicolumn{{3}}{{c}}{{ILS}} & \\multicolumn{{3}}{{c}}{{GRASP}} \\\\
    \\cmidrule(lr){{2-4}} \\cmidrule(lr){{5-7}}
    Métrica & Melhor & Média & Pior & Melhor & Média & Pior \\\\
    \\midrule
    GAP médio (\\%) & {min(ils_gaps):.2f} & {statistics.mean(ils_gaps):.2f} & {max(ils_gaps):.2f} & {min(grasp_gaps):.2f} & {statistics.mean(grasp_gaps):.2f} & {max(grasp_gaps):.2f} \\\\
    Tempo médio (s) & {min(ils_times):.2f} & {statistics.mean(ils_times):.2f} & {max(ils_times):.2f} & {min(grasp_times):.2f} & {statistics.mean(grasp_times):.2f} & {max(grasp_times):.2f} \\\\
    Tempo (\\%) & {ils_time_pct['min']:.2f} & {ils_time_pct['avg']:.2f} & {ils_time_pct['max']:.2f} & {grasp_time_pct['min']:.2f} & {grasp_time_pct['avg']:.2f} & {grasp_time_pct['max']:.2f} \\\\
    \\bottomrule
\\end{{tabular}}
"""

print(latex_2opt)

print("\n" + "=" * 70)
print("TABELA LATEX - ILS (Swap*) vs GRASP (Swap*)")
print("=" * 70)

latex_swap = f"""
\\begin{{tabular}}{{lcccccc}}
    \\toprule
    & \\multicolumn{{3}}{{c}}{{ILS}} & \\multicolumn{{3}}{{c}}{{GRASP}} \\\\
    \\cmidrule(lr){{2-4}} \\cmidrule(lr){{5-7}}
    Métrica & Melhor & Média & Pior & Melhor & Média & Pior \\\\
    \\midrule
    GAP médio (\\%) & {min(ils_swap_gaps):.2f} & {statistics.mean(ils_swap_gaps):.2f} & {max(ils_swap_gaps):.2f} & {min(grasp_swap_gaps):.2f} & {statistics.mean(grasp_swap_gaps):.2f} & {max(grasp_swap_gaps):.2f} \\\\
    Tempo médio (s) & {min(ils_swap_times):.2f} & {statistics.mean(ils_swap_times):.2f} & {max(ils_swap_times):.2f} & {min(grasp_swap_times):.2f} & {statistics.mean(grasp_swap_times):.2f} & {max(grasp_swap_times):.2f} \\\\
    Tempo (\\%) & {ils_swap_time_pct['min']:.2f} & {ils_swap_time_pct['avg']:.2f} & {ils_swap_time_pct['max']:.2f} & {grasp_swap_time_pct['min']:.2f} & {grasp_swap_time_pct['avg']:.2f} & {grasp_swap_time_pct['max']:.2f} \\\\
    \\bottomrule
\\end{{tabular}}
"""

print(latex_swap)

# Salvar em arquivo
with open('tabela_metricas_comparativas.tex', 'w') as f:
    f.write("% Tabela Comparativa - ILS (2-Opt) vs GRASP (2-Opt)\n")
    f.write(latex_2opt)
    f.write("\n\n% Tabela Comparativa - ILS (Swap*) vs GRASP (Swap*)\n")
    f.write(latex_swap)

print(f"\n✅ Tabelas salvas em: tabela_metricas_comparativas.tex")

conn.close()
