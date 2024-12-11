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
    
criar_banco()




    
    
    