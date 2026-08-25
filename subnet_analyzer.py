#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
import argparse
import datetime
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# --- CONFIGURACIÓN DE RUTAS Y API ---
script_real_path = Path(os.path.realpath(__file__)).parent
env_file = script_real_path / '.env'
if not env_file.exists():
    env_file = Path.cwd() / '.env'

if env_file.exists():
    load_dotenv(dotenv_path=env_file)
    print(f"✅ Archivo .env cargado desde: {env_file}")
else:
    print(f"❌ No se encontró .env en {script_real_path} ni en {Path.cwd()}")
    load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
if not ABUSEIPDB_API_KEY:
    print("❌ No se encontró ABUSEIPDB_API_KEY en el archivo .env")
    print("💡 Asegúrate de que el .env contenga: ABUSEIPDB_API_KEY=tu_clave_aqui")
else:
    print(f"🔑 API Key cargada correctamente: {ABUSEIPDB_API_KEY[:5]}...")

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

# --- FUNCIÓN: CONSULTAR REPUTACIÓN ---
def consultar_reputacion_ip(ip_address):
    """Consulta la reputación de una IP en AbuseIPDB."""
    if not ABUSEIPDB_API_KEY:
        print("   ⚠️  No se encontró API Key. Configura tu archivo .env")
        return None

    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90'
    }

    try:
        response = requests.get(ABUSEIPDB_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                return {
                    'ip': data['data']['ipAddress'],
                    'abuse_score': data['data'].get('abuseConfidenceScore', 0),
                    'total_reports': data['data'].get('totalReports', 0),
                    'country': data['data'].get('countryName', 'Desconocido'),
                    'isp': data['data'].get('isp', 'Desconocido')
                }
            else:
                print("   ℹ️  No se encontró información de reputación para esta IP.")
                return None
        else:
            print(f"   ⚠️  Error HTTP {response.status_code}: {response.text[:100]}")
            return None
    except Exception as e:
        print(f"   ⚠️  Error de conexión: {e}")
        return None

# --- FUNCIÓN: GENERAR REGLA FIREWALL ---
def generar_regla_firewall(red, accion="DROP"):
    """Genera una regla de iptables para bloquear toda la subred."""
    return f"iptables -A INPUT -s {red} -j {accion}"

# --- FUNCIÓN: ANALIZAR SUBRED ---
def analizar_subred(ip_cidr):
    try:
        red = ipaddress.ip_network(ip_cidr, strict=False)
        hosts = list(red.hosts())

        print("\n" + "="*60)
        print(f"{Fore.CYAN}🔍 SOC Subnet Analyzer - Reporte de Incidentes{Style.RESET_ALL}")
        print("="*60)
        
        print(f"{Fore.YELLOW}📌 Dirección IP/CIDR:{Style.RESET_ALL} {ip_cidr}")
        print(f"{Fore.YELLOW}📅 Fecha y hora:{Style.RESET_ALL} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)

        print(f"{Fore.GREEN}🌐 Dirección de Red:{Style.RESET_ALL} {red.network_address}")
        print(f"{Fore.GREEN}🔢 Máscara de Subred:{Style.RESET_ALL} {red.netmask}")
        print(f"{Fore.GREEN}📡 Broadcast:{Style.RESET_ALL} {red.broadcast_address}")
        print(f"{Fore.GREEN}📊 Total de Hosts:{Style.RESET_ALL} {red.num_addresses - 2 if red.num_addresses > 2 else 0}")
        print(f"{Fore.GREEN}🔹 Primer Host:{Style.RESET_ALL} {hosts[0] if hosts else 'N/A'}")
        print(f"{Fore.GREEN}🔸 Último Host:{Style.RESET_ALL} {hosts[-1] if hosts else 'N/A'}")
        print("-"*60)

        ip_a_consultar = str(red.network_address)
        print(f"{Fore.CYAN}🛡️  Consultando reputación de IP ({ip_a_consultar}) en AbuseIPDB...{Style.RESET_ALL}")
        
        info_reputacion = consultar_reputacion_ip(ip_a_consultar)
        if info_reputacion:
            score = info_reputacion['abuse_score']
            if score >= 80:
                color_score = Fore.RED
                emoji_score = "🔴"
            elif score >= 40:
                color_score = Fore.YELLOW
                emoji_score = "🟡"
            else:
                color_score = Fore.GREEN
                emoji_score = "🟢"
            
            print(f"   {emoji_score} {color_score}Nivel de Abuso: {score}%{Style.RESET_ALL}")
            print(f"   📝 Reportes totales: {info_reputacion['total_reports']}")
            print(f"   🌍 País: {info_reputacion['country']}")
            print(f"   🏢 ISP: {info_reputacion['isp']}")
        else:
            print(f"   {Fore.YELLOW}⚠️  No se pudo consultar la reputación. La IP puede no tener reportes o hubo un error.{Style.RESET_ALL}")
        
        print("-"*60)

        print(f"{Fore.CYAN}🛡️  Regla de Firewall sugerida (aislar red):{Style.RESET_ALL}")
        regla = generar_regla_firewall(red.network_address)
        print(f"   {Fore.YELLOW}{regla}{Style.RESET_ALL}")
        print("-"*60)

        nombre_archivo = f"bitacora_{red.network_address}.txt"
        with open(nombre_archivo, "w") as f:
            f.write(f"Reporte de Incidente - Subred {red.network_address}\n")
            f.write(f"Fecha: {datetime.datetime.now()}\n")
            f.write(f"IP/CIDR: {ip_cidr}\n")
            f.write(f"Red: {red.network_address}\n")
            f.write(f"Máscara: {red.netmask}\n")
            f.write(f"Broadcast: {red.broadcast_address}\n")
            f.write(f"Hosts: {hosts[0] if hosts else 'N/A'} - {hosts[-1] if hosts else 'N/A'}\n")
            if info_reputacion:
                f.write(f"\n--- REPUTACIÓN DE IP ---\n")
                f.write(f"IP consultada: {info_reputacion['ip']}\n")
                f.write(f"Score de abuso: {info_reputacion['abuse_score']}%\n")
                f.write(f"Reportes: {info_reputacion['total_reports']}\n")
                f.write(f"País: {info_reputacion['country']}\n")
                f.write(f"ISP: {info_reputacion['isp']}\n")
            f.write(f"\n--- REGLA DE FIREWALL ---\n")
            f.write(f"{regla}\n")

        print(f"{Fore.GREEN}✅ Bitácora guardada en: {nombre_archivo}{Style.RESET_ALL}")
        print("="*60 + "\n")

    except ValueError as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Usa el formato correcto (ej: 192.168.1.0/24){Style.RESET_ALL}")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Herramienta de análisis de subredes y reputación de IPs para Blue Team."
    )
    parser.add_argument(
        "ip_cidr",
        help="Dirección IP con notación CIDR (ej: 192.168.1.0/24)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="SOC Subnet Analyzer v2.0 (con inteligencia de amenazas)"
    )
    args = parser.parse_args()

    analizar_subred(args.ip_cidr)
