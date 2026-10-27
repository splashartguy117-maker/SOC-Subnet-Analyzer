🛡️ SOC Subnet Analyzer

Una herramienta rápida y ligera desarrollada en Python para el cálculo y análisis de subredes orientada a entornos Blue Team, análisis de redes e investigaciones de respuesta a incidentes en un SOC (Security Operations Center).

Permite a los analistas de seguridad realizar triaje rápido de direcciones IP, determinar rangos de red utilizables, calcular máscaras de subred en notación CIDR y de comodín (wildcard masks), facilitando la identificación de activos y el aislamiento de segmentos de red comprometidos.

⚡ Características Principales

Cálculo de Subredes en Notación CIDR: Obtén dirección de red, dirección de broadcast, primera/última IP utilizable y total de hosts.

Máscaras de Comodín (Wildcard Masks): Útil para la configuración rápida de reglas de Firewall, listas de control de acceso (ACLs) y firmas en SIEM / IDS.

Diseño Ligero: Ejecución directa en terminal sin dependencias externas pesadas.

Integración CLI Global: Configurable como un comando ejecutable desde cualquier directorio del sistema (subnet-analyzer).

📁 Estructura del Repositorio

SOC-Subnet-Analyzer/
├── subnet_analyzer.py      # Script principal del analizador
├── README.md               # Documentación del proyecto
└── LICENSE                 # Licencia de uso libre (MIT)


📋 Requisitos Previos

Sistema Operativo: Linux (Debian, Ubuntu, Kali, Q4OS, etc.) o macOS.

Lenguaje: Python 3.x preinstalado.

⚙️ Instalación y Configuración como Comando Global

Sigue estos pasos para poder invocar la herramienta desde cualquier directorio ejecutando únicamente subnet-analyzer:

1. Clonar el repositorio

git clone https://github.com/splashartguy117-maker/SOC-Subnet-Analyzer.git
cd SOC-Subnet-Analyzer


2. Verificar o añadir el Shebang al script

Asegúrate de que la primera línea del archivo principal (ej. subnet_analyzer.py) contenga el shebang para que el sistema sepa cómo ejecutarlo:

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


3. Dar permisos de ejecución al archivo

chmod +x subnet_analyzer.py


4. Crear el enlace simbólico global

Crea un enlace en /usr/local/bin apuntando a la ruta absoluta de tu script. Usa el comando pwd para confirmar tu ubicación exacta antes de enlazar:

# Ejemplo usando la ruta absoluta obtenida con pwd:
sudo ln -s $(pwd)/subnet_analyzer.py /usr/local/bin/subnet-analyzer


(Si prefieres hacerlo manualmente, sustituye $(pwd) por tu ruta real, por ejemplo: /home/usuario/proyectos/SOC-Subnet-Analyzer/subnet_analyzer.py).

5. Actualizar la caché del shell (Opcional)

Si la terminal no reconoce el comando inmediatamente tras la instalación, recarga el índice de ejecutables:

En Bash: hash -r

En Zsh: rehash

💻 Ejemplo de Uso

Una vez configurado, puedes ejecutar la herramienta desde cualquier lugar del sistema:

# Ejecución global desde cualquier directorio
subnet-analyzer


Salida esperada en terminal:

==================================================
           SOC SUBNET ANALYZER TOOL               
==================================================
[+] Ingresa la subred/IP en notacion CIDR (ej. 192.168.1.0/24): 10.0.4.0/22

[-] Resultados del Análisis:
--------------------------------------------------
* Dirección de Red:      10.0.4.0
* Máscara de Subred:     255.255.252.0
* Máscara Wildcard:      0.0.3.255
* Dirección Broadcast:   10.0.7.255
* Primer Host Útil:      10.0.4.1
* Último Host Útil:      10.0.7.254
* Total de Hosts Útiles: 1022
==================================================


🤝 Contribución

¡Las contribuciones para mejorar la herramienta y expandir sus capacidades en operaciones SOC son bienvenidas!

Haz un Fork de este repositorio.

Crea una rama para tu nueva característica (git checkout -b feature/NuevaFeature).

Realiza tus cambios y haz Commit (git commit -m 'Añadida nueva funcionalidad').

Haz Push a la rama (git push origin feature/NuevaFeature).

Abre un Pull Request.

📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
