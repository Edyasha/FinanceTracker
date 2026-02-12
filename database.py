import sqlite3
from datetime import datetime

class TransactionDB:
    def __init__(self, db_name="my_finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL, -- 'income' або 'expense'
                amount REAL,
                category TEXT,
                date DATE
            )
        ''')
        self.conn.commit()

    def add_transaction(self, amount, t_type):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO transactions (amount, date, type) VALUES (?, ?, ?)',
                            (amount, now, t_type))
        self.conn.commit()
        print(f"Запис успішно доданий у базу: {amount}грн.")

    def get_all_transactions(self):
        self.cursor.execute('SELECT amount, date, type FROM transactions ORDER BY date DESC')
        rows = self.cursor.fetchall()
        return rows

    def get_monthly_stats(self):
        current_month = datetime.now().strftime("%Y-%m")

        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions
            WHERE type = "Дохід" AND date LIKE?
        ''', (f"{current_month}%",))
        total_income = self.cursor.fetchone()[0] or 0

        self.cursor.execute('''
             SELECT SUM(amount) FROM transactions
             WHERE type = "Витрата" AND date LIKE?
        ''', (f"{current_month}%",))
        total_expense = self.cursor.fetchone()[0] or 0

        return total_income, total_expense