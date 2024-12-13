import sqlite3
from datetime import datetime
from tkinter import messagebox

def initialize_sales_db():
    """
    Cria as tabelas necessárias para salvar vendas e itens associados.
    """
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    # Tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            vendedor TEXT NOT NULL,
            cliente TEXT NOT NULL,
            data TEXT NOT NULL,
            parcelas INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # Tabela de itens da venda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            code TEXT NOT NULL,
            venda_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id)
    
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parcelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            valor_parcela REAL NOT NULL,              
            cliente TEXT NOT NULL,
            data_parcela TEXT NOT NULL,
            pagou TEXT NOT NULL,
            FOREIGN KEY (data_parcela) REFERENCES vendas(data),
            FOREIGN KEY (venda_id) REFERENCES vendas(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            sale_price REAL NOT NULL,
            purchase_price REAL NOT NULL,
            brand TEXT NOT NULL,
            product_type TEXT NOT NULL
        )
        ''')


    conn.commit()
    conn.close()


initialize_sales_db()

