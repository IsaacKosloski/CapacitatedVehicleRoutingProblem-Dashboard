import streamlit as st

st.set_page_config(page_title="CVRP Dashboard", layout="centered")

st.title("🚚 Bem-vindo ao Dashboard de Análise CVRP")

st.markdown("""
Este painel interativo permite:

- 📊 Visualizar estatísticas de custo de soluções para o CVRP;
- 🛣️ Navegar pelas rotas geradas em cada execução;
- ⏱️ Assistir à animação das soluções;
- 🗺️ Alternar entre visualizações com Plotly ou mapas reais (Folium).

Use o menu lateral para começar 🚀
""")
