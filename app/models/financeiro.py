class ContaReceber:
    def __init__(self, id=None, cliente_id=None, descricao=None, valor=None, 
                 data_vencimento=None, data_recebimento=None, status='PENDENTE'):
        self.id = id
        self.cliente_id = cliente_id
        self.descricao = descricao
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.data_recebimento = data_recebimento
        self.status = status
    
    def validar(self):
        if not self.descricao or not self.valor or not self.data_vencimento:
            raise ValueError("Descrição, valor e vencimento são obrigatórios")

class ContaPagar:
    # Implementação similar para contas a pagar
    pass