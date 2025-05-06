import sqlite3

DB_PATH = "cvrp_analysis.db"


def add_method_column_if_missing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se a coluna 'method' já existe na tabela 'analysis'
    cursor.execute("PRAGMA table_info(analysis);")
    columns = [col[1] for col in cursor.fetchall()]

    if 'method' not in columns:
        print("🛠️ Adicionando coluna 'method' à tabela 'analysis'...")
        cursor.execute("ALTER TABLE analysis ADD COLUMN method TEXT;")
        conn.commit()
        print("✅ Coluna adicionada com sucesso.")
    else:
        print("ℹ️ A coluna 'method' já existe na tabela 'analysis'. Nenhuma alteração foi feita.")

    conn.close()


if __name__ == "__main__":
    add_method_column_if_missing()
