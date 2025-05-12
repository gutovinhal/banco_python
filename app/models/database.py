import sqlite3
from pathlib import Path
from hashlib import sha256

class Database:
    def __init__(self, db_name='gestao.db'):
        db_path = Path(__file__).parent.parent.parent / 'data' / 'database' / db_name
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(str(db_path))
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_admin_user()
    
    def create_tables(self):
        tables = [
            """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                nome TEXT NOT NULL,
                nivel_acesso INTEGER DEFAULT 1
            )""",
            """CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE,
                telefone TEXT,
                email TEXT,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
            )""",
            """CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER DEFAULT 0,
                categoria TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                total REAL NOT NULL,
                data TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )""",
            """CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )""",
            """CREATE TABLE IF NOT EXISTS logs_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                acao TEXT NOT NULL,
                data TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )"""
        ]

        for table in tables:
            try:
                self.cursor.execute(table)
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela: {e}")
        
        self.conn.commit()
    
    def create_admin_user(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
        if self.cursor.fetchone()[0] == 0:
            senha_hash = sha256('admin123'.encode()).hexdigest()
            try:
                self.cursor.execute(
                    "INSERT INTO usuarios (username, senha_hash, nome, nivel_acesso) VALUES (?, ?, ?, ?)",
                    ('admin', senha_hash, 'Administrador', 3)
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar usuário admin: {e}")
    
    def close(self):
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()