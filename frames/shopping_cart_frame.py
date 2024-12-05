import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

class ShoppingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=8)  # Lado esquerdo (aproximadamente 35%)
        self.grid_columnconfigure(1, weight=1)  # Divisor (fixo)
        self.grid_columnconfigure(2, weight=12)  # Lado direito (aproximadamente 65%)

        # Lado esquerdo (carrinho)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Data
        self.date_button = ctk.CTkButton(self.left_frame, text=self.get_current_date(), font=("Arial", 16), command=self.open_calendar)
        self.date_button.pack(padx=20, pady=20)
        
        # Dropdown para selecionar usuário
        self.user_dropdown = ctk.CTkOptionMenu(self.left_frame, values=self.get_vendedores(), command=self.on_user_select)
        self.user_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")  # Colocando abaixo do botão de data
        
        # Lado direito (exibição de produtos)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Widgets no lado direito (exibição de produtos)
        self.search_label = ctk.CTkLabel(self.right_frame, text="Pesquise por Produto", font=("Arial", 16))
        self.search_label.pack(padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(self.right_frame)
        self.search_entry.pack(padx=20, pady=5)

        self.search_button = ctk.CTkButton(self.right_frame, text="Pesquisar", command=self.search_product)
        self.search_button.pack(padx=20, pady=5)

        # Configurando a tabela do carrinho
        self.products_table = ttk.Treeview(
            self.right_frame,
            columns=("ID", "CODIGO", "Nome", "Preço", "Estoque", "Marca", "Tipo"),
            show="headings",
        )
        self.products_table.pack(padx=20, pady=20, fill="both", expand=True)

        # Configurando as colunas da tabela
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

        # Configurando cores alternadas
        self.products_table.tag_configure("odd", background="white")
        self.products_table.tag_configure("even", background="#f0f0f0")

        # Divisor (linha vertical) no meio
        self.divider = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.divider.grid(row=0, column=1, sticky="ns", rowspan=1)  # Divisória entre os frames

    def get_current_date(self):
        """Função para retornar a data atual no formato YYYY-MM-DD"""
        return datetime.now().strftime("%Y-%m-%d")

    def open_calendar(self):
        """Função para abrir o calendário e permitir a seleção de uma data"""
        # Criar uma nova janela de calendário
        calendar_window = tk.Toplevel(self)  # Usando 'tk' para criar a janela
        calendar_window.title("Selecionar Data")

        # Criar o calendário
        cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=20, pady=20)

        # Função para definir a data escolhida no botão
        def select_date():
            selected_date = cal.get_date()
            self.date_button.configure(text=selected_date)  # Atualiza o texto do botão com a data selecionada
            calendar_window.destroy()  # Fecha a janela do calendário

        # Botão para confirmar a seleção da data
        select_button = ctk.CTkButton(calendar_window, text="Confirmar Data", command=select_date)
        select_button.pack(pady=10)

    def search_product(self):
        # Função para buscar produto
        search_query = self.search_entry.get()

        if not search_query:
            messagebox.showwarning("Atenção", "Digite o nome ou código do produto para pesquisar.")
            return

        try:
            conn = sqlite3.connect("products.db")
            cursor = conn.cursor()

            cursor.execute('''SELECT id, code, name, sale_price, quantity, brand, product_type FROM products
                              WHERE name LIKE ? OR code LIKE ?''', ('%' + search_query + '%', '%' + search_query + '%'))

            products = cursor.fetchall()
            conn.close()

            if products:
                self.populate_table(products)
            else:
                messagebox.showinfo("Resultado", "Nenhum produto encontrado.")
                self.populate_table([])

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")

    def populate_table(self, data):
        """Limpa a tabela e insere novos dados"""
        for row in self.products_table.get_children():
            self.products_table.delete(row)

        for index, item in enumerate(data):
            tag = "even" if index % 2 == 0 else "odd"
            self.products_table.insert("", "end", values=item, tags=(tag,))

    def get_vendedores(self):
        """Recupera os vendedores do banco de dados"""
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT name FROM users WHERE role = ?', ("vendedor",))
        users = c.fetchall()
        conn.close()

        # Converte o resultado para uma lista de nomes
        return [user[0] for user in users]

    def on_user_select(self, selected_user):
        """Evento quando um vendedor é selecionado"""
        print(f"Usuário selecionado: {selected_user}")



    def get_current_date(self):
        # Retorna a data atual no formato desejado
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y")

    def open_calendar(self):
        # Função para abrir o calendário (pode ser implementada)
        print("Abrir calendário")