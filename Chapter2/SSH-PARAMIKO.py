import threading, paramiko, subprocess

# Función para manejar la conexión SSH y ejecutar comandos
def sshComands(ip, user, passwd, command):
    try:
        # Crear un cliente SSH
        client = paramiko.SSHClient()
        
        # Esta línea evita el error de "authenticity of host" aceptando la llave automáticamente
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conectar al servidor SSH
        client.connect(ip, username=user, password=passwd)
        print(f"[+] Conectado a {ip} como {user}")
        
        # Ejecutar el comando
        stdin, stdout, stderr = client.exec_command(command)
        
        # Obtener la salida y errores
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print(f"[+] Salida del comando:\n{output}")
        if error:
            print(f"[!] Error del comando:\n{error}")
        
    except Exception as e:
        print(f"[!!] Error al conectar o ejecutar comando: {e}")
    finally:
        # Cerrar la conexión SSH
        client.close()
        print(f"[+] Conexión cerrada con {ip}")

# Ejecución con tus credenciales probadas
if __name__ == "__main__":
    input_ip = input("Ingrese la IP del servidor SSH: ")
    input_user = input("Ingrese el nombre de usuario: ")
    input_passwd = input("Ingrese la contraseña: ")
    input_command = input("Ingrese el comando a ejecutar: ")
    sshComands(input_ip, input_user, input_passwd, input_command)