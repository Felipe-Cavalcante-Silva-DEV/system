import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from basevendas import save_sale
import datetime

class ExpensesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Widgets do Frame "Expenses"
        self.title_home = ctk.CTkLabel(self, text="Expenses", font=("Arial Bold", 36))
        self.title_home.grid(row=0, column=0, padx=20, pady=20)

        # Botão para finalizar a venda
        self.finalize_button = ctk.CTkButton(self, text="Finalizar Venda", command=self.finalize_sale)
        self.finalize_button.grid(row=1, column=0, padx=20, pady=20)



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
                    INSERT INTO itens_venda (venda_id, produto_id, nome, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venda_id, item["id"], item["name"], item["quantity"], item["sale_price"]))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"Venda registrada com sucesso! ID da venda: {venda_id}")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar a venda: {e}")



    def finalize_sale(self):
        """
        Finaliza a venda, salvando os dados no banco de dados.
        """
        # Obter itens do carrinho
        conn = sqlite3.connect("carrinho.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, code, name, quantity, sale_price FROM carrinho")
        cart_items = [
            {"id": row[0], "code": row[1], "name": row[2], "quantity": row[3], "sale_price": row[4]}
            for row in cursor.fetchall()
        ]
        conn.close()

        if not cart_items:
            messagebox.showwarning("Aviso", "O carrinho está vazio. Não é possível finalizar a venda.")
            return

        # Calcular o total da venda
        total_value = sum(item["quantity"] * item["sale_price"] for item in cart_items)

        # Solicitar informações do vendedor e cliente (simulação)
        vendedor = "Vendedor Padrão"  # Você pode substituir isso por uma entrada de texto na interface
        cliente = "Cliente Padrão"   # Ou solicitar o nome do cliente no momento da venda

        # Salvar a venda
        save_sale(cart_items, total_value, vendedor, cliente)

        # Limpar o carrinho após salvar a venda
        conn = sqlite3.connect("carrinho.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carrinho")
        conn.commit()
        conn.close()

        # Mensagem de confirmação
        messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
