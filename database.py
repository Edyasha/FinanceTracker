import sqlite3

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
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def add_transaction(self, amount, category, date, t_type):
        self.cursor.execute('INSERT INTO transactions (amount, category, date, t_type) VALUES (?, ?, ?, ?)',
                            (amount, category, date, t_type))
        self.conn.commit()