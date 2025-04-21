import sqlite3
from config import DB_NAME

class DatabaseManager:
    def __init__(self):
        self.db_name = DB_NAME

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_name TEXT,
                file_name TEXT,
                cost REAL,
                vehicles_used INTEGER
            );

            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis (
                instance_name TEXT PRIMARY KEY,
                mean_cost REAL,
                std_dev REAL,
                min_cost REAL,
                max_cost REAL,
                median REAL,
                range REAL,
                coeff_var REAL
            );
            ''')

    def insert_solution(self, instance_name, file_name, cost, vehicles_used):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           INSERT INTO solutions (instance_name, file_name, cost, vehicles_used)
                           VALUES (?, ?, ?, ?)
                           ''', (instance_name, file_name, cost, vehicles_used))

    def get_costs_by_instance(self, instance_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT cost FROM solutions WHERE instance_name = ?', (instance_name,))
            return [row[0] for row in cursor.fetchall()]

    def insert_analysis(self, instance_name, stats):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO analysis
                (instance_name, mean_cost, std_dev, min_cost, max_cost, median, range, coeff_var)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (instance_name, *stats))

    def solution_exists(self, instance_name, file_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM solutions
                WHERE instance_name = ? AND file_name = ?
            ''', (instance_name, file_name))
            return cursor.fetchone() is not None
