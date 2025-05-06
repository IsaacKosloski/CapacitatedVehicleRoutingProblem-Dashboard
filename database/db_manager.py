import sqlite3

class DatabaseManager:
    def __init__(self, db_path="cvrp_analysis.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute('DROP TABLE IF EXISTS solutions')
            cursor.execute('DROP TABLE IF EXISTS analysis')

            cursor.execute('''
                CREATE TABLE solutions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instance_name TEXT,
                    file_name TEXT,
                    cost REAL,
                    vehicles_used INTEGER,
                    method TEXT
                );
            ''')

            cursor.execute('''
                CREATE TABLE analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instance_name TEXT,
                    method TEXT,
                    mean_cost REAL,
                    std_dev REAL,
                    min_cost REAL,
                    max_cost REAL,
                    median REAL,
                    range REAL,
                    coeff_var REAL
                );
            ''')

    def insert_solution(self, instance_name, file_name, cost, vehicles_used, method):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO solutions (instance_name, file_name, cost, vehicles_used, method)
                VALUES (?, ?, ?, ?, ?)
            ''', (instance_name, file_name, cost, vehicles_used, method))

    def solution_exists(self, instance_name, file_name, method):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM solutions
                WHERE instance_name = ? AND file_name = ? AND method = ?
            ''', (instance_name, file_name, method))
            return cursor.fetchone() is not None

    def get_costs_by_instance_and_method(self, instance_name, method):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT cost FROM solutions
                WHERE instance_name = ? AND method = ?
            ''', (instance_name, method))
            return [row[0] for row in cursor.fetchall()]

    def insert_analysis(self, instance_name, method, stats):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analysis (
                    instance_name, method,
                    mean_cost, std_dev, min_cost, max_cost,
                    median, range, coeff_var
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                instance_name, method,
                stats["mean"], stats["std_dev"],
                stats["min"], stats["max"],
                stats["median"], stats["range"],
                stats["coeff_var"]
            ))

    def get_all_methods(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT method FROM solutions")
            return [row[0] for row in cursor.fetchall()]
