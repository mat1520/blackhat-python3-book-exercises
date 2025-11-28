import sys
import socket
import threading

# Función para mostrar un volcado hexadecimal
def volcado_hexadecimal(origen, longitud=16):
    """
    Genera un volcado hexadecimal de los datos proporcionados.
    Muestra el desplazamiento, los valores hexadecimales y los caracteres ASCII.
    """
    resultado = []
    ancho_offset = 4  # Ancho del desplazamiento en hexadecimal

    if isinstance(origen, bytes):
        for i in range(0, len(origen), longitud):
            segmento = origen[i:i+longitud]
            hexadecimales = " ".join(f"{x:02X}" for x in segmento)
            ascii_texto = "".join(chr(x) if 0x20 <= x < 0x7F else "." for x in segmento)
            resultado.append(f"{i:04X}  {hexadecimales:<{longitud*3}}  {ascii_texto}")

    print("\n".join(resultado))


# Función para recibir datos de un socket
def recibir_datos(conexion):
    """
    Recibe datos de un socket hasta que no haya más disponibles o se alcance un tiempo de espera.
    """
    buffer = b""
    conexion.settimeout(2)

    try:
        while True:
            datos = conexion.recv(4096)
            if not datos:
                break
            buffer += datos
    except socket.timeout:
        pass

    return buffer


# Función para modificar solicitudes (si es necesario)
def procesar_solicitud(buffer):
    """
    Permite modificar las solicitudes antes de enviarlas al servidor remoto.
    """
    return buffer


# Función para modificar respuestas (si es necesario)
def procesar_respuesta(buffer):
    """
    Permite modificar las respuestas antes de enviarlas al cliente local.
    """
    return buffer


# Función principal para manejar la comunicación entre cliente y servidor remoto
def manejar_proxy(socket_cliente, servidor_remoto, puerto_remoto, recibir_primero):
    """
    Gestiona la comunicación entre el cliente local y el servidor remoto.
    """
    # Conexión al servidor remoto
    socket_remoto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_remoto.connect((servidor_remoto, puerto_remoto))

    # Si se debe recibir datos primero del servidor remoto
    if recibir_primero:
        buffer_remoto = recibir_datos(socket_remoto)
        if buffer_remoto:
            print("[<==] Datos recibidos del servidor remoto:")
            volcado_hexadecimal(buffer_remoto)

            # Procesar la respuesta antes de enviarla al cliente
            buffer_remoto = procesar_respuesta(buffer_remoto)
            socket_cliente.send(buffer_remoto)

    while True:
        # Recibir datos del cliente local
        buffer_local = recibir_datos(socket_cliente)
        if buffer_local:
            print(f"[==>] Recibidos {len(buffer_local)} bytes del cliente local")
            volcado_hexadecimal(buffer_local)

            # Procesar la solicitud antes de enviarla al servidor remoto
            buffer_local = procesar_solicitud(buffer_local)
            socket_remoto.send(buffer_local)
            print("[==>] Enviados al servidor remoto")

        # Recibir datos del servidor remoto
        buffer_remoto = recibir_datos(socket_remoto)
        if buffer_remoto:
            print(f"[<==] Recibidos {len(buffer_remoto)} bytes del servidor remoto")
            volcado_hexadecimal(buffer_remoto)

            # Procesar la respuesta antes de enviarla al cliente local
            buffer_remoto = procesar_respuesta(buffer_remoto)
            socket_cliente.send(buffer_remoto)
            print("[<==] Enviados al cliente local")

        # Cerrar conexiones si no hay más datos
        if not buffer_local or not buffer_remoto:
            socket_cliente.close()
            socket_remoto.close()
            print("[*] No hay más datos. Conexiones cerradas.")
            break


# Función para iniciar el servidor proxy
def iniciar_servidor(host_local, puerto_local, host_remoto, puerto_remoto, recibir_primero):
    """
    Configura un servidor que escucha conexiones y las redirige al servidor remoto.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        servidor.bind((host_local, puerto_local))
    except socket.error as error:
        print(f"[!!] Error al enlazar {host_local}:{puerto_local}")
        print(f"[!!] Verifica que el puerto no esté en uso.")
        print(f"Error: {error}")
        sys.exit(1)

    print(f"[*] Escuchando en {host_local}:{puerto_local}")
    servidor.listen(5)

    while True:
        cliente, direccion = servidor.accept()
        print(f"[==>] Conexión entrante desde {direccion[0]}:{direccion[1]}")

        # Crear un hilo para manejar la conexión
        hilo_proxy = threading.Thread(target=manejar_proxy, args=(cliente, host_remoto, puerto_remoto, recibir_primero))
        hilo_proxy.start()


# Función principal
def main():
    """
    Punto de entrada principal para configurar y ejecutar el proxy.
    """
    if len(sys.argv[1:]) != 5:
        print("Uso: ./tcp_proxy.py [host_local] [puerto_local] [host_remoto] [puerto_remoto] [recibir_primero]")
        print("Ejemplo: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(1)

    # Asignar argumentos de línea de comandos
    host_local = sys.argv[1]
    puerto_local = int(sys.argv[2])
    host_remoto = sys.argv[3]
    puerto_remoto = int(sys.argv[4])
    recibir_primero = sys.argv[5].lower() == "true"

    # Iniciar el servidor
    iniciar_servidor(host_local, puerto_local, host_remoto, puerto_remoto, recibir_primero)


if __name__ == "__main__":
    main()