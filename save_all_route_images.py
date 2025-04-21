import os
from models.solution_parser import extract_routes
from models.instance_parser import get_coordinates_from_vrp
from models.route_saver import save_route_images

def save_all_images():
    data_solutions_dir = "data/solutions"
    data_instances_dir = "data/instances"
    output_root = "routes"

    for letter_dir in os.listdir(data_solutions_dir):
        letter_path = os.path.join(data_solutions_dir, letter_dir)
        if not os.path.isdir(letter_path):
            continue

        for instance in os.listdir(letter_path):
            sol_path = os.path.join(letter_path, instance)
            if not os.path.isdir(sol_path):
                continue

            vrp_file = os.path.join(data_instances_dir, letter_dir, f"{instance}.vrp")
            if not os.path.isfile(vrp_file):
                print(f"[!] VRP file not found for {instance}")
                continue

            coords = get_coordinates_from_vrp(vrp_file)
            output_folder = os.path.join(output_root, instance)
            os.makedirs(output_folder, exist_ok=True)

            for sol_file in os.listdir(sol_path):
                if sol_file.endswith(".sol"):
                    sol_file_path = os.path.join(sol_path, sol_file)
                    routes = extract_routes(sol_file_path)
                    sol_name = os.path.splitext(sol_file)[0]
                    save_route_images(routes, coords, sol_name, output_folder)

if __name__ == "__main__":
    save_all_images()
