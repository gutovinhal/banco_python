import tkinter as tk
from tkinter import ttk, messagebox

class ClientesView:
    def __init__(self, notebook, db):
        self.db = db
        self.frame = ttk.Frame(notebook)
        self.setup_ui()
        self.carregar_clientes()
    
    def setup_ui(self):
        # Frame de formulário
        form_frame = ttk.LabelFrame(self.frame, text="Dados do Cliente", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos
        tk.Label(form_frame, text="Nome*:").grid(row=0, column=0, sticky=tk.W)
        self.nome_entry = tk.Entry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)
        
        # Botões
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame, text="Adicionar", command=self.adicionar_cliente).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "CPF", "Telefone"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def carregar_clientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        self.db.cursor.execute("SELECT id, nome, cpf, telefone FROM clientes")
        for cliente in self.db.cursor.fetchall():
            self.tree.insert("", tk.END, values=cliente)
    
    def adicionar_cliente(self):
        nome = self.nome_entry.get()
        try:
            self.db.cursor.execute(
                "INSERT INTO clientes (nome, data_cadastro) VALUES (?, datetime('now'))",
                (nome,))
            self.db.conn.commit()
            self.carregar_clientes()
            self.nome_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Cliente adicionado!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))