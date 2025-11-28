#!/usr/bin/env python3
"""
Script de prueba para generar tráfico de email que el sniffer pueda capturar.
Simula una conexión POP3 o SMTP en texto plano.
"""

import socket
import sys

def test_pop3(servidor="mail.example.com", puerto=110):
    """
    Simula una conexión POP3 para probar el sniffer.
    """
    try:
        print(f"[*] Intentando conectar a {servidor}:{puerto} (POP3)")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((servidor, puerto))
        
        # Recibir banner del servidor
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # Enviar comando USER (esto es lo que el sniffer capturará)
        usuario = "testuser@example.com"
        sock.send(f"USER {usuario}\r\n".encode())
        print(f"[>] USER {usuario}")
        
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # Enviar comando PASS (esto también será capturado)
        password = "testpassword123"
        sock.send(f"PASS {password}\r\n".encode())
        print(f"[>] PASS {password}")
        
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # Cerrar conexión
        sock.send(b"QUIT\r\n")
        sock.close()
        
        print("\n[*] Conexión cerrada")
        print("[*] El sniffer debería haber capturado USER y PASS")
        
    except socket.timeout:
        print("[!] Timeout - El servidor no respondió")
    except ConnectionRefusedError:
        print("[!] Conexión rechazada - El servidor no está escuchando en ese puerto")
    except Exception as e:
        print(f"[!] Error: {e}")

def test_smtp(servidor="mail.example.com", puerto=25):
    """
    Simula una conexión SMTP para probar el sniffer.
    """
    try:
        print(f"[*] Intentando conectar a {servidor}:{puerto} (SMTP)")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((servidor, puerto))
        
        # Recibir banner del servidor
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # HELO
        sock.send(b"HELO test.com\r\n")
        print("[>] HELO test.com")
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # MAIL FROM (esto será capturado)
        sock.send(b"MAIL FROM:<sender@test.com>\r\n")
        print("[>] MAIL FROM:<sender@test.com>")
        respuesta = sock.recv(1024)
        print(f"[<] {respuesta.decode('utf-8', errors='ignore').strip()}")
        
        # QUIT
        sock.send(b"QUIT\r\n")
        sock.close()
        
        print("\n[*] Conexión cerrada")
        print("[*] El sniffer debería haber capturado MAIL FROM")
        
    except socket.timeout:
        print("[!] Timeout - El servidor no respondió")
    except ConnectionRefusedError:
        print("[!] Conexión rechazada - El servidor no está escuchando en ese puerto")
    except Exception as e:
        print(f"[!] Error: {e}")

def main():
    print("=" * 60)
    print("Script de Prueba para Mail Sniffer")
    print("=" * 60)
    print("\n[!] IMPORTANTE: Ejecuta el mail_sniffer.py en otra terminal primero:")
    print("    sudo venv/bin/python3 mail_sniffer.py\n")
    
    print("Opciones de prueba:")
    print("1. Probar con servidor POP3 público (puede no funcionar)")
    print("2. Probar con servidor SMTP público (puede no funcionar)")
    print("3. Servidor personalizado")
    print("4. Usar servidor de prueba local (requiere configuración)")
    
    opcion = input("\nSelecciona una opción (1-4): ").strip()
    
    if opcion == "1":
        # Intentar con un servidor POP3 público
        servidor = input("Servidor POP3 (ej: pop.gmail.com): ").strip() or "pop.gmail.com"
        test_pop3(servidor, 110)
    elif opcion == "2":
        # Intentar con un servidor SMTP público
        servidor = input("Servidor SMTP (ej: smtp.gmail.com): ").strip() or "smtp.gmail.com"
        test_smtp(servidor, 25)
    elif opcion == "3":
        servidor = input("Servidor: ").strip()
        puerto = int(input("Puerto: ").strip())
        protocolo = input("Protocolo (pop3/smtp): ").strip().lower()
        
        if protocolo == "pop3":
            test_pop3(servidor, puerto)
        else:
            test_smtp(servidor, puerto)
    elif opcion == "4":
        print("\n[*] Para configurar un servidor de prueba local:")
        print("    1. Instala: sudo apt install dovecot-pop3d")
        print("    2. Configura en /etc/dovecot/dovecot.conf:")
        print("       disable_plaintext_auth = no")
        print("    3. Reinicia: sudo systemctl restart dovecot")
        print("    4. Prueba con: localhost puerto 110")
    else:
        print("[!] Opción inválida")

if __name__ == "__main__":
    main()
