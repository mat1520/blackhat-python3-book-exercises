import socket
import os
import struct
import sys

def obtener_interfaces():
    """
    Obtiene las interfaces de red disponibles en el sistema usando comandos del sistema.
    """
    import subprocess
    interfaces = []
    
    try:
        # Usar 'ip' command en Linux
        resultado = subprocess.run(['ip', '-4', 'addr', 'show'], 
                                  capture_output=True, text=True, check=True)
        
        iface_actual = None
        for linea in resultado.stdout.split('\n'):
            if not linea.startswith(' '):
                # Nueva interfaz
                partes = linea.split(':')
                if len(partes) >= 2:
                    iface_actual = partes[1].strip()
            elif 'inet ' in linea and iface_actual:
                # Extraer IP
                partes = linea.strip().split()
                if len(partes) >= 2:
                    ip = partes[1].split('/')[0]
                    interfaces.append((iface_actual, ip))
        
        return interfaces
    except Exception as e:
        # Fallback manual
        return None

def mostrar_interfaces():
    """
    Muestra las interfaces de red disponibles.
    """
    interfaces = obtener_interfaces()
    
    if interfaces:
        print("\n[*] Interfaces de red disponibles:")
        for iface, ip in interfaces:
            print(f"    {iface}: {ip}")
        return interfaces
    else:
        print("\n[*] No se pudieron detectar interfaces automáticamente")
        print("[*] Interfaces comunes en Linux:")
        print("    lo: 127.0.0.1 (loopback)")
        print("    eth0, enp0s3: IP de tu red local")
        print("    wlan0, wlp2s0: IP de tu WiFi")
        print("\n[*] Usa 'ip addr' para ver tus interfaces")
        return None

def parsear_cabecera_ip(datos):
    """
    Parsea la cabecera IP de los datos raw.
    """
    # Desempaquetar los primeros 20 bytes (cabecera IP básica)
    cabecera = struct.unpack('!BBHHHBBH4s4s', datos[:20])
    
    version_ihl = cabecera[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    ttl = cabecera[5]
    protocolo = cabecera[6]
    ip_origen = socket.inet_ntoa(cabecera[8])
    ip_destino = socket.inet_ntoa(cabecera[9])
    
    return {
        'version': version,
        'ttl': ttl,
        'protocolo': protocolo,
        'origen': ip_origen,
        'destino': ip_destino
    }

def obtener_protocolo(numero):
    """
    Convierte el número de protocolo a su nombre.
    """
    protocolos = {
        1: 'ICMP',
        6: 'TCP',
        17: 'UDP',
        41: 'IPv6',
        47: 'GRE',
        50: 'ESP',
        51: 'AH'
    }
    return protocolos.get(numero, f'Otro ({numero})')

def main():
    # Verificar privilegios
    if os.name != "nt" and os.geteuid() != 0:
        print("[!!] Este script requiere privilegios de root (sudo)")
        sys.exit(1)
    
    # Mostrar interfaces disponibles
    interfaces = mostrar_interfaces()
    
    print("\n[*] Para sniffing, usa una IP de TU máquina (no IPs externas)")
    host = input("[?] Ingrese la dirección IP de la interfaz a esnifar: ").strip()
    
    # Validar que la IP no esté vacía
    if not host:
        print("[!!] Debe ingresar una dirección IP válida")
        sys.exit(1)
    
    try:
        # Crear un socket raw
        if os.name == "nt":
            socket_sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            socket_sniffer.bind((host, 0))
            socket_sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            socket_sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        else:
            # En Linux, usamos IPPROTO_ICMP para simplificar
            socket_sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            socket_sniffer.bind((host, 0))
        
        print(f"\n[*] Iniciando el esnifado en {host}")
        print("[*] Esperando paquetes ICMP (prueba hacer: ping {})".format(host))
        print("[*] Presiona Ctrl+C para detener\n")
        
        contador = 0
        while True:
            # Recibir paquete
            datos, direccion = socket_sniffer.recvfrom(65565)
            
            # Parsear cabecera IP
            try:
                cabecera = parsear_cabecera_ip(datos)
                contador += 1
                
                print(f"[{contador}] Paquete capturado:")
                print(f"    Protocolo: {obtener_protocolo(cabecera['protocolo'])}")
                print(f"    Origen: {cabecera['origen']}")
                print(f"    Destino: {cabecera['destino']}")
                print(f"    TTL: {cabecera['ttl']}")
                print(f"    Tamaño: {len(datos)} bytes")
                print()
            except Exception as e:
                print(f"[!] Error al parsear paquete: {e}")
    
    except OSError as e:
        if e.errno == 99:
            print(f"\n[!!] Error: {host} no es una IP válida de tu máquina")
            print("[!!] Usa una de las IPs mostradas arriba")
        else:
            print(f"\n[!!] Error de socket: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[*] Esnifado detenido")
        print(f"[*] Total de paquetes capturados: {contador}")
        if os.name == "nt":
            socket_sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit(0)
    except Exception as e:
        print(f"\n[!!] Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()