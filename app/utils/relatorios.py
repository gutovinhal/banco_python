import sqlite3
from datetime import datetime
from app.utils.utils import get_date_column, format_currency  # Novas importações

def gerar_relatorio_clientes(db):
    try:
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/relatorio_clientes_{data}.txt"
        
        db.cursor.execute("SELECT nome, cpf, email, data_cadastro FROM clientes ORDER BY nome")
        clientes = db.cursor.fetchall()
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE CLIENTES\n")
            f.write("="*50 + "\n\n")
            for cliente in clientes:
                f.write(f"Nome: {cliente[0]}\n")
                f.write(f"CPF: {cliente[1]}\n")
                f.write(f"Email: {cliente[2]}\n")
                f.write(f"Cadastro: {cliente[3]}\n")
                f.write("-"*50 + "\n")
        
        return nome_arquivo
    except Exception as e:
        raise Exception(f"Erro ao gerar relatório: {str(e)}")

def gerar_relatorio_vendas(db):
    try:
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorios/relatorio_vendas_{data}.txt"
        date_column = get_date_column(db.cursor, 'vendas')  # Usando função utilitária
        
        db.cursor.execute(f"""
            SELECT v.id, v.{date_column}, c.nome, v.total 
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.{date_column} DESC
            LIMIT 100
        """)
        
        vendas = db.cursor.fetchall()
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE VENDAS\n")
            f.write("="*50 + "\n\n")
            for venda in vendas:
                f.write(f"ID: {venda[0]}\n")
                f.write(f"Data: {venda[1]}\n")
                f.write(f"Cliente: {venda[2]}\n")
                f.write(f"Total: {format_currency(venda[3])}\n")  # Formatação consistente
                f.write("-"*50 + "\n")
        
        return nome_arquivo
    except Exception as e:
        raise Exception(f"Erro ao gerar relatório: {str(e)}")