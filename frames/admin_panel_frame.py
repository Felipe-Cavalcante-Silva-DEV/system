import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class AdminPanelFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título
        self.title_label = ctk.CTkLabel(self, text="Cadastro de Usuários", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Nome do usuário
        self.name_label = ctk.CTkLabel(self, text="Nome:")
        self.name_label.pack(padx=20, pady=5)

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(padx=20, pady=5)

        # Senha
        self.password_label = ctk.CTkLabel(self, text="Senha:")
        self.password_label.pack(padx=20, pady=5)

        self.password_entry = ctk.CTkEntry(self, show="*")  # Mostra senha como asteriscos
        self.password_entry.pack(padx=20, pady=5)

        # CPF
        self.cpf_label = ctk.CTkLabel(self, text="CPF:")
        self.cpf_label.pack(padx=20, pady=5)

        self.cpf_entry = ctk.CTkEntry(self)
        self.cpf_entry.pack(padx=20, pady=5)

        # Cargo/Permissão
        self.role_label = ctk.CTkLabel(self, text="Cargo/Permissão:")
        self.role_label.pack(padx=20, pady=5)

        self.role_entry = ctk.CTkEntry(self)
        self.role_entry.pack(padx=20, pady=5)

        # Botão de Cadastro
        self.add_button = ctk.CTkButton(self, text="Cadastrar Usuário", command=self.add_user)
        self.add_button.pack(pady=20)

        # Botão de pesquisa
        self.search_label = ctk.CTkLabel(self, text="Pesquisar Usuário por Nome ou CPF:", font=("Arial", 12))
        self.search_label.pack(padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(self)
        self.search_entry.pack(padx=20, pady=5)

        self.search_button = ctk.CTkButton(self, text="Pesquisar", command=self.search_user)
        self.search_button.pack(padx=20, pady=10)

        self.users_table = ctk.CTkTextbox(self, width=500, height=200)
        self.users_table.pack(padx=20, pady=20)

        # Cria a tabela de usuários, se não existir
        self.create_users_table()

    def create_users_table(self):
        # Conectar ao banco de dados e criar a tabela se não existir
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                cpf TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_user(self):
        # Obtém os dados inseridos
        name = self.name_entry.get()
        password = self.password_entry.get()
        cpf = self.cpf_entry.get()
        role = self.role_entry.get()

        if not name or not password or not cpf or not role:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            # Conectar ao banco de dados e inserir os dados
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO users (name, password, cpf, role)
                VALUES (?, ?, ?, ?)
            ''', (name, password, cpf, role))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.clear_entries()  # Limpar os campos de entrada após o cadastro
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    def search_user(self):
        search_term = self.search_entry.get()

        if not search_term:
            messagebox.showwarning("Atenção", "Digite um nome ou CPF para pesquisa!")
            return

        try:
            # Conectar ao banco de dados e buscar os dados
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('''
                SELECT * FROM users WHERE name LIKE ? OR cpf LIKE ?
            ''', ('%' + search_term + '%', '%' + search_term + '%'))
            users = c.fetchall()
            conn.close()

            if users:
                # Exibe os dados encontrados
                self.users_table.delete(1.0, ctk.END)  # Limpar a tabela de pesquisa
                for user in users:
                    self.users_table.insert(ctk.END, f"ID: {user[0]} - Nome: {user[1]} - CPF: {user[3]} - Cargo: {user[4]}\n")
            else:
                messagebox.showinfo("Nenhum Resultado", "Nenhum usuário encontrado!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")

    def clear_entries(self):
        # Limpar os campos de entrada
        self.name_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.cpf_entry.delete(0, ctk.END)
        self.role_entry.delete(0, ctk.END)
