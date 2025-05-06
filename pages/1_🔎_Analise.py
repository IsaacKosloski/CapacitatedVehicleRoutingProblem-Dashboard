import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "cvrp_analysis.db"

@st.cache_data
def get_analysis_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM analysis", conn)
    conn.close()
    return df

@st.cache_data
def get_solution_data(instance_name, method):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM solutions WHERE instance_name = ? AND method = ?",
        conn, params=(instance_name, method)
    )
    conn.close()
    return df

st.set_page_config(layout="centered")
st.title("🔎 Análise de Soluções CVRP")

# Carrega dados de análise
df_analysis = get_analysis_data()

if df_analysis.empty:
    st.warning("Nenhuma análise encontrada.")
    st.stop()

# Garante que só haja métodos válidos
methods = sorted([m for m in df_analysis["method"].dropna().unique() if isinstance(m, str)])
if not methods:
    st.warning("Nenhum método encontrado no banco de dados.")
    st.stop()

selected_method = st.selectbox("Método de solução:", methods)

# Filtra por método
filtered_by_method = df_analysis[df_analysis["method"] == selected_method]

# Grupos (A, B, E, etc.)
groups = sorted(filtered_by_method["instance_name"].str[0].unique())
selected_group = st.selectbox("Grupo da instância:", groups)

# Instâncias do grupo
filtered = filtered_by_method[filtered_by_method["instance_name"].str.startswith(selected_group)]
instances = sorted(filtered["instance_name"].unique())
selected_instance = st.selectbox("Instância:", instances)

# Mostra estatísticas
try:
    instance_stats = filtered[filtered["instance_name"] == selected_instance].iloc[0]

    st.subheader(f"📈 Estatísticas - {selected_instance} ({selected_method})")
    st.metric("Custo Médio", f"{instance_stats['mean_cost']:.2f}")
    st.metric("Desvio Padrão", f"{instance_stats['std_dev']:.2f}")
    st.metric("Coef. Variação", f"{instance_stats['coeff_var']:.2%}")
    st.metric("Mínimo", f"{instance_stats['min_cost']:.2f}")
    st.metric("Máximo", f"{instance_stats['max_cost']:.2f}")
    st.metric("Mediana", f"{instance_stats['median']:.2f}")

    # Lista as soluções individuais
    df_solutions = get_solution_data(selected_instance, selected_method)
    st.subheader("📋 Soluções individuais")
    st.dataframe(df_solutions[["file_name", "cost", "vehicles_used"]].rename(
        columns={
            "file_name": "Arquivo",
            "cost": "Custo",
            "vehicles_used": "Veículos"
        }
    ))

except IndexError:
    st.error("⚠️ Não foi possível carregar estatísticas para esta seleção.")
