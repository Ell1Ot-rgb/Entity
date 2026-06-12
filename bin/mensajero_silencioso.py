# /opt/eclosion/bin/mensajero_silencioso.py
import time
import shutil
import os
import glob

ORIGEN = "/dev/shm/buzon_salida"
DESTINO = "/mnt/caja_fuerte_remota/diario_del_mundo"

# Asegurar destino
os.makedirs(DESTINO, exist_ok=True)

print("[MENSAJERO] Guardia iniciada. Esperando sellos...")

while True:
    archivos = glob.glob(os.path.join(ORIGEN, "*.json"))
    
    if archivos:
        # PAUSA TÁCTICA (2s): Dejar que el evento físico se disipe
        time.sleep(2.0)
        
        for f in archivos:
            try:
                # Mover (Operación costosa)
                shutil.move(f, DESTINO)
                print(f"[MENSAJERO] {os.path.basename(f)} archivado en eternidad.")
            except Exception as e:
                print(f"[ERROR] {e}")
    
    time.sleep(1.0)
