# Entity - Sistema Fenomenológico

**Eclosión vΩ.4.2-Híbrida**: Validador de Realidad Física con Arquitectura de Esclusa de Aire

## 🎯 Descripción

Sistema filosófico de observación y validación de realidad física, diseñado para hardware limitado (2 núcleos, 8GB RAM, HDD) utilizando una arquitectura de "Esclusa de Aire" que separa la observación pura (RAM) de la persistencia (NVMe remoto).

### Componentes Principales

- **El Monje (monje_pasivo.py):** Observador pasivo que valida eventos mediante inferencia Bayesiana
- **El Mensajero (mensajero_silencioso.py):** Sistema de persistencia silencioso que archiva eventos validados
- **El Copiloto (generador_eventos.py):** Generador de eventos para interacción humana

## 🚀 Inicio Rápido

```bash
# Clonar el repositorio
git clone https://github.com/Ell1Ot-rgb/Entity.git
cd Entity

# Ejecutar el instalador maestro
chmod +x setup_eclosion.sh
sudo ./setup_eclosion.sh

# Copiar archivos al sistema
sudo cp bin/*.py /opt/eclosion/bin/
sudo cp systemd/*.service /etc/systemd/system/

# Activar servicios
sudo systemctl daemon-reload
sudo systemctl enable --now eclosion-monje
sudo systemctl enable --now eclosion-mensajero
```

## 📖 Documentación Completa

Para instrucciones detalladas de instalación, configuración de hardware, y uso del sistema, consulta:

**[INSTALLATION.md](docs/INSTALLATION.md)** - Dossier de Misión Completo

## 🏗️ Arquitectura

### Esclusa de Aire (RAM + NVMe Remoto)

```
[Sensores Físicos] → [El Monje] → [RAM: Buzón] → [El Mensajero] → [NVMe Remoto]
     ↓                   ↓              ↓               ↓
 Energía/Temp       Validación     Sellos Hash    Persistencia
 INA219/MSR         Bayesiana      Temporal       Permanente
```

### Aislamiento de CPU (Cgroups)

- **Núcleo 0 (mundo):** Sistema operativo y El Mensajero
- **Núcleo 1 (monje):** El Monje (observación pura sin interferencias)

## 🔧 Requisitos del Sistema

### Hardware Mínimo
- CPU: 2 núcleos físicos (Hyperthreading desactivado)
- RAM: 8GB
- Almacenamiento: HDD local + NVMe remoto vía NFS
- Sensores: INA219 (energía), GPS (tiempo opcional)

### Software
- Linux (Ubuntu/Debian recomendado)
- Python 3.7+
- NFS client
- cgroup-tools
- i2c-tools

## 📊 Estructura del Proyecto

```
Entity/
├── README.md                 # Este archivo
├── setup_eclosion.sh         # Instalador maestro
├── bin/                      # Scripts Python principales
│   ├── monje_pasivo.py       # El Monje (validador)
│   ├── mensajero_silencioso.py  # El Mensajero (persistencia)
│   └── generador_eventos.py  # El Copiloto (generador)
├── systemd/                  # Servicios systemd
│   ├── eclosion-monje.service
│   └── eclosion-mensajero.service
└── docs/                     # Documentación
    └── INSTALLATION.md       # Guía completa de instalación
```

## 🔬 Filosofía del Sistema

### Pureza Fenomenológica
El Monje no genera eventos activos; solo observa y valida. Su existencia computacional es mínima, acercándose al ideal de "observación sin perturbación".

### Prevención de Auto-Contaminación
La arquitectura de Esclusa de Aire garantiza que el acto de observar no contamina lo observado. El Monje nunca lee de disco, solo de sensores y RAM pura.

### Sellos Criptográficos
Cada concepto validado recibe un hash SHA-256, garantizando integridad temporal y trazabilidad absoluta.

## 📝 Uso Básico

### Verificar Estado de Servicios
```bash
sudo systemctl status eclosion-monje
sudo systemctl status eclosion-mensajero
```

### Ver Logs en Tiempo Real
```bash
sudo journalctl -u eclosion-monje -f
sudo journalctl -u eclosion-mensajero -f
```

### Generar Evento de Prueba
```bash
source /opt/eclosion/venv/bin/activate
sudo cgexec -g cpuset:mundo python /opt/eclosion/bin/generador_eventos.py
```

### Examinar Sellos Validados
```bash
# En RAM (temporal)
ls -lah /dev/shm/buzon_salida/

# En NVMe (persistente)
ls -lah /mnt/caja_fuerte_remota/diario_del_mundo/
```

## 🐛 Solución de Problemas

Consulta la sección "Resolución de Problemas" en [INSTALLATION.md](docs/INSTALLATION.md) para:
- Problemas con cgroups
- Configuración de sensores I2C
- Montaje de NVMe remoto vía NFS
- Ajuste de umbrales de detección

## 📜 Licencia

Sistema Fenomenológico Entity - Eclosión vΩ.4.2

---

**"El silencio es el ruido de fondo del universo."**
