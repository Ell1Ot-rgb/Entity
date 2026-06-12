# 📂 DOSSIER DE MISIÓN: DESPLIEGUE ECLOSIÓN vΩ.4.2

## Objetivo
Instalar un validador de realidad física (El Monje) y un sistema de persistencia desacoplado (El Mensajero) en un entorno de hardware limitado. 

**Prioridad:** Pureza Filosófica (Cero auto-contaminación).

## Arquitectura del Sistema

Este sistema implementa una "Esclusa de Aire" que separa:
- **Dominio Puro (RAM):** Observación y validación sin contaminación
- **Dominio Persistente (NVMe Remoto):** Almacenamiento de eventos validados

### Componentes

1. **El Monje (monje_pasivo.py):** Validador de realidad física
   - Ejecuta en núcleo dedicado (CPU 1)
   - Observación pasiva a 200Hz
   - Detección de sorpresas mediante Bayes Factor
   - Sellado criptográfico de conceptos validados

2. **El Mensajero (mensajero_silencioso.py):** Sistema de persistencia
   - Ejecuta con baja prioridad (nice -n 19)
   - Transfiere datos de RAM a NVMe remoto
   - Opera sin interferir con el Monje

3. **El Copiloto (generador_eventos.py):** Generador de eventos
   - Herramienta para interactuar con el sistema
   - Escribe en el "Laboratorio" RAM

## FASE 1: PREPARACIÓN DEL HARDWARE

### Requisitos del Sistema
- **CPU:** 2 núcleos físicos (Hyperthreading/SMT desactivado)
- **RAM:** 8GB mínimo
- **Almacenamiento:** HDD local + NVMe remoto vía NFS
- **Red:** Raspberry Pi 4 en 192.168.1.50 exportando /mnt/nvme_remoto

### Conexión de Sensores (Anclas de Realidad)

#### Sensor INA219 (Energía)
- Soldar al rail de 12V o 5V de la fuente de poder interna
- Conectar I2C:
  - SDA → GPIO 2
  - SCL → GPIO 3

#### Módulo GPS (Tiempo)
- Conectar pin PPS → GPIO 18

### Configuración BIOS/UEFI
1. Desactivar Hyperthreading (SMT) para núcleos físicos puros
2. Activar C-States (para mediciones de "silencio" profundo)

