import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3
from app.utils.utils import get_date_column, format_currency

class FinanceiroView:
    def __init__(self, master, db, auth, usuario_atual):
        self.db = db
        self.usuario_atual = usuario_atual
        self.frame = ttk.Frame(master)
        self.date_column = get_date_column(db.cursor, 'vendas')
        
        self.criar_widgets()
        self.carregar_dados()
    
    def criar_widgets(self):
        # Frame de filtros
        filter_frame = ttk.LabelFrame(self.frame, text="Filtros", padding=10)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        # Período
        ttk.Label(filter_frame, text="Período:").grid(row=0, column=0, padx=5, pady=2)
        
        self.periodo_var = tk.StringVar(value="7")
        ttk.Radiobutton(filter_frame, text="7 dias", variable=self.periodo_var, value="7", command=self.carregar_dados).grid(row=0, column=1, padx=5, pady=2)
        ttk.Radiobutton(filter_frame, text="30 dias", variable=self.periodo_var, value="30", command=self.carregar_dados).grid(row=0, column=2, padx=5, pady=2)
        ttk.Radiobutton(filter_frame, text="90 dias", variable=self.periodo_var, value="90", command=self.carregar_dados).grid(row=0, column=3, padx=5, pady=2)
        ttk.Radiobutton(filter_frame, text="Personalizado", variable=self.periodo_var, value="custom", command=self.habilitar_custom).grid(row=0, column=4, padx=5, pady=2)
        
        # Datas personalizadas
        self.custom_frame = ttk.Frame(filter_frame)
        self.custom_frame.grid(row=1, column=0, columnspan=5, pady=5)
        
        ttk.Label(self.custom_frame, text="De:").pack(side='left', padx=5)
        self.data_inicio = ttk.Entry(self.custom_frame, width=10)
        self.data_inicio.pack(side='left', padx=5)
        
        ttk.Label(self.custom_frame, text="Até:").pack(side='left', padx=5)
        self.data_fim = ttk.Entry(self.custom_frame, width=10)
        self.data_fim.pack(side='left', padx=5)
        
        ttk.Button(self.custom_frame, text="Aplicar", command=self.carregar_dados).pack(side='left', padx=5)
        
        # Desabilitar inicialmente
        for widget in self.custom_frame.winfo_children():
            widget.configure(state='disabled')
        
        # Resumo financeiro
        resumo_frame = ttk.LabelFrame(self.frame, text="Resumo Financeiro", padding=10)
        resumo_frame.pack(fill='x', padx=10, pady=5)
        
        metricas = [
            ("Total de Vendas:", "total_vendas"),
            ("Média Diária:", "media_diaria"),
            ("Produto Mais Vendido:", "produto_mais_vendido"),
            ("Cliente Mais Frequente:", "cliente_mais_frequente")
        ]
        
        self.metricas_labels = {}
        for i, (label, key) in enumerate(metricas):
            ttk.Label(resumo_frame, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=2)
            self.metricas_labels[key] = ttk.Label(resumo_frame, text="", font=('Arial', 10))
            self.metricas_labels[key].grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        # Detalhes das vendas
        vendas_frame = ttk.LabelFrame(self.frame, text="Detalhes das Vendas", padding=10)
        vendas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.vendas_tree = ttk.Treeview(vendas_frame, columns=('ID', 'Data', 'Cliente', 'Total'), show='headings')
        
        colunas = [
            ('ID', 50, 'center'),
            ('Data', 100, 'center'),
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
    
    def habilitar_custom(self):
        for widget in self.custom_frame.winfo_children():
            widget.configure(state='normal')
        
        hoje = datetime.now().strftime('%Y-%m-%d')
        self.data_inicio.delete(0, 'end')
        self.data_inicio.insert(0, hoje)
        self.data_fim.delete(0, 'end')
        self.data_fim.insert(0, hoje)
    
    def carregar_dados(self):
        periodo = self.periodo_var.get()
        
        try:
            if periodo == "custom":
                data_inicio = self.data_inicio.get()
                data_fim = self.data_fim.get()
                
                datetime.strptime(data_inicio, '%Y-%m-%d')
                datetime.strptime(data_fim, '%Y-%m-%d')
                
                where_clause = f"WHERE date(v.{self.date_column}) BETWEEN '{data_inicio}' AND '{data_fim}'"
            else:
                dias = int(periodo)
                where_clause = f"WHERE date(v.{self.date_column}) >= date('now', '-{dias} days')"
            
            # Carrega vendas
            for item in self.vendas_tree.get_children():
                self.vendas_tree.delete(item)
            
            query = f"""
                SELECT v.id, v.{self.date_column}, c.nome, v.total 
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                {where_clause}
                ORDER BY v.{self.date_column} DESC
            """
            
            self.db.cursor.execute(query)
            total_vendas = 0
            for venda in self.db.cursor.fetchall():
                self.vendas_tree.insert('', 'end', values=(
                    venda[0],
                    venda[1],
                    venda[2],
                    format_currency(venda[3])
                ))
                total_vendas += venda[3]
            
            # Atualiza métricas
            self.metricas_labels['total_vendas'].config(text=format_currency(total_vendas))
            
            if periodo != "custom":
                dias = int(periodo)
                media = total_vendas / dias if dias > 0 else 0
                self.metricas_labels['media_diaria'].config(text=format_currency(media))
            
            # Produto mais vendido
            query = f"""
                SELECT p.nome, SUM(iv.quantidade) as total
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                JOIN vendas v ON iv.venda_id = v.id
                {where_clause}
                GROUP BY p.nome
                ORDER BY total DESC
                LIMIT 1
            """
            
            self.db.cursor.execute(query)
            result = self.db.cursor.fetchone()
            produto = result[0] + f" ({result[1]} un)" if result else "N/A"
            self.metricas_labels['produto_mais_vendido'].config(text=produto)
            
            # Cliente mais frequente
            query = f"""
                SELECT c.nome, COUNT(*) as total
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                {where_clause}
                GROUP BY c.nome
                ORDER BY total DESC
                LIMIT 1
            """
            
            self.db.cursor.execute(query)
            result = self.db.cursor.fetchone()
            cliente = f"{result[0]} ({result[1]} compras)" if result else "N/A"
            self.metricas_labels['cliente_mais_frequente'].config(text=cliente)
            
        except ValueError as e:
            messagebox.showwarning("Aviso", f"Data inválida: {str(e)}")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")