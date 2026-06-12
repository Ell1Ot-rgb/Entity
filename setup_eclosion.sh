#!/bin/bash
# setup_eclosion.sh - Despliegue vΩ.4.2

# 1. PARÁMETROS
USER_HOME="/opt/eclosion"
RAM_LAB="/dev/shm/laboratorio"
RAM_BUZON="/dev/shm/buzon_salida"
NVME_MOUNT="/mnt/caja_fuerte_remota"
REMOTE_NFS="192.168.1.50:/mnt/nvme_remoto"

echo "[INFO] Iniciando despliegue de Eclosión vΩ.4.2..."

# 2. PREPARAR SISTEMA DE ARCHIVOS (LA ESCLUSA)
echo "[INFO] Configurando Esclusa de Aire..."
# Crear directorios en RAM (Volátiles, Puros)
sudo mkdir -p $RAM_LAB $RAM_BUZON
sudo chmod 777 $RAM_LAB $RAM_BUZON

# Montar NVMe Remoto (Persistente, Sucio)
sudo mkdir -p $NVME_MOUNT
# Instalar cliente NFS si falta
if ! dpkg -l | grep -q nfs-common; then
    sudo apt-get update && sudo apt-get install -y nfs-common
fi
# Montar con noatime para reducir ruido
if ! mount | grep -q $NVME_MOUNT; then
    sudo mount -t nfs -o noatime,tcp,soft $REMOTE_NFS $NVME_MOUNT
    echo "[OK] NVMe remoto montado."
else
    echo "[INFO] NVMe ya estaba montado."
fi

# 3. PREPARAR ENTORNO DE SOFTWARE
echo "[INFO] Instalando dependencias del Monje..."
sudo apt-get install -y python3-venv python3-dev i2c-tools libgpiod-dev linux-tools-generic

# Crear directorio del proyecto
sudo mkdir -p $USER_HOME/bin $USER_HOME/logs
sudo chown -R $USER:$USER $USER_HOME

# Entorno Virtual
python3 -m venv $USER_HOME/venv
source $USER_HOME/venv/bin/activate

# Instalar librerías científicas y de hardware
pip install numpy scipy psutil adafruit-circuitpython-ina219 RPi.GPIO

# 4. CONFIGURAR GRUPOS DE CONTROL (CGROUPS)
# Esto aísla al Monje en el Núcleo 1 y al Sistema en el Núcleo 0
echo "[INFO] Configurando aislamiento de CPU..."
# Nota: Requiere cgroup-tools instalado
if ! dpkg -l | grep -q cgroup-tools; then
    sudo apt-get install -y cgroup-tools
fi

# Crear grupo 'monje' (Núcleo 1, Alta Prioridad)
sudo cgcreate -g cpuset,memory:monje
sudo cgset -r cpuset.cpus=1 monje
sudo cgset -r cpuset.mems=0 monje
# Crear grupo 'mundo' (Núcleo 0, Resto del sistema)
sudo cgcreate -g cpuset,memory:mundo
sudo cgset -r cpuset.cpus=0 mundo
sudo cgset -r cpuset.mems=0 mundo

echo "[OK] Despliegue completado. Listo para inyectar código."
