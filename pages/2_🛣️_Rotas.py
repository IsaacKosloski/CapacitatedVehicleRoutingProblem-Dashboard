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

# 🔎 Listar instâncias disponíveis
grupo_options = sorted([d for d in os.listdir(DB_SOLUTIONS) if os.path.isdir(os.path.join(DB_SOLUTIONS, d))])
selected_group = st.selectbox("Grupo de instância:", grupo_options)

instancias = []
instancia_path = os.path.join(DB_SOLUTIONS, selected_group)
if os.path.isdir(instancia_path):
    instancias = sorted([d for d in os.listdir(instancia_path) if os.path.isdir(os.path.join(instancia_path, d))])


if not instancias:
    st.warning("Nenhuma instância encontrada.")
    st.stop()

selected_instance = st.selectbox("Selecione uma instância:", sorted(instancias))

# 📍 Carrega coordenadas da instância
vrp_path = os.path.join(DB_INSTANCES, selected_instance[0], f"{selected_instance}.vrp")
coords = get_coordinates_from_vrp(vrp_path)

# 📁 Diretório das soluções da instância selecionada
sol_dir = os.path.join(DB_SOLUTIONS, selected_instance[0], selected_instance)
sol_files = sorted([f for f in os.listdir(sol_dir) if f.endswith(".sol")])

# 🌍 Opções de visualização e animação
col1, col2 = st.columns(2)
vis_mode = col1.selectbox("Modo de visualização:", ["Plotly", "Folium"])
animate = col2.checkbox("Ativar animação automática")

# 🚀 Inicializa controle da animação
if "frame_index" not in st.session_state:
    st.session_state.frame_index = 0

if animate:
    speed = st.slider("Velocidade da animação (seg):", 0.2, 3.0, 1.0, 0.2)

    current_index = st.session_state.frame_index
    current_sol = sol_files[current_index]

    routes = extract_routes(os.path.join(sol_dir, current_sol))
    st.write(f"🟢 Exibindo: {current_sol}")

    if vis_mode == "Plotly":
        fig = plot_routes_plotly(routes, coords)
        st.plotly_chart(fig)
    else:
        plot_routes_folium(routes, coords)

    time.sleep(speed)

    # Avança quadro
    st.session_state.frame_index += 1
    if st.session_state.frame_index >= len(sol_files):
        st.session_state.frame_index = 0

    try:
        st.rerun()  # Streamlit >= 1.25
    except AttributeError:
        st.experimental_rerun()  # Versões antigas


else:
    # ⏹️ Reset ao sair da animação
    if "frame_index" in st.session_state:
        st.session_state.frame_index = 0

    selected_sol = st.selectbox("Selecione uma execução:", sol_files)
    routes = extract_routes(os.path.join(sol_dir, selected_sol))

    if vis_mode == "Plotly":
        fig = plot_routes_plotly(routes, coords)
        st.plotly_chart(fig)
    else:
        plot_routes_folium(routes, coords)
