# 🔍 Herramienta de Análisis de Subredes para Respuesta a Incidentes (Blue Team)

## 🎯 Propósito del Proyecto
Durante la contención de un incidente de ciberseguridad, aislar segmentos de red infectados es una tarea crítica. Esta herramienta, desarrollada en **Python**, automatiza los cálculos de *subnetting* (IPv4) necesarios para crear reglas de firewall inmediatas.

Al proporcionar una IP comprometida y su notación CIDR, el script calcula instantáneamente la dirección de red (para aislamiento), el broadcast y el rango de hosts válidos, eliminando el margen de error humano bajo presión.

## 🛠️ Habilidades Demostradas
- Programación funcional en **Python**.
- Dominio de los protocolos **TCP/IP** y cálculo de subredes.
- Creación de herramientas de línea de comandos (CLI) integradas al `$PATH` de Linux.
- Manejo de argumentos con la librería `argparse`.
- Generación automática de bitácoras de incidentes (archivos `.txt`).

## ⚙️ Instalación en Linux (Integración al sistema)

Esta herramienta está diseñada para comportarse como un comando nativo en tu sistema Linux (Kali, BackBox, etc.).

1. Descarga el repositorio:
   ```bash
   git clone [URL_DE_TU_REPOSITORIO]
   cd SOC-Subnet-Analyzer
## ⚙️ Instalación en Linux (Integración al sistema)

Esta herramienta está diseñada para comportarse como un comando nativo en tu sistema Linux.

**1. Clona el repositorio**
```bash
git clone https://github.com/splashartguy117-maker/SOC-Subnet-Analyzer.git
cd SOC-Subnet-Analyzer
```

**2. Da permisos de ejecución al script**
```bash
chmod +x subnet_analyzer.py
```

**3. Instala globalmente (opcional)**
```bash
sudo ln -s $(pwd)/subnet_analyzer.py /usr/local/bin/subnet-analyzer
```
