# Guía de Inicio Rápido - Eclosión vΩ.4.2

## Prerrequisitos Hardware

Antes de comenzar, asegúrate de tener:

1. **PC con:**
   - 2 núcleos físicos (Hyperthreading desactivado en BIOS)
   - 8GB RAM mínimo
   - Linux instalado (Ubuntu/Debian recomendado)

2. **Raspberry Pi 4 (Almacenamiento Remoto):**
   - IP configurada en 192.168.1.50
   - NVMe conectado y montado en `/mnt/nvme_remoto`
   - NFS server configurado exportando `/mnt/nvme_remoto`

3. **Sensores (Opcional pero recomendado):**
   - Sensor INA219 conectado a I2C (GPIO 2/3)
   - Módulo GPS con PPS en GPIO 18

## Instalación en 5 Pasos

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Ell1Ot-rgb/Entity.git
cd Entity
```

### 2. Ejecutar el Instalador
```bash
chmod +x setup_eclosion.sh
sudo ./setup_eclosion.sh
```

**Nota:** Este proceso puede tardar varios minutos. Instalará dependencias, configurará cgroups y creará el entorno virtual Python.

### 3. Copiar Archivos al Sistema
```bash
# Copiar scripts Python
sudo cp bin/*.py /opt/eclosion/bin/

# Copiar servicios systemd
sudo cp systemd/*.service /etc/systemd/system/
```

### 4. Activar los Servicios
```bash
sudo systemctl daemon-reload
sudo systemctl enable eclosion-monje
sudo systemctl enable eclosion-mensajero
sudo systemctl start eclosion-monje
sudo systemctl start eclosion-mensajero
```

### 5. Verificar que Funciona
```bash
# Ver estado de los servicios
sudo systemctl status eclosion-monje
sudo systemctl status eclosion-mensajero

# Ver logs en tiempo real
sudo journalctl -u eclosion-monje -f
```

## Primera Prueba

### Generar un Evento de Prueba
```bash
# Activar entorno virtual
source /opt/eclosion/venv/bin/activate

# Ejecutar generador de eventos
sudo cgexec -g cpuset:mundo python /opt/eclosion/bin/generador_eventos.py
```

### Ver los Resultados

**Sellos en RAM (temporal):**
```bash
ls -lh /dev/shm/buzon_salida/
cat /dev/shm/buzon_salida/sello_*.json
```

**Sellos archivados (permanente):**
```bash
ls -lh /mnt/caja_fuerte_remota/diario_del_mundo/
cat /mnt/caja_fuerte_remota/diario_del_mundo/sello_*.json
```

## Comandos Útiles

### Control de Servicios
```bash
# Detener servicios
sudo systemctl stop eclosion-monje
sudo systemctl stop eclosion-mensajero

# Reiniciar servicios
sudo systemctl restart eclosion-monje
sudo systemctl restart eclosion-mensajero

# Ver logs
sudo journalctl -u eclosion-monje -n 50
sudo journalctl -u eclosion-mensajero -n 50
```

### Monitoreo del Sistema
```bash
# Ver uso de CPU por núcleo
mpstat -P ALL 1

# Ver procesos en cgroups
cat /sys/fs/cgroup/cpuset/monje/tasks
cat /sys/fs/cgroup/cpuset/mundo/tasks

# Ver temperatura del sistema
cat /sys/class/thermal/thermal_zone0/temp
```

### Limpieza de Datos
```bash
# Limpiar buzón RAM
sudo rm -f /dev/shm/buzon_salida/*.json

# Limpiar laboratorio RAM
sudo rm -f /dev/shm/laboratorio/*
```

## Solución Rápida de Problemas

### Error: "No se puede montar NVMe remoto"
```bash
# Verificar conectividad
ping 192.168.1.50

# Verificar que NFS está exportado
showmount -e 192.168.1.50

# Montar manualmente
sudo mount -t nfs 192.168.1.50:/mnt/nvme_remoto /mnt/caja_fuerte_remota
```

### Error: "No se pueden crear cgroups"
```bash
# Instalar cgroup-tools
sudo apt-get install cgroup-tools

# Verificar que el kernel soporta cgroups
cat /proc/cgroups
```

### Error: "Sensor INA219 no encontrado"
```bash
# Verificar I2C
sudo i2cdetect -y 1

# Habilitar I2C si no está activo
sudo raspi-config  # En Raspberry Pi
# O editar /boot/config.txt y añadir: dtparam=i2c_arm=on
```

### Error: "ModuleNotFoundError" en Python
```bash
# Activar entorno virtual primero
source /opt/eclosion/venv/bin/activate

# Reinstalar dependencias
pip install numpy scipy psutil adafruit-circuitpython-ina219 RPi.GPIO
```

## Próximos Pasos

1. **Calibrar Umbrales:** Ajusta el umbral de sorpresa en `/opt/eclosion/bin/monje_pasivo.py` según tu hardware
2. **Personalizar Eventos:** Modifica `generador_eventos.py` para crear tus propios eventos
3. **Análisis de Datos:** Examina los JSON generados para entender los patrones de tu sistema

## Documentación Completa

Para información detallada sobre arquitectura, filosofía y configuración avanzada, consulta:
- [INSTALLATION.md](INSTALLATION.md) - Guía completa
- [README.md](../README.md) - Descripción general del proyecto

---

**¡Sistema listo! El Monje observa, El Mensajero archiva.**
