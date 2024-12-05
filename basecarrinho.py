import sqlite3

conn = sqlite3.connect('carrinho.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            sale_price REAL NOT NULL,
            brand TEXT NOT NULL,
            product_type TEXT NOT NULL
        ); 
''')
