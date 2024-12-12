import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

def create_cart_table(parent):
    """Cria a tabela Treeview para o carrinho."""
    # Criando a tabela Treeview
    cart_table = ttk.Treeview(parent, columns=("ID", "Codigo", "Nome", "Quantidade", "Preço"), show="headings")
    cart_table.pack(padx=20, pady=20, fill="both", expand=True)

    # Configurando as colunas
    cart_table.heading("ID", text="ID")
    cart_table.heading("Codigo", text="CODIGO")
    cart_table.heading("Nome", text="Nome")
    cart_table.heading("Quantidade", text="Quantidade")
    cart_table.heading("Preço", text="Preço")

    cart_table.column("ID", width=25, anchor="center")
    cart_table.column("Codigo", width=40, anchor="center")
    cart_table.column("Nome", width=150, anchor="center")
    cart_table.column("Quantidade", width=80, anchor="center")
    cart_table.column("Preço", width=60, anchor="center")

    # Configurando cores alternadas
    cart_table.tag_configure("odd", background="white")
    cart_table.tag_configure("even", background="#f0f0f0")

    # Vinculando evento de duplo clique
    cart_table.bind("<Double-1>", lambda event: edit_cell(cart_table, event))

    return cart_table

def edit_cell(cart_table, event):
    """Edita o valor da célula na Treeview e atualiza o banco de dados."""
    # Identificar o item e a coluna selecionados
    item_id = cart_table.focus()
    column_index = int(cart_table.identify_column(event.x).replace("#", "")) - 1

    # Bloquear edição de colunas específicas (ID, Codigo, Nome)
    if column_index in (0, 1, 2):  # Índices das colunas que não podem ser editadas
        messagebox.showwarning("Aviso", "Esta coluna não pode ser editada.")
        return

    # Obter valores atuais
    current_values = cart_table.item(item_id, "values")
    current_value = current_values[column_index]

    # Solicitar novo valor
    new_value = simpledialog.askstring("Editar", "Novo valor:", initialvalue=current_value)
    if new_value is None:  # Cancelar edição
        return

    # Verificar se o novo valor para a quantidade é válido
    if column_index == 3:  # Coluna de quantidade
        try:
            new_value = int(new_value)
            if new_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro positivo.")
            return

        # Calcular novo preço total
        unit_price = float(current_values[4].replace(",", ".")) / int(current_values[3])  # Preço unitário atual
        new_sale_price = unit_price * new_value
    else:
        new_sale_price = float(current_values[4].replace("R$", "").replace(",", "."))  # Remove R$ and replace comma with period


    # Atualizar a Treeview
    new_values = list(current_values)
    new_values[column_index] = new_value
    new_values[4] = f"{new_sale_price:.2f}".replace(".", ",")  # Atualizar o preço total na exibição
    cart_table.item(item_id, values=new_values)

    # Atualizar o banco de dados
    column_names = ["id", "code", "name", "quantity", "sale_price"]
    try:
        with sqlite3.connect("carrinho.db") as conn:
            cursor = conn.cursor()

            # Atualizar a quantidade e o preço no banco de dados
            cursor.execute(
                f"UPDATE carrinho SET {column_names[column_index]} = ?, sale_price = ? WHERE id = ?",
                (new_value, new_sale_price, current_values[0])
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao atualizar o banco de dados: {e}")
