# 🔍 SOC Subnet Analyzer

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)]()

Herramienta profesional de análisis de subredes con inteligencia de amenazas, diseñada para equipos de **Blue Team** y **Respuesta a Incidentes**.

Al proporcionar una IP comprometida y su notación CIDR, el script calcula instantáneamente la dirección de red, el broadcast y el rango de hosts válidos, además de consultar la reputación de la IP en **AbuseIPDB** y generar reglas de firewall listas para usar.

---

## 🎯 Características

- ✅ Cálculo instantáneo de subredes IPv4 (red, broadcast, rango de hosts)
- 🛡️ **Consulta de reputación** de IPs en AbuseIPDB (detección de amenazas)
- 🔥 **Generación de reglas de firewall** (iptables) para aislar redes infectadas
- 📄 **Reportes automáticos** en formato `.txt` para bitácoras de incidentes
- 🎨 **Salida con colores** para mejorar la legibilidad en terminal
- 🔐 **Manejo seguro de API Keys** mediante archivo `.env`
- 🌍 **Compatible con cualquier distribución de Linux**

---

## 📋 Requisitos previos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)
- Conexión a Internet (para consultar la API de AbuseIPDB)

---

## 📥 Instalación

### 1️⃣ Instalar dependencias del sistema

Elige el comando según tu distribución:

| Distribución | Comando |
|--------------|---------|
| **Void Linux** | `sudo xbps-install -S python3 python3-pip git` |
| **Arch / CachyOS / Manjaro** | `sudo pacman -S --needed python python-pip git` |
| **Debian / Ubuntu / Kali** | `sudo apt update && sudo apt install python3 python3-pip git` |
| **Fedora / RHEL** | `sudo dnf install python3 python3-pip git` |
| **openSUSE** | `sudo zypper install python3 python3-pip git` |

---

### 2️⃣ Clonar el repositorio

```bash
git clone https://github.com/splashartguy117-maker/SOC-Subnet-Analyzer.git
cd SOC-Subnet-Analyzer
```

---

### 3️⃣ Instalar las dependencias de Python

Tienes **dos opciones**. Elige la que mejor se adapte a tu sistema:

#### 🅰️ Opción A: Instalación con `pip` (recomendada)

```bash
pip install -r requirements.txt
```

> **⚠️ Nota:** Si tu distribución da el error `externally-managed-environment`, usa la Opción B o agrega la bandera `--break-system-packages`:
> ```bash
> pip install --user --break-system-packages -r requirements.txt
> ```

#### 🅱️ Opción B: Instalación con paquetes del sistema (más limpia)

| Distribución | Comando |
|--------------|---------|
| **Void Linux** | `sudo xbps-install -S python3-requests python3-colorama python3-dotenv` |
| **Arch / CachyOS** | `sudo pacman -S --needed python-requests python-colorama python-dotenv` |
| **Debian / Ubuntu** | `sudo apt install python3-requests python3-colorama python3-dotenv` |
| **Fedora** | `sudo dnf install python3-requests python3-colorama python3-dotenv` |

---

### 4️⃣ Configurar tu API Key de AbuseIPDB

