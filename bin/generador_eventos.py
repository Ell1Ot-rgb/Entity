# /opt/eclosion/bin/generador_eventos.py
import time
import os

LABORATORIO = "/dev/shm/laboratorio"
os.makedirs(LABORATORIO, exist_ok=True)

def escribir_poema(nombre, contenido):
    ruta = os.path.join(LABORATORIO, nombre)
    print(f"[MUNDO] El humano escribe: {nombre}...")
    with open(ruta, "w") as f:
        f.write(contenido)
    # El archivo vive lo justo para ser medido
    time.sleep(0.5)
    os.remove(ruta)
    print("[MUNDO] Evento finalizado.")

if __name__ == "__main__":
    # Ejemplo de interacción
    escribir_poema("triste.txt", "El silencio es el ruido de fondo del universo.")
