import streamlit as st
import os
import time
from models.solution_parser import extract_routes
from models.instance_parser import get_coordinates_from_vrp
from pages.plot_routes import plot_routes_plotly, plot_routes_folium

st.set_page_config(layout="wide")
st.title("🛣️ Visualização das Rotas")

DB_SOLUTIONS = "data/solutions"
DB_INSTANCES = "data/instances"

# Seleção de método (BruteForce, ILS, GRASP...)
methods = sorted([m for m in os.listdir(DB_SOLUTIONS) if os.path.isdir(os.path.join(DB_SOLUTIONS, m))])
selected_method = st.selectbox("Método de Solução:", methods)

# Grupo e instância
grupo_options = sorted([d for d in os.listdir(os.path.join(DB_SOLUTIONS, selected_method))])
selected_group = st.selectbox("Grupo da instância:", grupo_options)

instancias = []
instancia_path = os.path.join(DB_SOLUTIONS, selected_method, selected_group)
if os.path.isdir(instancia_path):
    instancias = sorted([d for d in os.listdir(instancia_path) if os.path.isdir(os.path.join(instancia_path, d))])

selected_instance = st.selectbox("Instância:", instancias)

# Coordenadas
vrp_path = os.path.join(DB_INSTANCES, selected_group, f"{selected_instance}.vrp")
coords = get_coordinates_from_vrp(vrp_path)

# Soluções disponíveis
sol_dir = os.path.join(DB_SOLUTIONS, selected_method, selected_group, selected_instance)
sol_files = sorted([f for f in os.listdir(sol_dir) if f.endswith(".sol")])

col1, col2 = st.columns(2)
vis_mode = col1.selectbox("Modo de visualização:", ["Plotly", "Folium"])
animate = col2.checkbox("Ativar animação automática")

if "frame_index" not in st.session_state:
    st.session_state.frame_index = 0

if animate:
    speed = st.slider("Velocidade da animação (seg):", 0.2, 3.0, 1.0, 0.2)

    current_index = st.session_state.frame_index
    current_sol = sol_files[current_index]

    routes = extract_routes(os.path.join(sol_dir, current_sol))
    st.write(f"🟢 Exibindo: {current_sol}")
    st.subheader(f"🚚 Veículos utilizados: {len(routes)}")

    if vis_mode == "Plotly":
        fig = plot_routes_plotly(routes, coords)
        st.plotly_chart(fig)
    else:
        plot_routes_folium(routes, coords)

    time.sleep(speed)

    st.session_state.frame_index += 1
    if st.session_state.frame_index >= len(sol_files):
        st.session_state.frame_index = 0

    st.rerun()
else:
    st.session_state.frame_index = 0
    selected_sol = st.selectbox("Selecione uma execução:", sol_files)
    routes = extract_routes(os.path.join(sol_dir, selected_sol))
    # Mostrar número total de pontos
    num_pontos = len(coords)
    st.subheader(f"**📍 Número de pontos (incluindo depósito): {num_pontos}**")

    # Mostrar veículos usados
    st.subheader(f"🚚 Veículos utilizados: {len(routes)}")

    highlighted_route = st.selectbox("🔦 Destacar rota:", ["Todas"] + [f"Rota {i + 1}" for i in range(len(routes))])
    highlight_index = None \
        if (
            highlighted_route == "Todas") \
        else (
            int(highlighted_route.split()[1]) - 1)

    if vis_mode == "Plotly":
        fig = plot_routes_plotly(routes, coords, highlight_index=highlight_index)
        st.plotly_chart(fig, use_container_width=True)
    else:
        plot_routes_folium(routes, coords)
