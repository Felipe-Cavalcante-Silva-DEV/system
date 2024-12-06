import tkinter as tk
from tkinter import ttk

def create_cart_table(parent):
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
    

    # Retornando a instância da Treeview para manipulação futura
    return cart_table
