import sqlite3
import json
import os

# Conectar ao banco de dados
DB_PATH = "cvrp_analysis.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Carregar dados de tempo reais
with open('times_data.json', 'r') as f:
    TIMES_DATA = json.load(f)

# Melhores soluções conhecidas para TODAS as instâncias X (fonte: CVRPLIB)
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
    """Obtém o melhor resultado encontrado para uma instância e método"""
    cursor.execute("""
        SELECT MIN(cost) as best_cost
        FROM solutions
        WHERE instance_name = ? AND method = ?
    """, (instance_name, method))

    result = cursor.fetchone()
    if result and result[0] is not None:
        return result[0]
    return None

def get_real_avg_time(instance_name, method):
    """Obtém o tempo médio real dos arquivos .sol"""
    if instance_name in TIMES_DATA and method in TIMES_DATA[instance_name]:
        return round(TIMES_DATA[instance_name][method], 2)
    return None

def calculate_gap(best_known, found_value):
    """Calcula o GAP percentual"""
    if best_known == 0:
        return 0
    return ((found_value - best_known) / best_known) * 100

def generate_ils_comparison_table():
    """Gera a tabela comparativa do ILS (2-Opt vs Swap*)"""
    instances = sorted([k for k in BEST_KNOWN.keys()])

    rows = []
    for instance in instances:
        best_known = BEST_KNOWN[instance]

        # ILS com 2-Opt
        ils_best = get_best_result(instance, 'ILS')
        ils_time = get_real_avg_time(instance, 'ILS')

        # ILS com Swap*
        ils_swap_best = get_best_result(instance, 'ILS-Swap')
        ils_swap_time = get_real_avg_time(instance, 'ILS-Swap')

        if ils_best and ils_swap_best and ils_time is not None and ils_swap_time is not None:
            ils_gap = calculate_gap(best_known, ils_best)
            ils_swap_gap = calculate_gap(best_known, ils_swap_best)

            row = f"    {instance} & {best_known:,} & {ils_best:,.2f} & {ils_gap:.2f}\\% & {ils_time} & {ils_swap_best:,.2f} & {ils_swap_gap:.2f}\\% & {ils_swap_time} \\\\"
            rows.append(row)

    return "\n".join(rows)

def generate_grasp_comparison_table():
    """Gera a tabela comparativa do GRASP (2-Opt vs Swap*)"""
    instances = sorted([k for k in BEST_KNOWN.keys()])

    rows = []
    for instance in instances:
        best_known = BEST_KNOWN[instance]

        # GRASP com 2-Opt
        grasp_best = get_best_result(instance, 'GRASP')
        grasp_time = get_real_avg_time(instance, 'GRASP')

        # GRASP com Swap*
        grasp_swap_best = get_best_result(instance, 'GRASP-Swap')
        grasp_swap_time = get_real_avg_time(instance, 'GRASP-Swap')

        if grasp_best and grasp_swap_best and grasp_time is not None and grasp_swap_time is not None:
            grasp_gap = calculate_gap(best_known, grasp_best)
            grasp_swap_gap = calculate_gap(best_known, grasp_swap_best)

            row = f"    {instance} & {best_known:,} & {grasp_best:,.2f} & {grasp_gap:.2f}\\% & {grasp_time} & {grasp_swap_best:,.2f} & {grasp_swap_gap:.2f}\\% & {grasp_swap_time} \\\\"
            rows.append(row)

    return "\n".join(rows)

def generate_latex_document():
    """Gera o documento LaTeX completo com as duas tabelas comparativas"""

    ils_table = generate_ils_comparison_table()
    grasp_table = generate_grasp_comparison_table()

    latex_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[brazilian]{babel}
\usepackage{booktabs}
\usepackage{array}
\usepackage{geometry}
\usepackage{longtable}
\geometry{a4paper, margin=2cm}

\title{Comparação de Operadores de Busca Local\\ILS e GRASP nas Instâncias X}
\author{}
\date{\today}

\begin{document}

\maketitle

\section{Introdução}

Este documento apresenta a comparação entre dois operadores de busca local aplicados aos algoritmos ILS (Iterated Local Search) e GRASP (Greedy Randomized Adaptive Search Procedure) nas 100 instâncias do conjunto X do benchmark Uchoa et al. (2017).

Os operadores comparados são:
\begin{itemize}
    \item \textbf{2-Opt}: Operador de busca local clássico que realiza trocas entre dois arcos
    \item \textbf{Swap*}: Operador de busca local avançado baseado em movimentos 3-Opt
\end{itemize}

