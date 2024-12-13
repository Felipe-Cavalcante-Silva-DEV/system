import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from basevendas import save_sale
import datetime
from widgets.tabelavendas import create_sales_table
from widgets.tabelaprodutos import create_products_table


def get_all_rows_as_strings():
    try:
        conn = sqlite3.connect("sales.db")  # Conecta ao banco de dados
        cursor = conn.cursor()
        query = "SELECT id, vendedor, cliente, total, data FROM vendas"  # Seleciona todas as colunas
        cursor.execute(query)
        
        rows = cursor.fetchall()  # Obtém todas as linhas do resultado
        result_strings = []
        
        for row in rows:
            # Converte todos os valores para string e combina em uma única string
            row_string = "  |  ".join(str(value) for value in row)
            result_strings.append(row_string)
        
        return result_strings
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return []
    finally:
        conn.close()  # Fecha a conexão




from tkinter import ttk

def get_items_for_sale(venda_id):
    try:
        conn = sqlite3.connect("sales.db")  # Conecta ao banco de dados
        cursor = conn.cursor()
        
        # Consulta para obter os itens relacionados à venda
        query = '''
            SELECT id, venda_id, code, nome, quantidade, preco_unitario, total
            FROM itens_venda
            WHERE venda_id = ?
        '''
        cursor.execute(query, (venda_id,))
        items = cursor.fetchall()
        
        return items  # Retorna os itens como uma lista de tuplas
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return []
    finally:
        conn.close()  # Fecha a conexão


class ExpensesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid para o frame principal
        # As colunas 0 (esquerda) e 2 (direita) têm o mesmo peso
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Lado esquerdo
        self.grid_columnconfigure(1, weight=0)  # Divisor
        self.grid_columnconfigure(2, weight=1)  # Lado direito

        # Divisor (linha vertical) no meio
        self.divider = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.divider.grid(row=0, column=1, sticky="ns")

        # Lado esquerdo (formulário de cadastro)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configuração do grid dentro do left_frame
        self.left_frame.grid_rowconfigure(0, weight=1)  # Parte superior
        self.left_frame.grid_rowconfigure(1, weight=1)  # Parte inferior
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Frames internos do lado esquerdo
        self.left_frame_up = ctk.CTkFrame(self.left_frame)  # Agora é filho de left_frame
        self.left_frame_up.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.left_frame_down = ctk.CTkFrame(self.left_frame)  # Agora é filho de left_frame
        self.left_frame_down.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Lado direito (exibição de produtos)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Configuração do grid dentro do right_frame (se necessário)
        self.right_frame.grid_rowconfigure(0, weight=1)  # Ajuste para o conteúdo
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Título
        self.title_home = ctk.CTkLabel(self.left_frame_up, text="Expenses", font=("Arial Bold", 36))
        self.title_home.pack(pady=10)

        # Dropdown para IDs de vendas
        self.sales_option = ctk.StringVar(value="Select a sale")
        self.row_strings = get_all_rows_as_strings()

        
        #         # Limite de caracteres para cada item no menu
        # max_chars = 100

        # # Crie uma lista de valores com texto limitado
        # limited_values = [item[:max_chars] for item in self.row_strings]

        # if self.row_strings:

        #     self.vendasid_button = ctk.CTkOptionMenu(self.left_frame_up,
        #         values=limited_values,  # Use os valores limitados
        #         variable=self.sales_option,
        #         font=("Arial", 16),
        #         command=self.display_sale_items,
        #         width=520,  # Largura fixa
        #         height=30   # Altura fixa
        #     )

        # # Agora, posicione o botão com place() sem passar width/height
        # self.vendasid_button.place(x=25, y=125)


        self.importar_button = ctk.CTkButton(self.left_frame_up, text="Importar")
        self.importar_button.place(x=660, y=125)

        # Tabela de vendas (Treeview)
        self.sales_table = create_sales_table(self.left_frame_up)
        self.sales_table.place(x=20, y=170, width=780, height=220)









        self.products_table = create_products_table(self.left_frame_down)
        self.products_table.place(x=20, y=270, width=780, height=260)



    def display_sale_items(self, selected_sale):
        # Extrai o ID da venda do string selecionado
        venda_id = selected_sale.split("  |  ")[0]
        if venda_id.isdigit():
            items = get_items_for_sale(int(venda_id))
            self.update_sales_table(items)
        else:
            # Limpa a tabela se a seleção for inválida
            self.update_sales_table([])
            

    def update_sales_table(self, items):
        """Atualiza a Treeview com os itens fornecidos."""
        # Limpa a Treeview
        for item in self.sales_table.get_children():
            self.sales_table.delete(item)

        # Adiciona os novos itens
        for i, item in enumerate(items):
            tag = "even" if i % 2 == 0 else "odd"  # Alterna as cores das linhas
            self.sales_table.insert("", "end", values=item, tags=(tag,))
