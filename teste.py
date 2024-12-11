import sqlite3
import customtkinter as ctk
from datetime import datetime
import os
from PIL import Image
from frames.home_frame import HomeFrame
from frames.inventory_frame import InventoryFrame
from frames.admin_panel_frame import AdminPanelFrame
from frames.shopping_cart_frame import ShoppingFrame
from frames.expenses_frame import ExpensesFrame
from widgets.tabelacarrinho import create_cart_table
from widgets.tabelaprodutos import create_products_table

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SYS")
         # Inicialmente com tamanho menor  (275x250)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        
        def get_vendedores():
            conn = sqlite3.connect("users.db")  # Conecta ao banco de dados
            cursor = conn.cursor()
            query = "SELECT name FROM users WHERE role = 'VENDEDOR' COLLATE NOCASE"  # Query para selecionar os nomes dos vendedores
            cursor.execute(query)
            vendedores = [row[0] for row in cursor.fetchall()]  # Extrai os nomes dos resultados
            conn.close()  # Fecha a conexão
            return vendedores
    
    
        vendedores = get_vendedores()
        self.option_button = ctk.CTkOptionMenu(self, values=vendedores, font=("Arial", 16),)
        self.option_button.pack()
        
        
        # Para resgatar o valor selecionado
        vendedor_selecionado = self.option_button.get()

        # Agora, você pode usar essa informação para fazer o que precisar
        print(f"Vendedor selecionado: {vendedor_selecionado}")

        
    
    
    
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
