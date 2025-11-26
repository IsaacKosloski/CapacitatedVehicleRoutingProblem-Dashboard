import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Dashboard CVRP",
    page_icon="🚚",
    layout="wide"
)

# Título principal
st.title("🚚 Capacitated Vehicle Routing Problem Dashboard")
st.markdown("Bem-vindo ao painel de análise e visualização de soluções para o **Problema de Roteamento de Veículos com Capacidade (CVRP)**.")

st.markdown("---")
st.markdown("""
Este dashboard permite:

- 📊 Analisar estatísticas agregadas por instância e método
- 📉 Comparar métodos como *BruteForce*, *ILS* e *GRASP*
- 🛣️ Visualizar as rotas executadas em mapas e gráficos
- 📤 Exportar os dados ou acessar uma simulação de API externa
""")

st.markdown("---")
st.info("ℹ️ Use a **barra lateral** para navegar entre as páginas.")

# -------------------------- SIDEBAR --------------------------
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/11632418?v=4", width=100)

    st.markdown("## 🧭 Navegação")
    st.markdown("---")

    st.markdown("### 🔎 Análises")
    st.page_link("pages/1_🔎_Analise.py", label="Análise Estatística", icon="📈")
    st.page_link("pages/3_📊_Comparativo.py", label="Comparativo por Método", icon="📊")

    st.markdown("### 🛣️ Visualização")
    st.page_link("pages/2_🛣️_Rotas.py", label="Visualizar Rotas", icon="🗺️")

    st.markdown("### 📤 Exportação")
    st.page_link("pages/4_📤_Exportar.py", label="Exportar Dados", icon="📤")

    st.markdown("---")
    st.markdown("👨‍💻 Desenvolvido por **Isaac Kosloski**")
    st.link_button("🔗 GitHub", "https://github.com/IsaacKosloski")
