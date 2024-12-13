import sqlite3
from tkinter import messagebox
from basecarrinho import criar_banco


def search_product(search_entry, products_table):
    # Função para buscar produto
    search_query = search_entry.get()

    if not search_query:
        messagebox.showwarning("Atenção", "Digite o nome ou código do produto para pesquisar.")
        return

    try:
        conn = sqlite3.connect("sales.db")
        cursor = conn.cursor()

        cursor.execute(''' 
        SELECT id, code, name, quantity, sale_price, brand, product_type FROM products
        WHERE name LIKE ? OR code LIKE ?
        ''', ('%' + search_query + '%', '%' + search_query + '%'))

        products = cursor.fetchall()
        conn.close()

        # Limpar os dados atuais da tabela
        for row in products_table.get_children():
            products_table.delete(row)

        # Inserir os resultados no Treeview
        if products:
            for i, product in enumerate(products):
                tag = "even" if i % 2 == 0 else "odd"
                products_table.insert("", "end", values=product, tags=(tag,))
        else:
            messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")
        
        
        
        
        





