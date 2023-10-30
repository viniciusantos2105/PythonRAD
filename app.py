import tkinter as tk
from tkinter import messagebox

class Pessoa:
    def __init__(self, nome, username, senha):
        self.nome = nome
        self.username = username
        self.senha = senha

class CrudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD App")

        self.pessoas = []
        self.logged_in = False
        self.current_user = None

        self.login_frame = tk.Frame(root)
        self.login_frame.grid(row=0, column=0)
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        tk.Label(self.login_frame, text="Senha:").grid(row=1, column=0)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.grid(row=0, column=1)
        self.login_senha_entry = tk.Entry(self.login_frame, show="*")
        self.login_senha_entry.grid(row=1, column=1)
        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=1)

        self.create_frame = tk.Frame(root)
        self.create_frame.grid(row=1, column=0)
        tk.Label(self.create_frame, text="Nome:").grid(row=0, column=0)
        tk.Label(self.create_frame, text="Username:").grid(row=1, column=0)
        tk.Label(self.create_frame, text="Senha:").grid(row=2, column=0)
        self.create_nome_entry = tk.Entry(self.create_frame)
        self.create_nome_entry.grid(row=0, column=1)
        self.create_username_entry = tk.Entry(self.create_frame)
        self.create_username_entry.grid(row=1, column=1)
        self.create_senha_entry = tk.Entry(self.create_frame, show="*")
        self.create_senha_entry.grid(row=2, column=1)
        create_button = tk.Button(self.create_frame, text="Criar Pessoa", command=self.criar_pessoa)
        create_button.grid(row=3, column=1)

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=2, rowspan=4)
        self.output_text = tk.Text(self.main_frame, height=10, width=30)
        self.output_text.grid(row=0, column=0)

        self.view_button = tk.Button(self.main_frame, text="Visualizar Pessoas", command=self.visualizar_pessoas)
        self.view_button.grid(row=2, column=0)
        self.edit_frame = tk.Button(self.main_frame, text="Editar Username", command=self.editar_username)
        self.edit_frame.grid(row=0, column=1)
        self.delete_frame = tk.Button(self.main_frame, text="Excluir Pessoa", command=self.excluir_pessoa)
        self.delete_frame.grid(row=0, column=2)

    def login(self):
        username = self.login_username_entry.get()
        senha = self.login_senha_entry.get()
        for pessoa in self.pessoas:
            if pessoa.username == username and pessoa.senha == senha:
                self.logged_in = True
                self.current_user = pessoa
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Login bem-sucedido.")
                return
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Credenciais inválidas. Tente novamente.")

    def criar_pessoa(self):
        nome = self.create_nome_entry.get()
        username = self.create_username_entry.get()
        senha = self.create_senha_entry.get()
        pessoa = Pessoa(nome, username, senha)
        self.pessoas.append(pessoa)
        self.create_nome_entry.delete(0, tk.END)
        self.create_username_entry.delete(0, tk.END)
        self.create_senha_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Pessoa criada com sucesso.")

    def visualizar_pessoas(self):
        if self.logged_in:
            self.output_text.delete(1.0, tk.END)
            pessoas_info = "Pessoas:\n"
            for pessoa in self.pessoas:
                pessoas_info += f"Nome: {pessoa.nome}, Username: {pessoa.username}\n"
            self.output_text.insert(tk.END, pessoas_info)
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Você precisa fazer login para visualizar pessoas.")

    def editar_username(self):
        if self.logged_in:
            self.edit_username_window = tk.Toplevel(self.root)
            tk.Label(self.edit_username_window, text="Novo Username:").pack()
            self.new_username_entry = tk.Entry(self.edit_username_window)
            self.new_username_entry.pack()
            edit_button = tk.Button(self.edit_username_window, text="Editar", command=self.perform_username_edit)
            edit_button.pack()
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Você precisa fazer login para editar um username.")

    def perform_username_edit(self):
        new_username = self.new_username_entry.get()
        self.current_user.username = new_username
        self.edit_username_window.destroy()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Username editado com sucesso.")

    def excluir_pessoa(self):
        if self.logged_in:
            self.delete_window = tk.Toplevel(self.root)
            tk.Label(self.delete_window, text="Username da Pessoa a ser Excluída:").pack()
            self.username_to_delete_entry = tk.Entry(self.delete_window)
            self.username_to_delete_entry.pack()
            delete_button = tk.Button(self.delete_window, text="Excluir", command=self.perform_excluir_pessoa)
            delete_button.pack()
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Você precisa fazer login para excluir uma pessoa.")

    def perform_excluir_pessoa(self):
        username = self.username_to_delete_entry.get()
        for pessoa in self.pessoas:
            if pessoa.username == username:
                self.pessoas.remove(pessoa)
                self.logged_in = False
                self.current_user = None
                self.delete_window.destroy()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Pessoa excluída com sucesso.")
                return
        self.delete_window.destroy()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Pessoa não encontrada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudApp(root)
    root.mainloop()
