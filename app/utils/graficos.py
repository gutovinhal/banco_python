import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime, timedelta
from app.utils.utils import get_date_column, format_currency  # Nova importação

def gerar_grafico_vendas_por_mes(db, frame):
    date_column = get_date_column(db.cursor, 'vendas')  # Usando a função utilitária
    
    data_inicio = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    db.cursor.execute(f"""
        SELECT strftime('%Y-%m', {date_column}) as mes, 
               SUM(total) as total
        FROM vendas
        WHERE {date_column} >= ?
        GROUP BY mes
        ORDER BY mes
    """, (data_inicio,))
    
    dados = db.cursor.fetchall()
    meses = [d[0] for d in dados]
    valores = [float(d[1]) for d in dados]  # Garantindo que é float
    
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(meses, valores, color='skyblue')
    
    # Adicionando valores formatados nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                format_currency(height),  # Usando formatação consistente
                ha='center', va='bottom')
    
    ax.set_title('Vendas por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Total (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return canvas