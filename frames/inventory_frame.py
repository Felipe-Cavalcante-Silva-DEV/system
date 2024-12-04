import customtkinter as ctk
import sqlite3

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Lado esquerdo
        self.grid_columnconfigure(1, weight=0)  # Divisor
        self.grid_columnconfigure(2, weight=1)  # Lado direito

        # Divisor (linha vertical) no meio
        self.divider = ctk.CTkFrame(self, width=2, height=600, fg_color="gray")
        self.divider.grid(row=0, column=1, sticky="ns")

        # Lado esquerdo (formulário de cadastro)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Lado direito (exibição de produtos)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Widgets no lado esquerdo
        self.title_label = ctk.CTkLabel(self.left_frame, text="Cadastro de Produtos", font=("Arial", 16))
        self.title_label.pack(padx=20, pady=20)

        self.name_label = ctk.CTkLabel(self.left_frame, text="Nome do Produto:")
        self.name_label.pack(padx=20, pady=5)

        self.name_entry = ctk.CTkEntry(self.left_frame)
        self.name_entry.pack(padx=20, pady=5)

        self.code_label = ctk.CTkLabel(self.left_frame, text="Código:")
        self.code_label.pack(padx=20, pady=5)

        self.code_entry = ctk.CTkEntry(self.left_frame)
        self.code_entry.pack(padx=20, pady=5)

        self.quantity_label = ctk.CTkLabel(self.left_frame, text="Quantidade:")
        self.quantity_label.pack(padx=20, pady=5)

        self.quantity_entry = ctk.CTkEntry(self.left_frame)
        self.quantity_entry.pack(padx=20, pady=5)

        self.sale_price_label = ctk.CTkLabel(self.left_frame, text="Preço de Venda:")
        self.sale_price_label.pack(padx=20, pady=5)

        self.sale_price_entry = ctk.CTkEntry(self.left_frame)
        self.sale_price_entry.pack(padx=20, pady=5)

        self.purchase_price_label = ctk.CTkLabel(self.left_frame, text="Preço de Compra:")
        self.purchase_price_label.pack(padx=20, pady=5)

        self.purchase_price_entry = ctk.CTkEntry(self.left_frame)
        self.purchase_price_entry.pack(padx=20, pady=5)

        self.brand_label = ctk.CTkLabel(self.left_frame, text="Marca:")
        self.brand_label.pack(padx=20, pady=5)

        self.brand_entry = ctk.CTkEntry(self.left_frame)
        self.brand_entry.pack(padx=20, pady=5)

        self.product_type_label = ctk.CTkLabel(self.left_frame, text="Tipo de Produto:")
        self.product_type_label.pack(padx=20, pady=5)

        self.product_type_entry = ctk.CTkEntry(self.left_frame)
        self.product_type_entry.pack(padx=20, pady=5)

        # Botão de Cadastro
        self.add_button = ctk.CTkButton(self.left_frame, text="Cadastrar Produto", command=self.add_product)
        self.add_button.pack(padx=20, pady=20)

        # Widgets no lado direito (exibição de produtos)
        self.search_label = ctk.CTkLabel(self.right_frame, text="Pesquise por Produto", font=("Arial", 16))
        self.search_label.pack(padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(self.right_frame)
        self.search_entry.pack(padx=20, pady=5)

        self.search_button = ctk.CTkButton(self.right_frame, text="Pesquisar", command=self.search_product)
        self.search_button.pack(padx=20, pady=5)

        self.products_table = ctk.CTkTextbox(self.right_frame, width=500, height=200)
        self.products_table.pack(padx=20, pady=20)

    def add_product(self):
        # Função para adicionar produto ao banco de dados
        name = self.name_entry.get()
        code = self.code_entry.get()
        quantity = self.quantity_entry.get()
        sale_price = self.sale_price_entry.get()
        purchase_price = self.purchase_price_entry.get()
        brand = self.brand_entry.get()
        product_type = self.product_type_entry.get()

        # Verifique se todos os campos foram preenchidos
        if not all([name, code, quantity, sale_price, purchase_price, brand, product_type]):
            ctk.CTkMessagebox.show_warning("Atenção", "Preencha todos os campos!")
            return

        # Conectar ao banco de dados
        try:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                sale_price REAL NOT NULL,
                purchase_price REAL NOT NULL,
                brand TEXT NOT NULL,
                product_type TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            INSERT INTO products (name, code, quantity, sale_price, purchase_price, brand, product_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, code, quantity, sale_price, purchase_price, brand, product_type))

            conn.commit()
            conn.close()

            ctk.CTkMessagebox.show_info("Sucesso", "Produto cadastrado com sucesso!")

        except Exception as e:
            ctk.CTkMessagebox.show_error("Erro", f"Erro ao cadastrar: {e}")

    def search_product(self):
        # Função para buscar produto
        search_query = self.search_entry.get()
        
        if not search_query:
            ctk.CTkMessagebox.show_warning("Atenção", "Digite o nome ou código do produto para pesquisar.")
            return

        # Conectar ao banco de dados e procurar pelo produto
        try:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT name, code, quantity, sale_price, purchase_price, brand, product_type FROM products
            WHERE name LIKE ? OR code LIKE ?
            ''', ('%' + search_query + '%', '%' + search_query + '%'))

            products = cursor.fetchall()

            if products:
                result_text = "Nome | Código | Quantidade | Preço Venda | Preço Compra | Marca | Tipo\n"
                result_text += "-" * 80 + "\n"
                for product in products:
                    result_text += " | ".join(str(x) for x in product) + "\n"
                self.products_table.delete(1.0, ctk.END)
                self.products_table.insert(ctk.END, result_text)
            else:
                self.products_table.delete(1.0, ctk.END)
                self.products_table.insert(ctk.END, "Nenhum produto encontrado.")

            conn.close()

        except Exception as e:
            ctk.CTkMessagebox.show_error("Erro", f"Erro ao buscar produtos: {e}")


# Exemplo de inicialização do aplicativo
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    inventory_frame = InventoryFrame(app)
    inventory_frame.pack(fill="both", expand=True)
    app.mainloop()
