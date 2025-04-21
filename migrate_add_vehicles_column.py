import sqlite3

DB_PATH = "cvrp_analysis.db"


def add_vehicles_column_if_missing():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se a coluna 'vehicles_used' já existe
    cursor.execute("PRAGMA table_info(solutions);")
    columns = [col[1] for col in cursor.fetchall()]

    if 'vehicles_used' not in columns:
        print("🛠️ Adicionando coluna 'vehicles_used' à tabela 'solutions'...")
        cursor.execute("ALTER TABLE solutions ADD COLUMN vehicles_used INTEGER;")
        conn.commit()
        print("✅ Coluna adicionada com sucesso.")
    else:
        print("ℹ️ A coluna 'vehicles_used' já existe. Nenhuma alteração foi feita.")

    conn.close()


if __name__ == "__main__":
    add_vehicles_column_if_missing()
