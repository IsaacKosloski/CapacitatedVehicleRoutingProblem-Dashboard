import sqlite3

DB_PATH = "cvrp_analysis.db"
MAX_ROWS = 10  # Número de registros que serão mostrados por tabela

def print_table_data(cursor, table_name):
    print(f"\n📘 Tabela: {table_name}")
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {MAX_ROWS}")
        rows = cursor.fetchall()

        # Obtem nomes das colunas
        column_names = [description[0] for description in cursor.description]
        print(" | ".join(column_names))
        print("-" * 60)

        for row in rows:
            print(" | ".join(str(item) for item in row))

        if not rows:
            print("Tabela vazia.")
    except Exception as e:
        print(f"Erro ao acessar {table_name}: {e}")

def main():
    print(f"🔍 Conectando ao banco de dados: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    if not tables:
        print("⚠️ Nenhuma tabela encontrada no banco.")
        return

    print("📄 Tabelas encontradas:")
    for table in tables:
        print(f" - {table}")

    for table in tables:
        print_table_data(cursor, table)

    conn.close()
    print("\n✅ Finalizado.")

if __name__ == "__main__":
    main()