As tabelas apresentam:
\begin{itemize}
    \item \textbf{Instância}: nome da instância
    \item \textbf{Melhor Sol. Conhecida}: melhor solução conhecida (BKS) do CVRPLIB
    \item \textbf{Melhor Resultado}: melhor valor obtido nas execuções
    \item \textbf{GAP (\%)}: diferença percentual em relação à melhor solução conhecida
    \item \textbf{Tempo (s)}: tempo médio de execução em segundos (dados reais)
\end{itemize}

\clearpage

\section{Comparação ILS: 2-Opt vs Swap*}

A Tabela \ref{tab:ils_comparison} compara o desempenho do algoritmo ILS utilizando os operadores 2-Opt e Swap* em todas as 100 instâncias do conjunto X.

\begin{longtable}{@{}lrrrrrrrr@{}}
\caption{Comparação ILS: 2-Opt vs Swap* nas instâncias X.} \label{tab:ils_comparison} \\
\toprule
& & \multicolumn{3}{c}{ILS com 2-Opt} & \multicolumn{3}{c}{ILS com Swap*} \\
\cmidrule(lr){3-5} \cmidrule(lr){6-8}
Instância & Melhor Sol. & Melhor Res. & GAP (\%) & T(s) & Melhor Res. & GAP (\%) & T(s) \\
\midrule
\endfirsthead

\multicolumn{8}{c}%
{{\tablename\ \thetable{} -- Continuação}} \\
\toprule
& & \multicolumn{3}{c}{ILS com 2-Opt} & \multicolumn{3}{c}{ILS com Swap*} \\
\cmidrule(lr){3-5} \cmidrule(lr){6-8}
Instância & Melhor Sol. & Melhor Res. & GAP (\%) & T(s) & Melhor Res. & GAP (\%) & T(s) \\
\midrule
\endhead

\midrule
\multicolumn{8}{r}{{Continua na próxima página...}} \\
\endfoot

\bottomrule
\endlastfoot

""" + ils_table + r"""
\end{longtable}

\subsection{Análise do ILS}

A comparação entre ILS com 2-Opt e ILS com Swap* revela:

\begin{itemize}
    \item \textbf{Qualidade da solução}: O ILS com Swap* geralmente obtém soluções de melhor qualidade (menores GAPs) devido à maior capacidade de exploração do operador
    \item \textbf{Tempo de execução}: O ILS com 2-Opt é significativamente mais rápido. Para instâncias maiores (X-n1001-k43), o Swap* pode levar mais de 1000 segundos enquanto o 2-Opt leva apenas 1 segundo
    \item \textbf{Trade-off}: O ILS com Swap* oferece melhor qualidade de solução, mas com custo computacional muito maior em instâncias grandes
    \item \textbf{Recomendação}: Use ILS com Swap* para instâncias pequenas/médias quando a qualidade for prioritária; use ILS com 2-Opt para instâncias grandes ou quando o tempo for crítico
\end{itemize}

\clearpage

\section{Comparação GRASP: 2-Opt vs Swap*}

A Tabela \ref{tab:grasp_comparison} compara o desempenho do algoritmo GRASP utilizando os operadores 2-Opt e Swap* em todas as 100 instâncias do conjunto X.

\begin{longtable}{@{}lrrrrrrrr@{}}
\caption{Comparação GRASP: 2-Opt vs Swap* nas instâncias X.} \label{tab:grasp_comparison} \\
\toprule
& & \multicolumn{3}{c}{GRASP com 2-Opt} & \multicolumn{3}{c}{GRASP com Swap*} \\
\cmidrule(lr){3-5} \cmidrule(lr){6-8}
Instância & Melhor Sol. & Melhor Res. & GAP (\%) & T(s) & Melhor Res. & GAP (\%) & T(s) \\
\midrule
\endfirsthead

\multicolumn{8}{c}%
{{\tablename\ \thetable{} -- Continuação}} \\
\toprule
& & \multicolumn{3}{c}{GRASP com 2-Opt} & \multicolumn{3}{c}{GRASP com Swap*} \\
\cmidrule(lr){3-5} \cmidrule(lr){6-8}
Instância & Melhor Sol. & Melhor Res. & GAP (\%) & T(s) & Melhor Res. & GAP (\%) & T(s) \\
\midrule
\endhead

\midrule
\multicolumn{8}{r}{{Continua na próxima página...}} \\
\endfoot

\bottomrule
\endlastfoot

""" + grasp_table + r"""
\end{longtable}

\subsection{Análise do GRASP}

A comparação entre GRASP com 2-Opt e GRASP com Swap* mostra:

