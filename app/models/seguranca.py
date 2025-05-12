from hashlib import sha256

class Autenticacao:
    def __init__(self, db):
        self.db = db
    
    def autenticar(self, username, senha):
        senha_hash = sha256(senha.encode()).hexdigest()
        self.db.cursor.execute(
            "SELECT id, username, nome, nivel_acesso FROM usuarios WHERE username = ? AND senha_hash = ?",
            (username, senha_hash)
        )
        return self.db.cursor.fetchone()