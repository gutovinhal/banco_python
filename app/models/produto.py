class Produto:
    def __init__(self, id=None, nome=None, preco=None, estoque=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
    
    def validar(self):
        if not self.nome:
            raise ValueError("Nome do produto é obrigatório")
        if self.preco is None or self.preco <= 0:
            raise ValueError("Preço inválido")