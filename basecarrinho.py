import sqlite3

# Função para criar a tabela do banco de dados
def criar_banco():
    """Cria o banco de dados e a tabela 'carrinho', se ainda não existirem."""
    with sqlite3.connect('carrinho.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL DEFAULT 1,
                sale_price REAL NOT NULL
            );
        ''')

    conn.commit()
    conn.close()



def criar_banco():
    """Cria o banco de dados e a tabela 'carrinho', se ainda não existirem."""
    with sqlite3.connect('carrinho.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrinho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL DEFAULT 1,
                sale_price REAL NOT NULL
            );
        ''')
    conn.commit()
    conn.close()
    
    
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
        criar_banco()

        for item in selected_items:
            # Obter os dados do produto selecionado
            item_values = self.products_table.item(item, "values")
            id = item_values[0]
            nome = item_values[2]       # Nome do produto
            codigo = item_values[1]     # Código do produto
            quantidade = item_values[3] # Quantidade disponível
            preco = item_values[4]      # Preço do produto

            # Inserir os dados na tabela do carrinho
            try:
                cursor.execute('''
                    INSERT INTO carrinho (id, code, name, quantity, sale_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (id, codigo, nome, quantidade, preco))

                conn.commit()  # Confirmar a inserção no banco de dados

                # Opcional: mensagem de confirmação
                print(f'Produto "{nome}" adicionado ao carrinho.')
            
            except sqlite3.IntegrityError:
                # Caso já exista o produto (unique constraint no código)
                print(f'O produto "{nome}" já está no carrinho.')

        conn.close()  # Fechar a conexão com o banco

