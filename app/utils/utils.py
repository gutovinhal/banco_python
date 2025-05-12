import sqlite3
from datetime import datetime

def get_date_column(cursor, table_name):
    """Obtém o nome da coluna de data de uma tabela"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    
    # Ordem de prioridade para procurar coluna de data
    date_columns = ['data', 'data_venda', 'data_cadastro', 'created_at']
    for col in date_columns:
        if col in columns:
            return col
    
    # Fallback: procura por qualquer coluna com 'data' no nome
    date_cols = [col for col in columns if 'data' in col.lower()]
    return date_cols[0] if date_cols else columns[0] if columns else 'id'

def format_currency(value):
    """Formata valores monetários no padrão brasileiro"""
    if value is None:
        return "R$ 0,00"
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def validate_price(price_str):
    """Valida se uma string pode ser convertida em preço válido"""
    try:
        price = float(price_str)
        return price >= 0
    except ValueError:
        return False

def parse_date(data_str, formato_origem='%d/%m/%Y', formato_destino='%Y-%m-%d'):
    """Converte datas entre formatos"""
    try:
        data_obj = datetime.strptime(data_str, formato_origem)
        return data_obj.strftime(formato_destino)
    except ValueError:
        raise ValueError("Formato de data inválido. Use DD/MM/AAAA")

def validate_date(date_str, date_format='%d/%m/%Y'):
    """Valida se uma string é uma data válida"""
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False