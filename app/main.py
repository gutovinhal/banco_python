import tkinter as tk
from tkinter import ttk, messagebox
from views.clientes_view import ClientesView
from views.produtos_view import ProdutosView
from models.database import Database

class SistemaGestao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão Comercial")
        self.root.state('zoomed')
        
        self.db = Database()
        self.setup_ui()
    
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        
        # Abas do sistema
        self.clientes_view = ClientesView(self.notebook, self.db)
        self.produtos_view = ProdutosView(self.notebook, self.db)
        
        self.notebook.add(self.clientes_view.frame, text="Clientes")
        self.notebook.add(self.produtos_view.frame, text="Produtos")
        
        self.notebook.pack(expand=True, fill='both')