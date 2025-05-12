import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.utils.utils import format_currency

class ContasView:
    def __init__(self, master, db, auth, usuario_atual, tipo_conta):
        self.db = db
        self.usuario_atual = usuario_atual
        self.tipo_conta = tipo_conta  # 'receber' ou 'pagar'
        self.frame = ttk.Frame(master)
        
        self.criar_widgets()
        self.carregar_contas()
    
    def criar_widgets(self):
        """Cria a interface para contas a receber/pagar"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame de formulário
        form_frame = ttk.LabelFrame(main_frame, text=f"Nova Conta a {self.tipo_conta.title()}", padding=10)
        form_frame.pack(fill='x', pady=5)
        
        # Campos do formulário
        campos = [
            ("Descrição:", 0),
            ("Valor R$:", 1),
            ("Data Vencimento (DD/MM/AAAA):", 2),
            ("Status:", 3)
        ]
        
        self.entries = {}
        for label, row in campos:
            ttk.Label(form_frame, text=label).grid(row=row, column=0, sticky='e', padx=5, pady=2)
            if label == "Status:":
                entry = ttk.Combobox(form_frame, values=["Pendente", "Pago", "Cancelado"], state="readonly")
                entry.set("Pendente")
            elif label == "Data Vencimento (DD/MM/AAAA):":
                entry = ttk.Entry(form_frame)
                entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
            else:
                entry = ttk.Entry(form_frame)
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
            self.entries[label.lower().replace(" ", "_").replace(":", "").replace("(", "").replace(")", "")] = entry
        
        # Frame de botões
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_conta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_conta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Remover", command=self.remover_conta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Marcar como Pago", command=self.marcar_como_pago).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.LabelFrame(main_frame, text=f"Contas a {self.tipo_conta.title()}", padding=10)
        tree_frame.pack(fill='both', expand=True, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Descrição', 'Valor', 'Vencimento', 'Status'), show='headings')
        
        colunas = [
            ('ID', 50, 'center'),
            ('Descrição', 250, 'w'),
            ('Valor', 100, 'e'),
            ('Vencimento', 120, 'center'),
            ('Status', 100, 'center')
        ]
        
        for col, width, anchor in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.selecionar_conta)
    
    def carregar_contas(self):
        """Carrega as contas do banco de dados"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            self.db.cursor.execute(f"""
                SELECT id, descricao, valor, data_vencimento, status 
                FROM contas_{self.tipo_conta}
                ORDER BY data_vencimento
            """)
            
            for conta in self.db.cursor.fetchall():
                self.tree.insert('', 'end', values=(
                    conta[0],
                    conta[1],
                    format_currency(conta[2]),
                    conta[3],
                    conta[4]
                ))
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Falha ao carregar contas: {str(e)}")
    
    def selecionar_conta(self, event):
        """Preenche os campos com a conta selecionada"""
        selected = self.tree.focus()
        if selected:
            self.conta_selecionada = self.tree.item(selected)['values']
            self.entries['descrição'].delete(0, 'end')
            self.entries['descrição'].insert(0, self.conta_selecionada[1])
            self.entries['valor_r$'].delete(0, 'end')
            self.entries['valor_r$'].insert(0, self.conta_selecionada[2])
            self.entries['data_vencimento_ddmmaaaa'].delete(0, 'end')
            self.entries['data_vencimento_ddmmaaaa'].insert(0, self.conta_selecionada[3])
            self.entries['status'].set(self.conta_selecionada[4])
    
    def adicionar_conta(self):
        """Adiciona uma nova conta"""
        dados = self.validar_campos()
        if not dados:
            return
        
        try:
            self.db.cursor.execute(
                f"""INSERT INTO contas_{self.tipo_conta} 
                (descricao, valor, data_vencimento, status) 
                VALUES (?, ?, ?, ?)""",
                (dados['descricao'], dados['valor'], dados['data_vencimento'], dados['status'])
            )
            self.db.conn.commit()
            self.carregar_contas()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Conta adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar conta: {str(e)}")
    
    def editar_conta(self):
        """Edita a conta selecionada"""
        if not hasattr(self, 'conta_selecionada'):
            messagebox.showwarning("Aviso", "Selecione uma conta para editar!")
            return
        
        dados = self.validar_campos()
        if not dados:
            return
        
        try:
            self.db.cursor.execute(
                f"""UPDATE contas_{self.tipo_conta} SET 
                descricao=?, valor=?, data_vencimento=?, status=? 
                WHERE id=?""",
                (dados['descricao'], dados['valor'], dados['data_vencimento'], dados['status'], self.conta_selecionada[0])
            )
            self.db.conn.commit()
            self.carregar_contas()
            messagebox.showinfo("Sucesso", "Conta atualizada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao editar conta: {str(e)}")
    
    def marcar_como_pago(self):
        """Marca a conta como paga/recebida"""
        if not hasattr(self, 'conta_selecionada'):
            messagebox.showwarning("Aviso", "Selecione uma conta!")
            return
            
        try:
            self.db.cursor.execute(
                f"UPDATE contas_{self.tipo_conta} SET status='Pago', data_pagamento=date('now') WHERE id=?",
                (self.conta_selecionada[0],)
            )
            self.db.conn.commit()
            self.carregar_contas()
            messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar status: {str(e)}")
    
    def remover_conta(self):
        """Remove a conta selecionada"""
        if not hasattr(self, 'conta_selecionada'):
            messagebox.showwarning("Aviso", "Selecione uma conta para remover!")
            return
        
        if messagebox.askyesno("Confirmar", "Deseja realmente remover esta conta?"):
            try:
                self.db.cursor.execute(
                    f"DELETE FROM contas_{self.tipo_conta} WHERE id=?",
                    (self.conta_selecionada[0],)
                )
                self.db.conn.commit()
                self.carregar_contas()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Conta removida com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao remover conta: {str(e)}")
    
    def validar_campos(self):
        """Valida os campos do formulário"""
        descricao = self.entries['descrição'].get().strip()
        valor_str = self.entries['valor_r$'].get().strip()
        data_str = self.entries['data_vencimento_ddmmaaaa'].get().strip()
        status = self.entries['status'].get()
        
        if not descricao:
            messagebox.showwarning("Aviso", "Descrição é obrigatória!")
            return None
        
        try:
            valor = float(valor_str.replace("R$", "").replace(".", "").replace(",", "."))
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "Valor deve ser um número positivo!")
            return None
        
        try:
            dia, mes, ano = map(int, data_str.split('/'))
            data_vencimento = f"{ano:04d}-{mes:02d}-{dia:02d}"
        except ValueError:
            messagebox.showwarning("Aviso", "Data inválida! Use DD/MM/AAAA")
            return None
        
        return {
            'descricao': descricao,
            'valor': valor,
            'data_vencimento': data_vencimento,
            'status': status
        }
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set('Pendente')
            else:
                entry.delete(0, 'end')
        
        if hasattr(self, 'conta_selecionada'):
            del self.conta_selecionada
        
        # Restaura data padrão
        self.entries['data_vencimento_ddmmaaaa'].insert(0, datetime.now().strftime('%d/%m/%Y'))