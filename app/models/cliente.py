class Cliente:
    def __init__(self, id=None, nome=None, cpf=None, telefone=None, email=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
    
    def validar(self):
        if not self.nome:
            raise ValueError("Nome do cliente é obrigatório")
        if len(self.nome) < 3:
            raise ValueError("Nome muito curto")