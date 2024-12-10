import customtkinter as ctk
import tkinter.messagebox as messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from widgets.tabelaprodutos import create_products_table
from widgets.tabelacarrinho import create_cart_table
from basecarrinho import criar_banco



def get_vendedores():
        conn = sqlite3.connect("users.db")  # Conecta ao banco de dados
        cursor = conn.cursor()
        query = "SELECT name FROM users WHERE role = 'VENDEDOR' COLLATE NOCASE"  # Query para selecionar os nomes dos vendedores
        cursor.execute(query)
        vendedores = [row[0] for row in cursor.fetchall()]  # Extrai os nomes dos resultados
        conn.close()  # Fecha a conexão
        return vendedores

class ShoppingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid
        self.grid_rowconfigure(0, weight=1)  # Linha 0 com peso 1
        self.grid_rowconfigure(1, weight=1) 
        
        self.grid_columnconfigure(0, weight=1)  # Lado esquerdo (aproximadamente 35%)
        self.grid_columnconfigure(1, weight=0)  # Divisor (fixo)
        self.grid_columnconfigure(2, weight=1)  # Lado direito (aproximadamente 65%)

        # Lado esquerdo (carrinho)
        self.left_frame_up = ctk.CTkFrame(self)
        self.left_frame_up.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        self.left_frame_up.grid_rowconfigure(0, weight=1)  # Ajusta a linha 0
        self.left_frame_up.grid_rowconfigure(1, weight=1)  # Ajusta a linha 1
        self.left_frame_up.grid_rowconfigure(2, weight=1)  # Ajusta a linha 2
        self.left_frame_up.grid_rowconfigure(3, weight=1)    # Ajusta a linha 3
        self.left_frame_up.grid_columnconfigure(0, weight=1)  # Ajusta a coluna 0
        self.left_frame_up.grid_columnconfigure(1, weight=1) 
        self.left_frame_up.grid_columnconfigure(2, weight=3)
        

        self.car_label = ctk.CTkLabel(self.left_frame_up, text="Carrinho de Vendas", font=("Arial", 16))
        self.car_label.place(relx=0.5, rely=0.05, anchor="center")
        
        # Data  
        self.data_label = ctk.CTkLabel(self.left_frame_up, text="Data", font=("Arial", 16))
        self.data_label.grid(row=0, column=0, padx=20, pady=(50, 15), sticky="s")
        
        self.date_button = ctk.CTkButton(self.left_frame_up, text=self.get_current_date(), font=("Arial", 16), command=self.open_calendar)
        self.date_button.grid(row=1, column=0, padx=20, sticky="n")

        
        # DROPMENU DE VENDEDOR
        self.option_label = ctk.CTkLabel(self.left_frame_up, text="Vendedor", font=("Arial", 16))
        self.option_label.grid(row=0, column=1, padx=20, pady=(50, 15), sticky="s") 

        vendedores = get_vendedores()
        self.option_button = ctk.CTkOptionMenu(self.left_frame_up, values=vendedores, font=("Arial", 16),)
        self.option_button.grid(row=1, column=1, padx=20, sticky="n")

        # BOTÃO CRIAR CARRINHO
        self.criar_carrinho_label = ctk.CTkLabel(self.left_frame_up, text="Criar Carrinho", font=("Arial", 16))
        self.criar_carrinho_label.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="s") 

        self.criar_carrinho_button = ctk.CTkButton(self.left_frame_up, text="Criar Carrinho", font=("Arial", 16), command=self.carregar_dados)
        self.criar_carrinho_button.grid(row=3, column=0, padx=20, sticky="n",)
        
        
        # DELETAR PRODUTO CARRINHO
        self.deletar_produto_label = ctk.CTkLabel(self.left_frame_up, text="Deletar Produto", font=("Arial", 16))
        self.deletar_produto_label.grid(row=2, column=1, padx=20, pady=(0, 15), sticky="s")
                        
        self.deletar_produto_button = ctk.CTkButton(self.left_frame_up, text="Deletar Produto", font=("Arial", 16), command=self.delete_selected)
        self.deletar_produto_button.grid(row=3, column=1, padx=20, sticky="n",)


        # DROPMENU DE CLIENTE
        self.cliente_label = ctk.CTkLabel(self.left_frame_up, text="Cliente", font=("Arial", 16))
        self.cliente_label.grid(row=2, column=2, padx=20, pady=(0, 15), sticky="s") 

        self.cliente_button = ctk.CTkOptionMenu(self.left_frame_up, values=["cliente1", "cliente2"], font=("Arial", 16),)
        self.cliente_button.grid(row=3, column=2, padx=20, sticky="n")

        self.left_frame_down = ctk.CTkFrame(self)
        self.left_frame_down.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        
        
        self.cart_table = create_cart_table(self.left_frame_down)

            
        # Frame superior direito
        self.right_frame_up = ctk.CTkFrame(self)
        self.right_frame_up.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Configuração do layout da grid no frame
        self.right_frame_up.grid_columnconfigure(0, weight=1)  # Configura única coluna
        self.right_frame_up.grid_rowconfigure(0, weight=1)     # Linha para o título
        self.right_frame_up.grid_rowconfigure(1, weight=1)     # Linha para a entrada
        self.right_frame_up.grid_rowconfigure(2, weight=1)     # Linha para o botão "Pesquisar"
        self.right_frame_up.grid_rowconfigure(3, weight=1)     # Linha intermediária
        self.right_frame_up.grid_rowconfigure(4, weight=0)     # Linha para o botão no canto

        # Widgets no lado direito (exibição de produtos)
        self.search_label = ctk.CTkLabel(self.right_frame_up, text="Pesquise por Produto", font=("Arial", 16))
        self.search_label.grid(row=0, column=0, pady=10, sticky="n")  # Centralizado horizontalmente

        self.search_entry = ctk.CTkEntry(self.right_frame_up)
        self.search_entry.grid(row=1, column=0, pady=10, sticky="n")  # Centralizado horizontalmente

        self.search_button = ctk.CTkButton(self.right_frame_up, text="Pesquisar", command=self.search_product)
        self.search_button.grid(row=2, column=0, pady=10, sticky="n")  # Centralizado horizontalmente

        # Último botão no canto inferior direito com padding visual
        self.add_to_cart_button = ctk.CTkButton(self.right_frame_up, text="Adicionar Ao Carrinho", command=self.on_button_click)
        self.add_to_cart_button.grid(row=4, column=0, sticky="se", padx=70, pady=20)  # Espaço controlado





        self.right_frame_down = ctk.CTkFrame(self)
        self.right_frame_down.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # Configurando a tabela do carrinho
        self.products_table = create_products_table(self.right_frame_down)
        self.products_table.pack(padx=20, pady=20, fill="both", expand=True)

        

         # Divisória entre os frames

        # Divisor (linha vertical) no meio
        self.divider = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.divider.grid(row=0, column=1, sticky="ns", rowspan=2)  # Divisória entre os frames

    
    
    
    

        

    def on_button_click(self):
        """Adicionar produtos selecionados no carrinho e armazenar no banco de dados"""
        selected_items = self.products_table.selection()  # Obtém os itens selecionados na Treeview
        if not selected_items:
            messagebox.showinfo("Aviso", "Selecione pelo menos um produto!")
            return

        # Conectar ao banco de dados e garantir que a tabela 'carrinho' exista
        conn = sqlite3.connect('carrinho.db')
        cursor = conn.cursor()

        # Criar a tabela, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                sale_price REAL NOT NULL
            );
        ''')

        for item in selected_items:
            # Obter os dados do produto selecionado
            item_values = self.products_table.item(item, "values")
            id = item_values[0]
            nome = item_values[2]       # Nome do produto
            codigo = item_values[1]     # Código do produto
            quantidade = item_values[4] # Quantidade disponível
            preco = item_values[3]      # Preço do produto

            # Inserir os dados na tabela do carrinho
            try:
                cursor.execute('''
                    INSERT INTO carrinho (id, code, name, sale_price, quantity)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id, codigo, nome, preco, quantidade))

                conn.commit()  # Confirmar a inserção no banco de dados

                # Opcional: mensagem de confirmação
                print(f'Produto "{nome}" adicionado ao carrinho.')
            
            except sqlite3.IntegrityError:
                # Caso já exista o produto (unique constraint no código)
                print(f'O produto "{nome}" já está no carrinho.')

        conn.close()  # Fechar a conexão com o banco



    def delete_selected(self):
        """Deleta os itens selecionados"""
        selected_items = self.cart_table.selection()  # Obtem os IDs dos itens selecionados
        if not selected_items:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            return

        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar {len(selected_items)} item(s)?")
        if confirm:
            # Conectar ao banco de dados fora do loop
            conn = sqlite3.connect('carrinho.db')
            cursor = conn.cursor()

            for item_id in selected_items:
                # Deletar do banco de dados usando o iid da Treeview, que é o id do banco de dados
                cursor.execute("DELETE FROM carrinho WHERE id = ?", (item_id,))
                conn.commit()  # Commit para cada exclusão

                # Remover da Treeview
                self.cart_table.delete(item_id)

            conn.close()  # Fechar a conexão com o banco de dados

            messagebox.showinfo("Sucesso", "Itens deletados com sucesso!")





        

    
        


    

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
     # Fecha a janela do calendário

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
                for i, product in enumerate(products):
                    tag = "even" if i % 2 == 0 else "odd"  # Alterna entre as tags "odd" e "even"
                    self.products_table.insert("", "end", values=product, tags=(tag,))
            else:
                messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar produtos: {e}")

   


    
    
    def carregar_dados(self):
        """Carrega os dados do banco de dados para a Tabela do Carrinho."""
        # Conectar ao banco de dados
        conn = sqlite3.connect("carrinho.db")
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM carrinho')
        products = cursor.fetchall()
        conn.close()

        # Limpar dados existentes
        for item in self.cart_table.get_children():
            self.cart_table.delete(item)

        # Inserir novos dados
        if products:
            for i, product in enumerate(products):
                tag = "even" if i % 2 == 0 else "odd"
                
                # Reorganize os dados para corresponder à ordem das colunas
                item_values = (product[0],
                            product[2],  # Nome
                            product[1],  # Código
                            product[3],  # Quantidade
                            product[4])  # Preço

                # Inserir na Treeview, usando product[0] (id) como iid
                self.cart_table.insert("", "end", id=product[0], values=item_values, tags=(tag,))
        else:
            messagebox.showinfo("Resultado", "Nenhum produto encontrado.")
                
        
