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
        self.finalize_button.grid(row=2, column=0, padx=20, pady=20)

    def finalize_sale(self):
        """
        Finaliza a venda, salvando os dados no banco de dados.
        """
        vendedor = self.selected_vendedor.get()  # Obter o vendedor selecionado
        cliente = self.selected_cliente.get()  # Obter o cliente selecionado

        if vendedor == "Nenhum Vendedor" or cliente == "Nenhum Cliente":
            messagebox.showwarning("Aviso", "Por favor, selecione um vendedor e um cliente.")
            return

        # Obter itens do carrinho (exemplo simplificado)
        cart_items = [
            {"id": 1, "name": "Produto A", "quantity": 2, "sale_price": 10.0},
            {"id": 2, "name": "Produto B", "quantity": 1, "sale_price": 20.0}
        ]

        # Calcular o total da venda
        total_value = sum(item["quantity"] * item["sale_price"] for item in cart_items)

        # Salvar a venda no banco de dados
        save_sale(cart_items, total_value, vendedor, cliente)

        messagebox.showinfo("Sucesso", f"Venda registrada com sucesso! Vendedor: {vendedor}, Cliente: {cliente}")

    def save_sale(self, cart_items, total_value, vendedor, cliente):
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
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
