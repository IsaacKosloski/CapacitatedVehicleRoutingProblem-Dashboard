import os
import matplotlib.pyplot as plt

def save_route_images(routes, coords, solution_name, output_folder):
    """
    Gera e salva um gráfico das rotas com coordenadas, destacando o depósito.

    :param routes: lista de rotas, ex: [[1, 2, 3], [1, 4, 5]]
    :param coords: dicionário {id: (x, y)}
    :param solution_name: nome base do arquivo de imagem
    :param output_folder: caminho da pasta onde salvar o PNG
    """

    # Cria a pasta de destino, se necessário
    os.makedirs(output_folder, exist_ok=True)

    # Identifica o depósito (assumido como o primeiro nó da primeira rota)
    depot = routes[0][0]
    depot_coords = coords[depot]

    # Cria a figura
    plt.figure(figsize=(8, 6))

    for i, route in enumerate(routes):
        x = [coords[node][0] for node in route]
        y = [coords[node][1] for node in route]
        x.append(x[0])  # Volta ao depósito
        y.append(y[0])
        plt.plot(x, y, marker='o', label=f'Rota {i+1}')

    # Destaca o depósito
    plt.scatter(
        [depot_coords[0]], [depot_coords[1]],
        c='red', s=100, edgecolors='black', label='Depósito', zorder=5
    )

    plt.title(f"Rotas - {solution_name}")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    plt.legend()

    # Salva a imagem
    save_path = os.path.join(output_folder, f"{solution_name}.png")
    plt.savefig(save_path)
    plt.close()

    print(f"✅ Imagem salva: {save_path}")