## FASE 2: INSTALACIÓN DEL SOFTWARE

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/Ell1Ot-rgb/Entity.git
cd Entity
```

### Paso 2: Ejecutar el Instalador Maestro
```bash
chmod +x setup_eclosion.sh
sudo ./setup_eclosion.sh
```

Este script:
- Configura la "Esclusa de Aire" (directorios RAM y NVMe)
- Instala dependencias Python y del sistema
- Configura cgroups para aislamiento de CPU
- Crea entorno virtual Python

### Paso 3: Copiar Archivos del Proyecto
```bash
# Copiar scripts Python al directorio de instalación
sudo cp bin/*.py /opt/eclosion/bin/

# Copiar servicios systemd
sudo cp systemd/*.service /etc/systemd/system/
```

## FASE 3: ACTIVACIÓN DE SERVICIOS

### Habilitar y Arrancar Servicios
```bash
# Recargar configuración de systemd
sudo systemctl daemon-reload

# Habilitar servicios para arranque automático
sudo systemctl enable eclosion-monje
sudo systemctl enable eclosion-mensajero

# Iniciar servicios
sudo systemctl start eclosion-monje
sudo systemctl start eclosion-mensajero
```

### Verificar Estado de Servicios
```bash
# Ver estado del Monje
sudo systemctl status eclosion-monje

# Ver estado del Mensajero
sudo systemctl status eclosion-mensajero

# Ver logs en tiempo real
sudo journalctl -u eclosion-monje -f
sudo journalctl -u eclosion-mensajero -f
```

## FASE 4: USO DEL SISTEMA

### Generar Eventos de Prueba
```bash
# Activar entorno virtual
source /opt/eclosion/venv/bin/activate

# Ejecutar generador de eventos
sudo cgexec -g cpuset:mundo python /opt/eclosion/bin/generador_eventos.py
```

### Monitorear el Sistema

#### Ver Sellos en RAM (Buzón)
```bash
ls -lah /dev/shm/buzon_salida/
cat /dev/shm/buzon_salida/sello_*.json
```

#### Ver Datos Archivados (NVMe Remoto)
```bash
ls -lah /mnt/caja_fuerte_remota/diario_del_mundo/
cat /mnt/caja_fuerte_remota/diario_del_mundo/sello_*.json
```

## Arquitectura de Aislamiento

### Distribución de CPU (Cgroups)
- **Núcleo 0 (mundo):** Sistema operativo y El Mensajero
- **Núcleo 1 (monje):** El Monje (observador puro)

### Flujo de Datos
```
[Sensores Físicos] → [El Monje] → [RAM: Buzón] → [El Mensajero] → [NVMe Remoto]
       ↓                  ↓              ↓               ↓
   Energía/Temp      Validación    Sellos Hash    Persistencia
   INA219/MSR        Bayesiana     Temporal       Permanente
```

## Filosofía del Sistema

### Pureza Fenomenológica
El Monje no genera eventos activos; solo observa y valida. Su existencia computacional es mínima, acercándose al ideal de "observación sin perturbación".

### Esclusa de Aire
La separación RAM/NVMe previene la auto-contaminación: El Monje nunca lee de disco, solo de sensores y RAM pura.

### Sellos Criptográficos
Cada concepto validado recibe un hash SHA-256, garantizando integridad temporal y trazabilidad.

## Resolución de Problemas

### El Monje no Arranca
```bash
# Verificar que cgroups está configurado
cat /proc/cgroups

# Verificar sensor INA219
sudo i2cdetect -y 1
```

### NVMe Remoto no Monta
```bash
# Verificar conectividad
ping 192.168.1.50

# Verificar exportación NFS en Raspberry Pi
showmount -e 192.168.1.50

# Montar manualmente
sudo mount -t nfs -o noatime,tcp,soft 192.168.1.50:/mnt/nvme_remoto /mnt/caja_fuerte_remota
```

### Sin Detección de Eventos
- Verificar que el umbral de sorpresa (50.0 mW) es apropiado para tu hardware
- Ajustar en `/opt/eclosion/bin/monje_pasivo.py` línea 50

## Calibración Avanzada

### Ajustar Frecuencia de Observación
En `monje_pasivo.py`, modificar:
```python
time.sleep(0.005)  # 200Hz (cambiar para ajustar frecuencia)
```

### Ajustar Umbral de Sorpresa
En `monje_pasivo.py`, modificar:
```python
if desviacion > 50.0:  # Umbral en mW (ajustar según hardware)
```

### Ajustar Periodo Refractario
En `monje_pasivo.py`, modificar:
```python
time.sleep(0.1)  # Pausa post-evento (ajustar para evitar ecos)
```

## Desinstalación

```bash
# Detener servicios
sudo systemctl stop eclosion-monje eclosion-mensajero

# Deshabilitar servicios
sudo systemctl disable eclosion-monje eclosion-mensajero

# Eliminar archivos
sudo rm /etc/systemd/system/eclosion-*.service
sudo rm -rf /opt/eclosion

# Limpiar cgroups
sudo cgdelete cpuset:monje
sudo cgdelete cpuset:mundo

# Desmontar NVMe
sudo umount /mnt/caja_fuerte_remota
```

## Licencia y Créditos

Este sistema es parte del proyecto Entity - Sistema Fenomenológico.

**Filosofía:** "El silencio es el ruido de fondo del universo."

---

**FIN DEL DOSSIER. El sistema está listo para ser inyectado en la realidad.**