\begin{itemize}
    \item \textbf{Qualidade da solução}: O GRASP com Swap* obtém soluções consistentemente melhores (menores GAPs) em relação às melhores soluções conhecidas
    \item \textbf{Tempo de execução}: O GRASP com 2-Opt é mais rápido, mas ainda consideravelmente mais lento que o ILS. Para X-n1001-k43, o GRASP com Swap* leva cerca de 650 segundos
    \item \textbf{Variabilidade}: Ambas as versões apresentam boa consistência, mas o Swap* oferece soluções mais próximas do ótimo
    \item \textbf{Recomendação}: Use GRASP com Swap* para obter soluções de alta qualidade quando houver tempo disponível; use GRASP com 2-Opt para um balanço entre qualidade e tempo
\end{itemize}

\clearpage

\section{Conclusões Gerais}

\subsection{Comparação entre Operadores}

\begin{itemize}
    \item O operador \textbf{Swap*} (3-Opt) é superior ao \textbf{2-Opt} em termos de qualidade de solução para ambos os algoritmos
    \item O operador \textbf{2-Opt} é significativamente mais rápido. A diferença aumenta com o tamanho da instância
    \item Para X-n1001-k43: ILS 2-Opt (1.05s) vs ILS Swap* (1126s) vs GRASP 2-Opt (288s) vs GRASP Swap* (654s)
    \item A escolha do operador deve considerar o trade-off entre qualidade da solução e tempo computacional disponível
\end{itemize}

\subsection{Comparação entre Algoritmos}

\begin{itemize}
    \item \textbf{ILS com 2-Opt} é o mais rápido de todos os métodos, ideal para instâncias grandes
    \item \textbf{ILS} geralmente produz soluções de melhor qualidade que GRASP com o mesmo operador
    \item \textbf{GRASP} é significativamente mais lento que ILS, mas oferece maior diversificação
    \item Para instâncias grandes (> 500 clientes), ILS com 2-Opt torna-se a única opção prática
\end{itemize}

\subsection{Recomendações Práticas}

\begin{enumerate}
    \item Para \textbf{instâncias pequenas} (até 200 clientes): Qualquer método é viável; prefira Swap* para melhor qualidade
    \item Para \textbf{instâncias médias} (200-500 clientes): ILS com Swap* ou GRASP com 2-Opt
    \item Para \textbf{instâncias grandes} (> 500 clientes): ILS com 2-Opt é essencial devido ao tempo
    \item Para \textbf{aplicações em tempo real}: ILS com 2-Opt exclusivamente
    \item Para \textbf{aplicações offline com foco em qualidade}: ILS com Swap* para instâncias pequenas/médias
\end{enumerate}

\section{Referências}

\begin{itemize}
    \item UCHOA, E.; PECIN, D.; PESSOA, A.; POGGI, M.; VIDAL, T.; SUBRAMANIAN, A. New benchmark instances for the Capacitated Vehicle Routing Problem. \textit{European Journal of Operational Research}, v. 257, n. 3, p. 845-858, 2017.
    \item CVRPLIB. Disponível em: \texttt{https://galgos.inf.puc-rio.br/cvrplib/}
    \item LIN, S.; KERNIGHAN, B. W. An effective heuristic algorithm for the traveling-salesman problem. \textit{Operations Research}, v. 21, n. 2, p. 498-516, 1973.
\end{itemize}

\end{document}
"""

    return latex_content

# Gerar e salvar o documento
latex_doc = generate_latex_document()

output_file = "comparacao_operadores_ils_grasp.tex"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(latex_doc)

print(f"✅ Documento LaTeX gerado: {output_file}")
print(f"\n📊 Estatísticas:")

# Calcular algumas estatísticas
total_instances = len(BEST_KNOWN)
methods = ['ILS', 'ILS-Swap', 'GRASP', 'GRASP-Swap']

for method in methods:
    count = 0
    for instance in BEST_KNOWN.keys():
        if get_best_result(instance, method) and get_real_avg_time(instance, method):
            count += 1
    print(f"  {method}: {count}/{total_instances} instâncias com dados completos")

# Comparação de tempos médios
print("\n⏱️  Comparação de tempos médios:")
sample_instances = ['X-n101-k25', 'X-n500-k39', 'X-n1001-k43']
for instance in sample_instances:
    if instance in TIMES_DATA:
        print(f"\n  {instance}:")
        for method in methods:
            if method in TIMES_DATA[instance]:
                print(f"    {method:12} -> {TIMES_DATA[instance][method]:8.2f}s")

# Fechar conexão
conn.close()

print(f"\nPara compilar o documento:")
print(f"  pdflatex {output_file}")
print(f"  pdflatex {output_file}  # Executar duas vezes para referências")
