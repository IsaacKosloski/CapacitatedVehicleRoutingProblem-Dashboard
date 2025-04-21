import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\zaack\PycharmProjects\CapacitatedVehicleRoutingProblem-Dashboard\cvrp_analysis.db"

@st.cache_data
def get_analysis_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM analysis", conn)
    conn.close()
    return df

@st.cache_data
def get_solution_data(instance_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM solutions WHERE instance_name = ?", conn, params=(instance_name,)
    )
    conn.close()
    return df

st.title("📊 Análise de Soluções CVRP")

df_analysis = get_analysis_data()

if df_analysis.empty:
    st.warning("Nenhuma análise encontrada.")
    st.stop()

df_analysis["group"] = df_analysis["instance_name"].str[0]  # extrai A, B, E...

group_list = sorted(df_analysis["group"].unique())
selected_group = st.selectbox("Grupo de instância:", group_list)

filtered_df = df_analysis[df_analysis["group"] == selected_group]
selected_instance = st.selectbox("Instância:", sorted(filtered_df["instance_name"]))


instance_stats = df_analysis[df_analysis["instance_name"] == selected_instance].iloc[0]

st.metric("Custo Médio", f"{instance_stats['mean_cost']:.2f}")
st.metric("Desvio Padrão", f"{instance_stats['std_dev']:.2f}")
st.metric("Coef. Variação", f"{instance_stats['coeff_var']:.2%}")
st.metric("Mínimo", f"{instance_stats['min_cost']:.2f}")
st.metric("Máximo", f"{instance_stats['max_cost']:.2f}")
st.metric("Mediana", f"{instance_stats['median']:.2f}")

df_solutions = get_solution_data(selected_instance)
st.subheader("📋 Custos Individuais")
st.dataframe(df_solutions[["file_name", "cost", "vehicles_used"]].rename(
    columns={"file_name": "Arquivo", "cost": "Custo", "vehicles_used": "Veículos"}
))
