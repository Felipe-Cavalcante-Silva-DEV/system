import tkinter as tk
from tkinter import ttk


def create_edit_table(parent):
    # Criando a tabela Treeview
    editabel_table = ttk.Treeview(parent, columns=("ID Venda", "CODIGO", "Nome", "Quantidade", "Preço Unidade", "Preço Total"), show="headings", selectmode="extended")
    editabel_table.pack(padx=20, pady=20, fill="both", expand=True)

    # Configurando as colunas
    editabel_table.heading("ID Venda", text="ID Venda")
    editabel_table.heading("CODIGO", text="CODIGO")
    editabel_table.heading("Nome", text="Nome")
    editabel_table.heading("Quantidade", text="Quantidade")
    editabel_table.heading("Preço Unidade", text="Preço Unidade")  
    editabel_table.heading("Preço Total", text="Preço Total")
    

    editabel_table.column("ID Venda", width=25, anchor="center")
    editabel_table.column("CODIGO", width=40, anchor="center")
    editabel_table.column("Nome", width=150, anchor="center")
    editabel_table.column("Quantidade", width=60, anchor="center")
    editabel_table.column("Preço Unidade", width=60, anchor="center")   
    editabel_table.column("Preço Total", width=60, anchor="center") 
    

    # Configurando cores alternadas
    editabel_table.tag_configure("odd", background="white")
    editabel_table.tag_configure("even", background="#f0f0f0")

    # Retornando a instância da Treeview para manipulação futura
    return editabel_table

