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
            data TEXT NOT NULL
        )
    ''')

    # Tabela de itens da venda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id)
        )
    ''')

    conn.commit()
    conn.close()


initialize_sales_db()

def save_sale(cart_items, total_value, vendedor, cliente):
    """
    Salva uma venda no banco de dados, incluindo os itens do carrinho.

    :param cart_items: Lista de itens no carrinho (cada item é um dicionário com dados do produto).
    :param total_value: Valor total da venda.
    :param vendedor: Nome do vendedor.
    :param cliente: Nome do cliente.
    """
    if not cart_items:
        messagebox.showwarning("Aviso", "O carrinho está vazio. Não é possível finalizar a venda.")
        return

    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()

        # Inserir a venda na tabela 'vendas'
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO vendas (total, vendedor, cliente, data)
            VALUES (?, ?, ?, ?)
        ''', (total_value, vendedor, cliente, data_atual))

        venda_id = cursor.lastrowid  # Obter o ID da venda recém-criada

        # Inserir os itens na tabela 'itens_venda'
        for item in cart_items:
            cursor.execute('''
                INSERT INTO itens_venda (venda_id, produto_id, nome, quantidade, preco_unitario, total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (venda_id, item["id"], item["name"], item["quantity"], item["sale_price"], item["quantity"] * item["sale_price"]))


        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Venda registrada com sucesso! ID da venda: {venda_id}")

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao salvar a venda: {e}")


