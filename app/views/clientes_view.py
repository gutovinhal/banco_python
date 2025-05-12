import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ClientesView:
    def __init__(self, master, db, auth, usuario_atual):
        self.db = db
        self.usuario_atual = usuario_atual
        self.frame = ttk.Frame(master)
        
        self.criar_widgets()
        self.carregar_clientes()
    
    def criar_widgets(self):
        # Frame de formulário
        form_frame = ttk.LabelFrame(self.frame, text="Cadastro de Clientes", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos do formulário
        campos = [
            ("Nome:", 0),
            ("CPF:", 1),
            ("Telefone:", 2),
            ("Email:", 3)
        ]
        
        self.entries = {}
        for label, row in campos:
            ttk.Label(form_frame, text=label).grid(row=row, column=0, sticky='e', padx=5, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
            self.entries[label.lower().replace(":", "")] = entry
        
        # Botões
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_cliente).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Editar", command=self.editar_cliente).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remover", command=self.remover_cliente).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos).pack(side='left', padx=2)
        
        # Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Nome', 'CPF', 'Telefone', 'Email', 'Cadastro'), show='headings')
        
        colunas = [
            ('ID', 50, 'center'),
            ('Nome', 150, 'w'),
            ('CPF', 100, 'center'),
            ('Telefone', 100, 'center'),
            ('Email', 150, 'w'),
            ('Cadastro', 100, 'center')
        ]
        
        for col, width, anchor in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_cliente)
    
    def carregar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.db.cursor.execute("SELECT id, nome, cpf, telefone, email, data_cadastro FROM clientes ORDER BY nome")
        for cliente in self.db.cursor.fetchall():
            self.tree.insert('', 'end', values=cliente)
    
    def selecionar_cliente(self, event):
        selected = self.tree.focus()
        if selected:
            self.cliente_selecionado = self.tree.item(selected)['values']
            self.entries['nome'].delete(0, 'end')
            self.entries['nome'].insert(0, self.cliente_selecionado[1])
            self.entries['cpf'].delete(0, 'end')
            self.entries['cpf'].insert(0, self.cliente_selecionado[2])
            self.entries['telefone'].delete(0, 'end')
            self.entries['telefone'].insert(0, self.cliente_selecionado[3])
            self.entries['email'].delete(0, 'end')
            self.entries['email'].insert(0, self.cliente_selecionado[4])
    
    def adicionar_cliente(self):
        dados = {
            'nome': self.entries['nome'].get(),
            'cpf': self.entries['cpf'].get(),
            'telefone': self.entries['telefone'].get(),
            'email': self.entries['email'].get()
        }
        
        if not dados['nome']:
            messagebox.showwarning("Aviso", "O nome do cliente é obrigatório!")
            return
        
        try:
            self.db.cursor.execute(
                "INSERT INTO clientes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
                (dados['nome'], dados['cpf'], dados['telefone'], dados['email'])
            )
            self.db.conn.commit()
            self.carregar_clientes()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar cliente: {str(e)}")
    
    def editar_cliente(self):
        if not hasattr(self, 'cliente_selecionado'):
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return
        
        dados = {
            'nome': self.entries['nome'].get(),
            'cpf': self.entries['cpf'].get(),
            'telefone': self.entries['telefone'].get(),
            'email': self.entries['email'].get(),
            'id': self.cliente_selecionado[0]
        }
        
        try:
            self.db.cursor.execute(
                "UPDATE clientes SET nome=?, cpf=?, telefone=?, email=? WHERE id=?",
                (dados['nome'], dados['cpf'], dados['telefone'], dados['email'], dados['id'])
            )
            self.db.conn.commit()
            self.carregar_clientes()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar cliente: {str(e)}")
    
    def remover_cliente(self):
        if not hasattr(self, 'cliente_selecionado'):
            messagebox.showwarning("Aviso", "Selecione um cliente para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este cliente?"):
            try:
                self.db.cursor.execute(
                    "DELETE FROM clientes WHERE id=?",
                    (self.cliente_selecionado[0],)
                )
                self.db.conn.commit()
                self.carregar_clientes()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao remover cliente: {str(e)}")
    
    def limpar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        if hasattr(self, 'cliente_selecionado'):
            del self.cliente_selecionado