# /opt/eclosion/bin/monje_pasivo.py
import time
import numpy as np
import os
import json
import hashlib
from board import SCL, SDA
import busio
from adafruit_ina219 import INA219

# Configuración
BUZON = "/dev/shm/buzon_salida"
I2C_BUS = busio.I2C(SCL, SDA)
SENSOR_ENERGIA = INA219(I2C_BUS)

# Estado Interno (Modelo P(NC))
# Calibración inicial simple (media móvil exponencial)
linea_base_energia = 0.0
linea_base_temp = 45.0 # Valor semilla

def leer_sensores_72d():
    """Lee el estado físico sin generar eventos activos"""
    # 1. Energía (INA219 - Hardware Externo)
    potencia = SENSOR_ENERGIA.power
    # 2. Temperatura (MSR - Hardware Interno)
    # (Simulado aquí leyendo archivo térmico para compatibilidad universal Linux)
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = int(f.read()) / 1000.0
    # 3. Ciclos (TSC - Aproximado con time.perf_counter_ns para pureza Python)
    ciclos = time.perf_counter_ns()
    
    return np.array([potencia, temp, ciclos], dtype=np.float64)

def ciclo_monastico():
    global linea_base_energia
    print("[MONJE] Iniciando voto de silencio y observación...")
    
    while True:
        # 1. Observación Pasiva (200Hz)
        vector_no = leer_sensores_72d()
        
        # 2. Actualizar Modelo Interno (Aprendizaje Pasivo)
        # Si el cambio es suave, es ruido de fondo.
        linea_base_energia = (linea_base_energia * 0.99) + (vector_no[0] * 0.01)
        
        # 3. Detección de Sorpresa (Bayes Factor simplificado)
        # Desviación masiva instantánea vs Línea base
        desviacion = abs(vector_no[0] - linea_base_energia)
        
        if desviacion > 50.0: # Umbral de sorpresa calibrado (mW)
            # ¡EVENTO!
            bf = desviacion * 1000 # Pseudocálculo de BF para velocidad
            
            # 4. Sellar Concepto
            datos_sello = vector_no.tobytes()
            hash_sello = hashlib.sha256(datos_sello).hexdigest()
            
            acta = {
                "tipo": "CONCEPTO_VALIDADO",
                "hash": hash_sello,
                "sorpresa_bf": bf,
                "vector_72d": vector_no.tolist(),
                "timestamp": time.time()
            }
            
            # 5. Escribir en BUZÓN (RAM)
            # Usamos nombre único para evitar colisiones
            nombre_archivo = f"sello_{hash_sello[:8]}_{int(time.time()*1000)}.json"
            with open(os.path.join(BUZON, nombre_archivo), "w") as f:
                json.dump(acta, f)
            
            print(f"[MONJE] ¡Sorpresa! BF={bf:.0f} Hash={hash_sello[:8]}")
            
            # Periodo refractario para no medir el eco de la propia escritura
            time.sleep(0.1)
            
        time.sleep(0.005) # 200Hz

if __name__ == "__main__":
    ciclo_monastico()
