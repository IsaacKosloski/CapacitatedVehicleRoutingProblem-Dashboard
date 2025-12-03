import os
import re
import sqlite3
from collections import defaultdict

def extract_time_from_sol(file_path):
    """Extrai o tempo de execução de um arquivo .sol"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Procura por "Time X.XXXX"
            match = re.search(r'Time\s+([\d.]+)', content)
            if match:
                return float(match.group(1))
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
    return None

def extract_all_times():
    """Extrai tempos de todos os métodos e instâncias X"""
    times_data = defaultdict(lambda: defaultdict(list))

    methods = ['ILS', 'ILS-Swap', 'GRASP', 'GRASP-Swap']
    base_path = 'data/solutions'

    for method in methods:
        method_path = os.path.join(base_path, method, 'X')
        if not os.path.exists(method_path):
            print(f"Caminho não encontrado: {method_path}")
            continue

        # Lista todas as instâncias X
        instances = [d for d in os.listdir(method_path) if d.startswith('X-n')]

        for instance in instances:
            instance_path = os.path.join(method_path, instance)
            if not os.path.isdir(instance_path):
                continue

            # Lista todos os arquivos .sol
            sol_files = [f for f in os.listdir(instance_path) if f.endswith('.sol')]

            for sol_file in sol_files:
                sol_path = os.path.join(instance_path, sol_file)
                time = extract_time_from_sol(sol_path)
                if time is not None:
                    times_data[instance][method].append(time)

    return times_data

def calculate_average_times(times_data):
    """Calcula a média de tempo por instância e método"""
    avg_times = {}

    for instance, methods in sorted(times_data.items()):
        avg_times[instance] = {}
        for method, times in methods.items():
            if times:
                avg_times[instance][method] = sum(times) / len(times)

    return avg_times

def main():
    print("Extraindo tempos dos arquivos .sol...")
    times_data = extract_all_times()

    print(f"\nInstâncias processadas: {len(times_data)}")

    print("\nCalculando médias...")
    avg_times = calculate_average_times(times_data)

    # Salvar em arquivo para uso posterior
    import json
    with open('times_data.json', 'w') as f:
        json.dump(avg_times, f, indent=2)

    print(f"✅ Dados salvos em times_data.json")

    # Mostrar amostra
    print("\n=== AMOSTRA DE TEMPOS MÉDIOS ===")
    sample_instances = ['X-n101-k25', 'X-n200-k36', 'X-n500-k39', 'X-n1001-k43']

    for instance in sample_instances:
        if instance in avg_times:
            print(f"\n{instance}:")
            for method in ['ILS', 'ILS-Swap', 'GRASP', 'GRASP-Swap']:
                if method in avg_times[instance]:
                    time = avg_times[instance][method]
                    count = len(times_data[instance][method])
                    print(f"  {method:12} -> {time:8.4f}s (n={count})")

    return avg_times

if __name__ == "__main__":
    avg_times = main()
