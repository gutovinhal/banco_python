import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime, timedelta

def gerar_grafico_vendas_por_mes(db, frame):
    # Consulta para obter vendas dos últimos 6 meses
    data_inicio = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    db.cursor.execute("""
        SELECT strftime('%Y-%m', data_venda) as mes, 
               SUM(total) as total
        FROM vendas
        WHERE data_venda >= ?
        GROUP BY mes
        ORDER BY mes
    """, (data_inicio,))
    
    dados = db.cursor.fetchall()
    meses = [d[0] for d in dados]
    valores = [d[1] for d in dados]
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(meses, valores, color='skyblue')
    ax.set_title('Vendas por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Total (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Embed no Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    return canvas