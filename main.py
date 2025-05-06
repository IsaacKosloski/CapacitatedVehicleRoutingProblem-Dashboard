import os
from database import DatabaseManager
from models import SolutionParser
from analysis import StatisticsCalculator

def find_instance_file(instance_name):
    base_instance_dir = os.path.join("data", "instances")
    for letter_folder in os.listdir(base_instance_dir):
        instance_path = os.path.join(base_instance_dir, letter_folder, f"{instance_name}.vrp")
        if os.path.isfile(instance_path):
            return instance_path
    return None

def process_instance(instance_name, solution_path, method):
    print(f"🔍 {method} - {instance_name}")
    instance_file = find_instance_file(instance_name)
    if not instance_file:
        print(f"[ERRO] Instância .vrp '{instance_name}.vrp' não encontrada.")
        return

    db = DatabaseManager()
    parser = SolutionParser()
    stats_calc = StatisticsCalculator()

    for file in os.listdir(solution_path):
        if file.endswith(".sol"):
            if db.solution_exists(instance_name, file, method):
                print(f"[SKIP] {file} já está no banco.")
                continue

            filepath = os.path.join(solution_path, file)
            cost, routes = parser.parse_file(filepath)
            if cost is not None and routes:
                vehicles_used = len(routes)
                db.insert_solution(instance_name, file, cost, vehicles_used, method)
                print(f"[OK] {file} | Custo: {cost:.2f} | Veículos: {vehicles_used}")
            else:
                print(f"[ERRO] Falha ao extrair dados de {file}")

    costs = db.get_costs_by_instance_and_method(instance_name, method)
    stats = stats_calc.compute(costs)

    if stats:
        db.insert_analysis(instance_name, method, stats)
        print(f"[✓] Estatísticas salvas para {instance_name} ({method})")
    else:
        print(f"[!] Nenhum custo válido para {instance_name} ({method})")

def main():
    base_solution_dir = os.path.join("data", "solutions")
    db = DatabaseManager()

    db.create_tables()  # Execute uma única vez

    for method in os.listdir(base_solution_dir):
        method_path = os.path.join(base_solution_dir, method)
        if not os.path.isdir(method_path):
            continue

        for group in os.listdir(method_path):
            group_path = os.path.join(method_path, group)
            for instance in os.listdir(group_path):
                instance_path = os.path.join(group_path, instance)
                if os.path.isdir(instance_path):
                    process_instance(instance, instance_path, method)

if __name__ == "__main__":
    main()
