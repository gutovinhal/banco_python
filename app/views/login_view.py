import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        
        self.config(bg='#f0f0f0')
        self.pack(expand=True)
        
        self.criar_widgets()
    
    def criar_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Sistema de Gestão", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Usuário:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_usuario = ttk.Entry(frame, width=25)
        self.entry_usuario.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_senha = ttk.Entry(frame, show="*", width=25)
        self.entry_senha.grid(row=2, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Entrar", command=self.efetuar_login, width=10).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Sair", command=self.master.quit, width=10).pack(side='left', padx=10)
        
        self.entry_usuario.focus()
    
    def efetuar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not usuario or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        usuario_autenticado = self.sistema.auth.autenticar(usuario, senha)
        
        if usuario_autenticado:
            self.sistema.iniciar_sistema({
                'id': usuario_autenticado[0],
                'username': usuario_autenticado[1],
                'nome': usuario_autenticado[2],
                'nivel_acesso': usuario_autenticado[3]
            })
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")
            self.entry_senha.delete(0, 'end')
            self.entry_senha.focus()