import sqlite3

# Função para criar a tabela do banco de dados
def criar_banco():
    """Cria o banco de dados e a tabela 'products', se ainda não existirem."""
    conn = sqlite3.connect('carrinho.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL,
            sale_price REAL NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

# Função para inserir um produto no banco de dados
def inserir_produto(name, code, quantity, sale_price):
    """Insere um produto na tabela 'products'."""
    conn = sqlite3.connect('carrinho.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products (id ,name, code, quantity, sale_price)
            VALUES (?, ?, ?, ?);
        ''', (id, name, code, quantity, sale_price))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Erro: Código '{code}' já existe no banco de dados.")
    finally:
        conn.close()

# Função para obter todos os produtos
def obter_produtos():
    """Retorna todos os produtos da tabela 'products'."""
    conn = sqlite3.connect('carrinho.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products;')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Função para atualizar a quantidade de um produto
def atualizar_quantidade(code, nova_quantidade):
    """Atualiza a quantidade de um produto no banco de dados."""
    conn = sqlite3.connect('carrinho.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE products
        SET quantity = ?
        WHERE code = ?;
    ''', (nova_quantidade, code))
    conn.commit()
    conn.close()

# Função para deletar um produto
def deletar_produto(code):
    """Deleta um produto pelo código."""
    conn = sqlite3.connect('carrinho.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM products
        WHERE code = ?;
    ''', (code,))
    conn.commit()
    conn.close()
