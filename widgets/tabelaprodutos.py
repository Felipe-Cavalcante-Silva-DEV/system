import tkinter as tk
from tkinter import ttk

def create_products_table(parent):
    # Criando a tabela Treeview
    products_table = ttk.Treeview(parent, columns=("ID", "CODIGO", "Nome", "Estoque", "Preço", "Marca", "Tipo"), show="headings", selectmode="extended")
    products_table.pack(padx=20, pady=20, fill="both", expand=True)

    # Configurando as colunas
    products_table.heading("ID", text="ID")
    products_table.heading("CODIGO", text="CODIGO")
    products_table.heading("Nome", text="Nome")
    products_table.heading("Estoque", text="Estoque")
    products_table.heading("Preço", text="Preço")  
    products_table.heading("Marca", text="Marca")
    products_table.heading("Tipo", text="Tipo")

    products_table.column("ID", width=25, anchor="center")
    products_table.column("CODIGO", width=40, anchor="center")
    products_table.column("Nome", width=150, anchor="center")
    products_table.column("Estoque", width=60, anchor="center")
    products_table.column("Preço", width=60, anchor="center")   
    products_table.column("Marca", width=80, anchor="center")
    products_table.column("Tipo", width=80, anchor="center")

    # Configurando cores alternadas
    products_table.tag_configure("odd", background="white")
    products_table.tag_configure("even", background="#f0f0f0")

    # Retornando a instância da Treeview para manipulação futura
    return products_table
