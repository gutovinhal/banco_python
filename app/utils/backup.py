import shutil
from datetime import datetime
import os

def realizar_backup(origem):
    try:
        data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = f"backups/backup_{data_atual}.db"
        
        os.makedirs("backups", exist_ok=True)
        shutil.copy2(origem, destino)
        
        return destino
    except Exception as e:
        raise Exception(f"Erro ao realizar backup: {str(e)}")