1. Crea una cuenta gratuita en [AbuseIPDB](https://www.abuseipdb.com/).
2. Ve a tu perfil y copia tu **API Key**.
3. Crea el archivo `.env` en la raíz del proyecto:

```bash
nano .env
```

4. Pega el siguiente contenido (reemplaza con tu clave real):

```text
ABUSEIPDB_API_KEY=tu_clave_aqui
```

> **🔒 Importante:** No uses comillas, espacios ni caracteres extraños. El archivo debe contener exactamente una línea.

5. Guarda con `Ctrl+O`, `Enter`, `Ctrl+X`.

---

### 5️⃣ Dar permisos de ejecución

```bash
chmod +x subnet_analyzer.py
```

---

### 6️⃣ Instalación global (opcional, pero recomendada)

Para poder usar la herramienta desde **cualquier carpeta** como un comando nativo:

```bash
sudo ln -sf "$(pwd)/subnet_analyzer.py" /usr/local/bin/subnet-analyzer
```

#### Verificar la instalación

```bash
ls -la /usr/local/bin/subnet-analyzer
```

Debe mostrar algo como:
```
/usr/local/bin/subnet-analyzer -> /home/tu_usuario/SOC-Subnet-Analyzer/subnet_analyzer.py
```

#### Verificar que `/usr/local/bin` está en el PATH

```bash
echo $PATH | tr ':' '\n' | grep -x "/usr/local/bin"
```

Si **no aparece**, agrégalo a tu shell (ejemplo para Bash):

```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Uso

### Desde cualquier carpeta (si instalaste globalmente)

```bash
subnet-analyzer 192.168.1.0/24
```

### Desde la carpeta del proyecto

```bash
python3 subnet_analyzer.py 192.168.1.0/24
```

### Ver ayuda

```bash
subnet-analyzer -h
```

### Ver versión

```bash
subnet-analyzer -v
```

---

## 📊 Ejemplo de salida

```
============================================================
🔍 SOC Subnet Analyzer - Reporte de Incidentes
============================================================
📌 Dirección IP/CIDR: 192.168.1.0/24
📅 Fecha y hora: 2026-09-16 20:30:15
------------------------------------------------------------
🌐 Dirección de Red: 192.168.1.0
🔢 Máscara de Subred: 255.255.255.0
📡 Broadcast: 192.168.1.255
📊 Total de Hosts: 254
🔹 Primer Host: 192.168.1.1
🔸 Último Host: 192.168.1.254
------------------------------------------------------------
🛡️  Consultando reputación de IP (192.168.1.0) en AbuseIPDB...
   🟢 Nivel de Abuso: 0%
   📝 Reportes totales: 0
   🌍 País: Desconocido
   🏢 ISP: Desconocido
------------------------------------------------------------
🛡️  Regla de Firewall sugerida (aislar red):
   iptables -A INPUT -s 192.168.1.0/24 -j DROP
------------------------------------------------------------
✅ Bitácora guardada en: bitacora_192.168.1.0.txt
============================================================
```

---

## 📂 Estructura del Proyecto

```
SOC-Subnet-Analyzer/
├── subnet_analyzer.py   # Script principal
├── requirements.txt     # Dependencias de Python
├── .env                 # Variables de entorno (NO se sube a GitHub)
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Documentación
```

---

## 🛠️ Solución de problemas comunes

### ❌ `ModuleNotFoundError: No module named 'requests'`

**Causa:** Faltan las dependencias de Python.

**Solución:** Instálalas con la Opción A o B del paso 3.

---

### ❌ `python3: can't open file '.../main.py': [Errno 2] No such file or directory`

**Causa:** El enlace simbólico o un alias apunta a un archivo que no existe (`main.py` en lugar de `subnet_analyzer.py`).

**Solución:**

1. Verifica a dónde apunta el enlace:
   ```bash
   ls -la /usr/local/bin/subnet-analyzer
   ```

2. Si apunta mal, elimínalo y créalo de nuevo:
   ```bash
   sudo rm -f /usr/local/bin/subnet-analyzer
   sudo ln -sf "$(pwd)/subnet_analyzer.py" /usr/local/bin/subnet-analyzer
   ```

3. Revisa si tienes un comando duplicado en `~/.local/bin`:
   ```bash
   type subnet-analyzer
   ```
   Si aparece `/home/tu_usuario/.local/bin/subnet-analyzer`, bórralo:
   ```bash
   rm -f ~/.local/bin/subnet-analyzer
   hash -r
   ```

---

### ❌ `No se encontró el archivo .env`

**Causa:** El script busca el `.env` en la carpeta equivocada.

**Solución:** Asegúrate de que el `.env` esté en la **misma carpeta** que `subnet_analyzer.py`.

```bash
ls -la ~/SOC-Subnet-Analyzer/.env
```

Si no existe, créalo:
```bash
cd ~/SOC-Subnet-Analyzer
nano .env
```

---

### ❌ `❌ No se encontró ABUSEIPDB_API_KEY en el archivo .env`

**Causa:** El nombre de la variable está mal escrito o el archivo tiene formato incorrecto.

**Solución:** Verifica el contenido:
```bash
cat ~/SOC-Subnet-Analyzer/.env
```

Debe mostrar exactamente:
```text
ABUSEIPDB_API_KEY=tu_clave_real
```

Sin comillas, sin espacios alrededor del `=`, sin líneas vacías.

---

### ❌ `❌ Error en la consulta: 401 Client Error`

**Causa:** Tu API Key es inválida o está expirada.

**Solución:** Verifica tu clave en [AbuseIPDB](https://www.abuseipdb.com/account/api) y actualízala en el `.env`.

---

### ❌ `❌ Error en la consulta: 429 Client Error`

**Causa:** Excediste el límite de consultas diarias del plan gratuito (1000/día).

**Solución:** Espera 24 horas o actualiza tu plan en AbuseIPDB.

---

### ❌ `Permission denied` al leer el `.env`

**Solución:** Ajusta los permisos:
```bash
chmod 600 ~/SOC-Subnet-Analyzer/.env
```

---

## 🔐 Seguridad

- **NUNCA** subas tu archivo `.env` a GitHub. Ya está incluido en `.gitignore`.
- **NUNCA** compartas tu API Key públicamente.
- Si accidentalmente subes tu `.env`, **revoca la clave inmediatamente** en AbuseIPDB y genera una nueva.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar esta herramienta:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad: `git checkout -b feature/nueva-funcionalidad`.
3. Haz commit de tus cambios: `git commit -m "✨ Añade nueva funcionalidad"`.
4. Sube la rama: `git push origin feature/nueva-funcionalidad`.
5. Abre un Pull Request.

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**splashartguy117-maker**
- GitHub: [@splashartguy117-maker](https://github.com/splashartguy117-maker)

---

## 🙏 Agradecimientos

- [AbuseIPDB](https://www.abuseipdb.com/) por su API gratuita de inteligencia de amenazas.
- Comunidad de ciberseguridad por la inspiración y el feedback.

---

## ⭐ ¿Te gustó el proyecto?

Si esta herramienta te resultó útil, considera darle una **estrella ⭐** en GitHub. ¡Motiva a seguir creando más herramientas para la comunidad de Blue Team!
