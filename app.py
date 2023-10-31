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

        self.cadastro_frame = tk.Frame(root)
        self.cadastro_frame.grid(row=0, column=0)
        tk.Label(self.cadastro_frame, text="Nome:").grid(row=0, column=0)
        tk.Label(self.cadastro_frame, text="Username:").grid(row=1, column=0)
        tk.Label(self.cadastro_frame, text="Senha:").grid(row=2, column=0)
        self.cadastro_nome_entry = tk.Entry(self.cadastro_frame)
        self.cadastro_nome_entry.grid(row=0, column=1)
        self.cadastro_username_entry = tk.Entry(self.cadastro_frame)
        self.cadastro_username_entry.grid(row=1, column=1)
        self.cadastro_senha_entry = tk.Entry(self.cadastro_frame, show="*")
        self.cadastro_senha_entry.grid(row=2, column=1)
        cadastro_button = tk.Button(self.cadastro_frame, text="Cadastrar Pessoa", command=self.cadastrar_pessoa)
        cadastro_button.grid(row=3, column=1)

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

        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=1, rowspan=4)
        self.output_text = tk.Text(self.main_frame, height=10, width=40)
        self.output_text.grid(row=0, column=0)

        self.edit_button = tk.Button(self.main_frame, text="Editar Username", command=self.editar_username)
        self.edit_button.grid(row=0, column=1)
        self.listar_button = tk.Button(self.main_frame, text="Listar Pessoas", command=self.listar_pessoas)
        self.listar_button.grid(row=0, column=3)
        self.excluir_button = tk.Button(self.main_frame, text="Excluir Pessoa", command=self.excluir_pessoa)
        self.excluir_button.grid(row=1, column=1)
        self.cadastrar_usuario_button = tk.Button(self.main_frame, text="Cadastrar Usuário", command=self.show_cadastro_frame)
        self.cadastrar_usuario_button.grid(row=1, column=3)

        self.show_cadastro_frame()

    def show_cadastro_frame(self):
        self.login_frame.grid_forget()
        self.main_frame.grid_forget()
        self.cadastro_frame.grid(row=0, column=0)

    def show_login_frame(self):
        self.cadastro_frame.grid_forget()
        self.main_frame.grid_forget()
        self.login_frame.grid(row=0, column=0)

    def show_main_frame(self):
        self.cadastro_frame.grid_forget()
        self.login_frame.grid_forget()
        self.main_frame.grid(row=0, column=1)

    def cadastrar_pessoa(self):
        nome = self.cadastro_nome_entry.get()
        username = self.cadastro_username_entry.get()
        senha = self.cadastro_senha_entry.get()
        pessoa = Pessoa(nome, username, senha)
        self.pessoas.append(pessoa)
        self.cadastro_nome_entry.delete(0, tk.END)
        self.cadastro_username_entry.delete(0, tk.END)
        self.cadastro_senha_entry.delete(0, tk.END)
        self.show_login_frame()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Pessoa cadastrada com sucesso.")

    def login(self):
        username = self.login_username_entry.get()
        senha = self.login_senha_entry.get()
        for pessoa in self.pessoas:
            if pessoa.username == username and pessoa.senha == senha:
                self.logged_in = True
                self.current_user = pessoa
                self.show_main_frame()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Login bem-sucedido.")
                return
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Credenciais inválidas. Tente novamente.")

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

    def listar_pessoas(self):
        if self.logged_in:
            self.output_text.delete(1.0, tk.END)
            pessoas_info = "Pessoas:\n"
            for pessoa in self.pessoas:
                pessoas_info += f"Nome: {pessoa.nome}, Username: {pessoa.username}\n"
            self.output_text.insert(tk.END, pessoas_info)
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Você precisa fazer login para listar pessoas.")

    def excluir_pessoa(self):
        if self.logged_in:
            self.excluir_window = tk.Toplevel(self.root)
            tk.Label(self.excluir_window, text="Username da Pessoa a ser Excluída:").pack()
            self.username_to_delete_entry = tk.Entry(self.excluir_window)
            self.username_to_delete_entry.pack()
            delete_button = tk.Button(self.excluir_window, text="Excluir", command=self.perform_excluir_pessoa)
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
                self.excluir_window.destroy()
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Pessoa excluída com sucesso.")
                return
        self.excluir_window.destroy()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Pessoa não encontrada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudApp(root)
    root.mainloop()
