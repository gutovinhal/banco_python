import sqlite3
from datetime import datetime

def gerar_relatorio_clientes(db):
    try:
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/relatorio_clientes_{data}.txt"
        
        db.cursor.execute("SELECT nome, cpf, email FROM clientes ORDER BY nome")
        clientes = db.cursor.fetchall()
        
        with open(nome_arquivo, 'w') as f:
            f.write("Relatório de Clientes\n")
            f.write("="*30 + "\n")
            for cliente in clientes:
                f.write(f"Nome: {cliente[0]}\nCPF: {cliente[1]}\nEmail: {cliente[2]}\n")
                f.write("-"*30 + "\n")
        
        return nome_arquivo
    except Exception as e:
        raise Exception(f"Erro ao gerar relatório: {str(e)}")

def gerar_relatorio_vendas(db):
    try:
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/relatorio_vendas_{data}.txt"
        
        # Implemente a lógica para vendas quando tiver a tabela
        with open(nome_arquivo, 'w') as f:
            f.write("Relatório de Vendas\n")
            f.write("="*30 + "\n")
            f.write("Funcionalidade a ser implementada\n")
        
        return nome_arquivo
    except Exception as e:
        raise Exception(f"Erro ao gerar relatório: {str(e)}")