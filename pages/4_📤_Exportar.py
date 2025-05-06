import streamlit as st
import pandas as pd
import sqlite3
import io

DB_PATH = "cvrp_analysis.db"


def get_dataframe(table: str):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


st.set_page_config(layout="wide")
st.title("📤 Exportar Análises e Soluções")

tabs = st.tabs(["📊 Análise", "📋 Soluções", "🌐 API (Simulada)"])

# ---------------- ANALYSIS EXPORT ----------------
with tabs[0]:
    st.subheader("📊 Dados de Análise")

    df_analysis = get_dataframe("analysis")
    st.dataframe(df_analysis)

    col1, col2 = st.columns(2)
    with col1:
        csv = df_analysis.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Baixar CSV", csv, "analysis.csv", "text/csv")

    with col2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_analysis.to_excel(writer, index=False, sheet_name="Análise")
        st.download_button("⬇️ Baixar XLSX", output.getvalue(), "analysis.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- SOLUTIONS EXPORT ----------------
with tabs[1]:
    st.subheader("📋 Soluções Individuais")
    df_solutions = get_dataframe("solutions")
    st.dataframe(df_solutions)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇️ Baixar CSV", df_solutions.to_csv(index=False).encode("utf-8"), "solutions.csv",
                           "text/csv")

    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df_solutions.to_excel(writer, index=False, sheet_name="Soluções")
        st.download_button("⬇️ Baixar XLSX", buffer.getvalue(), "solutions.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ---------------- API SIMULADA ----------------
with tabs[2]:
    st.subheader("🌐 Acesso Externo via API (Simulação Local)")

    st.markdown("""
    Embora o Streamlit não seja um framework de API, você pode usar scripts Python separados com `Flask`, `FastAPI`, ou expor os dados por arquivos.

    Aqui está um exemplo de retorno JSON da análise:
    """)

    df_json = df_analysis.to_dict(orient="records")
    st.json(df_json[:5])  # Mostra os primeiros 5 registros

    st.markdown(
        "Para integrar com outras aplicações, use um serviço Flask + SQLite ou FastAPI + Pandas para servir este conteúdo.")
