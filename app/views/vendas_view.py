import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VendasView:
    def __init__(self, master, db, auth, usuario_atual):
        self.db = db
        self.usuario_atual = usuario_atual
        self.frame = ttk.Frame(master)
        self.itens_venda = []
        
        self.criar_widgets()
        self.carregar_clientes()
        self.carregar_produtos()
        self.carregar_vendas()
    
    def criar_widgets(self):
        # Frame superior
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        # Frame de formulário
        form_frame = ttk.LabelFrame(top_frame, text="Nova Venda", padding=10)
        form_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Cliente
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.cliente_combobox = ttk.Combobox(form_frame, state='readonly')
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=2, sticky='ew')
        
        # Produto
        ttk.Label(form_frame, text="Produto:").grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.produto_combobox = ttk.Combobox(form_frame, state='readonly')
        self.produto_combobox.grid(row=1, column=1, padx=5, pady=2, sticky='ew')
        
        # Quantidade
        ttk.Label(form_frame, text="Quantidade:").grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.quantidade_spin = ttk.Spinbox(form_frame, from_=1, to=100, width=5)
        self.quantidade_spin.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        self.quantidade_spin.set(1)
        
        # Botão Adicionar Item
        ttk.Button(form_frame, text="Adicionar Item", command=self.adicionar_item).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Frame de itens
        itens_frame = ttk.LabelFrame(top_frame, text="Itens da Venda", padding=10)
        itens_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        self.itens_tree = ttk.Treeview(itens_frame, columns=('ID', 'Produto', 'Quantidade', 'Preço', 'Total'), show='headings')
        
        colunas = [
            ('ID', 50, 'center'),
            ('Produto', 150, 'w'),
            ('Quantidade', 80, 'center'),
            ('Preço', 80, 'e'),
            ('Total', 80, 'e')
        ]
        
        for col, width, anchor in colunas:
            self.itens_tree.heading(col, text=col)
            self.itens_tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(itens_frame, orient='vertical', command=self.itens_tree.yview)
        self.itens_tree.configure(yscrollcommand=scrollbar.set)
        
        self.itens_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame inferior
        bottom_frame = ttk.Frame(self.frame)
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        # Total
        ttk.Label(bottom_frame, text="Total:").pack(side='left', padx=5)
        self.total_label = ttk.Label(bottom_frame, text="R$ 0,00", font=('Arial', 10, 'bold'))
        self.total_label.pack(side='left', padx=5)
        
        # Botões
        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text="Finalizar Venda", command=self.finalizar_venda).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Cancelar", command=self.limpar_venda).pack(side='left', padx=2)
        
        # Treeview de vendas
        vendas_frame = ttk.LabelFrame(self.frame, text="Histórico de Vendas", padding=10)
        vendas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.vendas_tree = ttk.Treeview(vendas_frame, columns=('ID', 'Data', 'Cliente', 'Total'), show='headings')
        
        colunas = [
            ('ID', 50, 'center'),
            ('Data', 120, 'center'),
            ('Cliente', 150, 'w'),
            ('Total', 100, 'e')
        ]
        
        for col, width, anchor in colunas:
            self.vendas_tree.heading(col, text=col)
            self.vendas_tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(vendas_frame, orient='vertical', command=self.vendas_tree.yview)
        self.vendas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.vendas_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def carregar_clientes(self):
        self.db.cursor.execute("SELECT id, nome FROM clientes ORDER BY nome")
        clientes = self.db.cursor.fetchall()
        self.clientes = {nome: id for id, nome in clientes}
        self.cliente_combobox['values'] = list(self.clientes.keys())
    
    def carregar_produtos(self):
        self.db.cursor.execute("SELECT id, nome, preco FROM produtos ORDER BY nome")
        produtos = self.db.cursor.fetchall()
        self.produtos = {nome: (id, preco) for id, nome, preco in produtos}
        self.produto_combobox['values'] = list(self.produtos.keys())
    
    def carregar_vendas(self):
        for item in self.vendas_tree.get_children():
            self.vendas_tree.delete(item)
        
        self.db.cursor.execute("""
            SELECT v.id, v.data, c.nome, v.total 
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.data DESC
        """)
        
        for venda in self.db.cursor.fetchall():
            self.vendas_tree.insert('', 'end', values=(
                venda[0],
                venda[1],
                venda[2],
                f"R$ {venda[3]:.2f}".replace(".", ",")
            ))
    
    def adicionar_item(self):
        produto_nome = self.produto_combobox.get()
        quantidade = self.quantidade_spin.get()
        
        if not produto_nome or not quantidade:
            messagebox.showwarning("Aviso", "Selecione um produto e informe a quantidade!")
            return
        
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade deve ser um número positivo!")
            return
        
        produto_id, preco = self.produtos[produto_nome]
        total_item = preco * quantidade
        
        # Adiciona à lista de itens
        self.itens_venda.append({
            'produto_id': produto_id,
            'nome': produto_nome,
            'quantidade': quantidade,
            'preco': preco,
            'total': total_item
        })
        
        # Atualiza a treeview de itens
        self.atualizar_itens()
        
        # Limpa seleção
        self.produto_combobox.set('')
        self.quantidade_spin.delete(0, 'end')
        self.quantidade_spin.insert(0, '1')
    
    def atualizar_itens(self):
        for item in self.itens_tree.get_children():
            self.itens_tree.delete(item)
        
        total_venda = 0
        for item in self.itens_venda:
            self.itens_tree.insert('', 'end', values=(
                item['produto_id'],
                item['nome'],
                item['quantidade'],
                f"R$ {item['preco']:.2f}".replace(".", ","),
                f"R$ {item['total']:.2f}".replace(".", ",")
            ))
            total_venda += item['total']
        
        self.total_label.config(text=f"R$ {total_venda:.2f}".replace(".", ","))
    
    def finalizar_venda(self):
        if not self.itens_venda:
            messagebox.showwarning("Aviso", "Adicione itens à venda!")
            return
        
        cliente_nome = self.cliente_combobox.get()
        if not cliente_nome:
            messagebox.showwarning("Aviso", "Selecione um cliente!")
            return
        
        cliente_id = self.clientes[cliente_nome]
        total_venda = sum(item['total'] for item in self.itens_venda)
        
        try:
            with self.db.conn:
                # Insere a venda
                self.db.cursor.execute(
                    "INSERT INTO vendas (cliente_id, usuario_id, total, data) VALUES (?, ?, ?, datetime('now'))",
                    (cliente_id, self.usuario_atual['id'], total_venda)
                )
                venda_id = self.db.cursor.lastrowid
                
                # Insere os itens da venda
                for item in self.itens_venda:
                    self.db.cursor.execute(
                        "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                        (venda_id, item['produto_id'], item['quantidade'], item['preco'])
                    )
                    
                    # Atualiza o estoque
                    self.db.cursor.execute(
                        "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                        (item['quantidade'], item['produto_id'])
                    )
                
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
                self.limpar_venda()
                self.carregar_vendas()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar venda: {str(e)}")
    
    def limpar_venda(self):
        self.itens_venda = []
        self.atualizar_itens()
        self.cliente_combobox.set('')
        self.produto_combobox.set('')
        self.quantidade_spin.delete(0, 'end')
        self.quantidade_spin.insert(0, '1')
        