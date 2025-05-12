import tkinter as tk
from tkinter import ttk, messagebox
from app.models.database import Database
from app.models.seguranca import Autenticacao
from app.views.login_view import LoginView

class SistemaGestao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão Comercial")
        self.root.geometry("1200x700")
        
        self.db = Database()
        self.auth = Autenticacao(self.db)
        self.usuario_atual = None
        
        self.configurar_estilos()
        self.show_login()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', font=('Segoe UI', 10))
        style.configure('TNotebook.Tab', padding=[10, 5], font=('Segoe UI', 10, 'bold'))

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.login_view = LoginView(self.root, self)
        self.login_view.pack(expand=True)

    def iniciar_sistema(self, usuario):
        self.usuario_atual = usuario
        self.login_view.destroy()
        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        
        from app.views.produtos_view import ProdutosView
        from app.views.clientes_view import ClientesView
        from app.views.vendas_view import VendasView
        from app.views.financeiro_view import FinanceiroView
        
        self.produtos_view = ProdutosView(self.notebook, self.db, self.auth, self.usuario_atual)
        self.clientes_view = ClientesView(self.notebook, self.db, self.auth, self.usuario_atual)
        self.vendas_view = VendasView(self.notebook, self.db, self.auth, self.usuario_atual)
        self.financeiro_view = FinanceiroView(self.notebook, self.db, self.auth, self.usuario_atual)
        
        self.notebook.add(self.produtos_view.frame, text="Produtos")
        self.notebook.add(self.clientes_view.frame, text="Clientes")
        self.notebook.add(self.vendas_view.frame, text="Vendas")
        self.notebook.add(self.financeiro_view.frame, text="Financeiro")
        
        self.notebook.pack(expand=True, fill='both')
        self.setup_menu()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Backup", command=self.executar_backup)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Relatórios
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Clientes", command=self.gerar_relatorio_clientes)
        report_menu.add_command(label="Vendas", command=self.gerar_relatorio_vendas)
        menubar.add_cascade(label="Relatórios", menu=report_menu)
        
        self.root.config(menu=menubar)

    def executar_backup(self):
        from app.utils.backup import realizar_backup
        path = realizar_backup('data/database/gestao.db')
        messagebox.showinfo("Backup", f"Backup criado em: {path}")

    def gerar_relatorio_clientes(self):
        from app.utils.relatorios import gerar_relatorio_clientes
        path = gerar_relatorio_clientes(self.db)
        messagebox.showinfo("Relatório", f"Relatório gerado em: {path}")

    def gerar_relatorio_vendas(self):
        from app.utils.relatorios import gerar_relatorio_vendas
        path = gerar_relatorio_vendas(self.db)
        messagebox.showinfo("Relatório", f"Relatório gerado em: {path}")