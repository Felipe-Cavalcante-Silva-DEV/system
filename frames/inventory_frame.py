import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3
from tkinter import ttk


class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Lado esquerdo
        self.grid_columnconfigure(1, weight=0)  # Divisor
        self.grid_columnconfigure(2, weight=1)  # Lado direito

        # Divisor (linha vertical) no meio
        self.divider = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.divider.grid(row=0, column=1, sticky="ns")

        # Lado esquerdo (formulário de cadastro)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Lado direito (exibição de produtos)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Barra seletora no topo do left_frame
        self.cadastro_type = ctk.StringVar(value="Manual")
        self.cadastro_bar = ctk.CTkSegmentedButton(
            self.left_frame,
            values=["Manual", "Outro Tipo 1", "Outro Tipo 2"],
            command=self.change_cadastro_type,
            variable=self.cadastro_type,
        )
        self.cadastro_bar.pack(padx=20, pady=10, fill="x")

        # Inicializar o formulário manual como padrão
        self.form_frame = ctk.CTkFrame(self.left_frame)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.init_manual_form()

        # Widgets no lado direito (exibição de produtos)
        self.search_label = ctk.CTkLabel(self.right_frame, text="Pesquise por Produto", font=("Arial", 16))
        self.search_label.pack(padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(self.right_frame)
        self.search_entry.pack(padx=20, pady=5)

        self.search_button = ctk.CTkButton(self.right_frame, text="Pesquisar", command=self.search_product)
        self.search_button.pack(padx=20, pady=5)

        # Criando a tabela usando Treeview
        self.products_table = ttk.Treeview(self.right_frame, columns=("ID", "CODIGO", "Nome", "Preço", "Estoque", "Marca", "Tipo"), show="headings")
        self.products_table.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Configurando as colunas
        self.products_table.heading("ID", text="ID")
        self.products_table.heading("CODIGO", text="CODIGO")
        self.products_table.heading("Nome", text="Nome")
        self.products_table.heading("Preço", text="Preço")
        self.products_table.heading("Estoque", text="Estoque")
        self.products_table.heading("Marca", text="Marca")
        self.products_table.heading("Tipo", text="Tipo")

        self.products_table.column("ID", width=25, anchor="center")
        self.products_table.column("CODIGO", width=70, anchor="center")
        self.products_table.column("Nome", width=180, anchor="w")
        self.products_table.column("Preço", width=90, anchor="e")
        self.products_table.column("Estoque", width=90, anchor="center")
        self.products_table.column("Marca", width=100, anchor="w")
        self.products_table.column("Tipo", width=100, anchor="w")

        self.init_database()

    def init_database(self):
        # Inicializar banco de dados
        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            sale_price REAL NOT NULL,
            purchase_price REAL NOT NULL,
            brand TEXT NOT NULL,
            product_type TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def change_cadastro_type(self, tipo):
        # Alterne entre tipos de cadastro
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        if tipo == "Manual":
            self.init_manual_form()
        elif tipo == "Outro Tipo 1":
            self.init_outro_tipo1_form()
        elif tipo == "Outro Tipo 2":
            self.init_outro_tipo2_form()

    def init_manual_form(self):
        # Campos de formulário para cadastro manual
        ctk.CTkLabel(self.form_frame, text="Cadastro Manual", font=("Arial Bold", 16)).pack(padx=20, pady=10)

        self.name_label = ctk.CTkLabel(self.form_frame, text="Nome do Produto:")
        self.name_label.pack(padx=20, pady=5)

        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.pack(padx=20, pady=5)

        self.code_label = ctk.CTkLabel(self.form_frame, text="Código:")
        self.code_label.pack(padx=20, pady=5)

        self.code_entry = ctk.CTkEntry(self.form_frame)
        self.code_entry.pack(padx=20, pady=5)

        self.quantity_label = ctk.CTkLabel(self.form_frame, text="Quantidade:")
        self.quantity_label.pack(padx=20, pady=5)

        self.quantity_entry = ctk.CTkEntry(self.form_frame)
        self.quantity_entry.pack(padx=20, pady=5)

        self.sale_price_label = ctk.CTkLabel(self.form_frame, text="Preço de Venda:")
        self.sale_price_label.pack(padx=20, pady=5)

        self.sale_price_entry = ctk.CTkEntry(self.form_frame)
        self.sale_price_entry.pack(padx=20, pady=5)

        self.purchase_price_label = ctk.CTkLabel(self.form_frame, text="Preço de Compra:")
        self.purchase_price_label.pack(padx=20, pady=5)

        self.purchase_price_entry = ctk.CTkEntry(self.form_frame)
        self.purchase_price_entry.pack(padx=20, pady=5)

        self.brand_label = ctk.CTkLabel(self.form_frame, text="Marca:")
        self.brand_label.pack(padx=20, pady=5)

        self.brand_entry = ctk.CTkEntry(self.form_frame)
        self.brand_entry.pack(padx=20, pady=5)

        self.product_type_label = ctk.CTkLabel(self.form_frame, text="Tipo de Produto:")
        self.product_type_label.pack(padx=20, pady=5)

        self.product_type_entry = ctk.CTkEntry(self.form_frame)
        self.product_type_entry.pack(padx=20, pady=5)

        # Botão de Cadastro
        self.add_button = ctk.CTkButton(self.form_frame, text="Cadastrar Produto", command=self.add_product)
        self.add_button.pack(padx=20, pady=20)

    def add_product(self):
        # Função para adicionar produto ao banco de dados
        name = self.name_entry.get()
        code = self.code_entry.get()
        quantity = self.quantity_entry.get()
        sale_price = self.sale_price_entry.get()
        purchase_price = self.purchase_price_entry.get()
        brand = self.brand_entry.get()
        product_type = self.product_type_entry.get()

        if not all([name, code, quantity, sale_price, purchase_price, brand, product_type]):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            conn = sqlite3.connect("products.db")
            cursor = conn.cursor()

            # Verifica se já existe um produto com o mesmo código ou nome
            cursor.execute('''
            SELECT id FROM products WHERE code = ? OR name = ?
            ''', (code, name))
            result = cursor.fetchone()

            if result:
                # Se já existir código ou nome, exibe erro
                messagebox.showerror("Erro", "Já existe um produto com este código ou nome.")
            else:
                # Caso contrário, insere um novo registro
                cursor.execute('''
                INSERT INTO products (name, code, quantity, sale_price, purchase_price, brand, product_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, code, quantity, sale_price, purchase_price, brand, product_type))
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

            conn.commit()
            conn.close()
            self.clear_form()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")



    def search_product(self):
        # Função para buscar produto
        search_query = self.search_entry.get()

        if not search_query:
            messagebox.showwarning("Atenção", "Digite o nome ou código do produto para pesquisar.")
            return

        try:
            conn = sqlite3.connect("products.db")
            cursor = conn.cursor()

            cursor.execute('''
            SELECT id, code, name, sale_price, quantity, brand, product_type FROM products
            WHERE name LIKE ? OR code LIKE ?
            ''', ('%' + search_query + '%', '%' + search_query + '%'))

            products = cursor.fetchall()
            conn.close()

            # Limpar os dados atuais da tabela
            for row in self.products_table.get_children():
                self.products_table.delete(row)

            # Inserir os resultados no Treeview
            if products:
                for product in products:
                    self.products_table.insert("", "end", values=product)
            else:
                messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")

    def clear_form(self):
        # Limpa o formulário após o cadastro
        for entry in [self.name_entry, self.code_entry, self.quantity_entry,
                      self.sale_price_entry, self.purchase_price_entry,
                      self.brand_entry, self.product_type_entry]:
            entry.delete(0, ctk.END)
