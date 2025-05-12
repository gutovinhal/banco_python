import sqlite3
from hashlib import sha256

conn = sqlite3.connect('data/database/gestao.db')
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    nome TEXT NOT NULL,
    nivel_acesso INTEGER DEFAULT 1
)
""")

# Insere o admin (senha: 'password')
senha_hash = sha256('password'.encode()).hexdigest()
cursor.execute(
    "INSERT OR IGNORE INTO usuarios (username, senha_hash, nome, nivel_acesso) VALUES (?, ?, ?, ?)",
    ('admin', senha_hash, 'Administrador', 3)
)

conn.commit()
conn.close()

print("Usuário admin criado com sucesso!")
print("Username: admin")
print("Senha: admin")