import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DB_PATH = "cvrp_analysis.db"

@st.cache_data
def get_comparative_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM analysis", conn)
    conn.close()
    return df

st.set_page_config(layout="wide")
st.title("📊 Comparativo entre Métodos por Instância")

df = get_comparative_data()

if df.empty:
    st.warning("Nenhuma análise disponível.")
    st.stop()

# Seleciona grupo (A, B, etc.)
groups = sorted(df["instance_name"].str[0].unique())
selected_group = st.selectbox("Grupo da instância:", groups)

filtered_group = df[df["instance_name"].str.startswith(selected_group)]
instances = sorted(filtered_group["instance_name"].unique())
selected_instance = st.selectbox("Instância:", instances)

# Filtra dados da instância
instance_data = df[df["instance_name"] == selected_instance]

if instance_data.empty:
    st.warning("Nenhum dado disponível para esta instância.")
    st.stop()

# Gráfico de barras comparando os métodos
fig = px.bar(
    instance_data,
    x="method",
    y="mean_cost",
    error_y="std_dev",
    text="mean_cost",
    title=f"Comparativo de Custo Médio por Método – {selected_instance}",
    labels={"mean_cost": "Custo Médio", "method": "Método"},
)

fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(yaxis_title="Custo Médio", xaxis_title="Método", uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig, use_container_width=True)

# Tabela de apoio
st.subheader("📋 Estatísticas por Método")
st.dataframe(instance_data[[
    "method", "mean_cost", "std_dev", "min_cost", "max_cost", "median", "coeff_var"
]].rename(columns={
    "method": "Método",
    "mean_cost": "Custo Médio",
    "std_dev": "Desvio Padrão",
    "min_cost": "Mínimo",
    "max_cost": "Máximo",
    "median": "Mediana",
    "coeff_var": "Coef. Variação"
}))
