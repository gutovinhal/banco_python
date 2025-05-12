import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.utils import get_date_column, format_currency

class ProdutosView:
    def __init__(self, master, db, auth, usuario_atual):
        self.db = db
        self.usuario_atual = usuario_atual
        self.frame = ttk.Frame(master)
        
        self.criar_widgets()
        self.carregar_produtos()
    
    def criar_widgets(self):
        # Frame de formulário
        form_frame = ttk.LabelFrame(self.frame, text="Cadastro de Produtos", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos do formulário
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.nome_entry = ttk.Entry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(form_frame, text="Preço:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.preco_entry = ttk.Entry(form_frame)
        self.preco_entry.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        ttk.Label(form_frame, text="Estoque:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.estoque_spin = ttk.Spinbox(form_frame, from_=0, to=1000)
        self.estoque_spin.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        
        # Botões
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_produto).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Editar", command=self.editar_produto).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Remover", command=self.remover_produto).pack(side='left', padx=2)
        
        # Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Nome', 'Preço', 'Estoque'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Preço', text='Preço')
        self.tree.heading('Estoque', text='Estoque')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nome', width=200)
        self.tree.column('Preço', width=100, anchor='e')
        self.tree.column('Estoque', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_produto)
    
    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.db.cursor.execute("SELECT id, nome, preco, estoque FROM produtos ORDER BY nome")
        for produto in self.db.cursor.fetchall():
            self.tree.insert('', 'end', values=produto)
    
    def selecionar_produto(self, event):
        selected = self.tree.focus()
        if selected:
            self.produto_selecionado = self.tree.item(selected)['values']
            self.nome_entry.delete(0, 'end')
            self.nome_entry.insert(0, self.produto_selecionado[1])
            self.preco_entry.delete(0, 'end')
            self.preco_entry.insert(0, self.produto_selecionado[2])
            self.estoque_spin.delete(0, 'end')
            self.estoque_spin.insert(0, self.produto_selecionado[3])
    
    def adicionar_produto(self):
        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        estoque = self.estoque_spin.get()
        
        try:
            preco = float(preco)
            estoque = int(estoque)
            
            self.db.cursor.execute(
                "INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
                (nome, preco, estoque)
            )
            self.db.conn.commit()
            self.carregar_produtos()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar produto: {str(e)}")
    
    def editar_produto(self):
        if not hasattr(self, 'produto_selecionado'):
            messagebox.showwarning("Aviso", "Selecione um produto para editar!")
            return
        
        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        estoque = self.estoque_spin.get()
        
        try:
            preco = float(preco)
            estoque = int(estoque)
            
            self.db.cursor.execute(
                "UPDATE produtos SET nome=?, preco=?, estoque=? WHERE id=?",
                (nome, preco, estoque, self.produto_selecionado[0])
            )
            self.db.conn.commit()
            self.carregar_produtos()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar produto: {str(e)}")
    
    def remover_produto(self):
        if not hasattr(self, 'produto_selecionado'):
            messagebox.showwarning("Aviso", "Selecione um produto para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente remover este produto?"):
            try:
                self.db.cursor.execute(
                    "DELETE FROM produtos WHERE id=?",
                    (self.produto_selecionado[0],)
                )
                self.db.conn.commit()
                self.carregar_produtos()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao remover produto: {str(e)}")
    
    def limpar_campos(self):
        self.nome_entry.delete(0, 'end')
        self.preco_entry.delete(0, 'end')
        self.estoque_spin.delete(0, 'end')
        self.estoque_spin.insert(0, 0)
        if hasattr(self, 'produto_selecionado'):
            del self.produto_selecionado