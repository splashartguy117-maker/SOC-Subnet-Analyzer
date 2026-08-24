#!/usr/bin/env python3
import ipaddress
import argparse
import datetime

def calculate_math_representation(network):
    # Extraemos el CIDR y calculamos los bits
    cidr = network.prefixlen
    host_bits = 32 - cidr
    total_hosts = (2 ** host_bits)
    usable_hosts = total_hosts - 2 if cidr < 31 else total_hosts
    
    # Determinamos el salto de octeto (Magic Number)
    netmask_octets = str(network.netmask).split('.')
    jump = 1
    modified_octet_value = 0
    for octet in netmask_octets:
        if int(octet) < 255:
            modified_octet_value = int(octet)
            jump = 256 - modified_octet_value
            break
            
    return host_bits, total_hosts, usable_hosts, jump, modified_octet_value

def analyze_subnet(ip_cidr, export_file=None):
    try:
        network = ipaddress.IPv4Network(ip_cidr, strict=False)
        host_bits, total_hosts, usable_hosts, jump, modified_octet_value = calculate_math_representation(network)
        
        first_host = network.network_address + 1 if network.prefixlen < 31 else network.network_address
        last_host = network.broadcast_address - 1 if network.prefixlen < 31 else network.broadcast_address
        
        # Construimos el reporte en una lista para poder imprimirlo y exportarlo fácilmente
        report = []
        report.append(f"[+] Análisis de Subred para: {ip_cidr}")
        report.append("-" * 55)
        report.append(f"Dirección de Red:          {network.network_address}")
        report.append(f"Dirección de Broadcast:    {network.broadcast_address}")
        report.append(f"Máscara de Red (Netmask):  {network.netmask}")
        report.append(f"Rango de Hosts Válidos:    {first_host} - {last_host}")
        report.append(f"Total de Hosts Útiles:     {usable_hosts}")
        report.append("-" * 55)
        report.append("[*] Desglose Analítico de los Cálculos:")
        report.append(f"  - Bits de red (CIDR): /{network.prefixlen}")
        report.append(f"  - Bits de host restantes: 32 - {network.prefixlen} = {host_bits} bits")
        report.append(f"  - Capacidad total de hosts: 2^{host_bits} = {total_hosts}")
        report.append(f"  - Hosts útiles (restando Red y Broadcast): {total_hosts} - 2 = {usable_hosts}")
        if network.prefixlen < 24:
            report.append(f"  - Salto de octeto: 256 - {modified_octet_value} (valor de máscara) = {jump}")
        report.append("-" * 55)
        
        # Unimos todo el texto
        output_text = "\n".join(report)
        
        # 1. Imprimir en pantalla
        print(f"\n{output_text}\n")
        
        # 2. Exportar a archivo de texto si se solicitó
        if export_file:
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(f"Bitácora de Incidente generada el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(output_text)
            print(f"[+] Éxito: Reporte exportado a '{export_file}'")
        
    except ValueError as e:
        print(f"[-] Error: Formato IP/CIDR inválido. Usa el formato x.x.x.x/y")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Herramienta de Análisis de Subredes para Respuesta a Incidentes (Blue Team)")
    parser.add_argument("-t", "--target", required=True, help="IP objetivo con su notación CIDR (ej. 172.16.0.5/23)")
    
    # Agregamos el nuevo argumento opcional para exportar
    parser.add_argument("-o", "--output", required=False, help="Nombre del archivo de texto para exportar el reporte (ej. reporte_ip.txt)")
    
    args = parser.parse_args()
    analyze_subnet(args.target, args.output)
