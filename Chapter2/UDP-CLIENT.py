import socket

target_host = input("Enter target host (IP or domain): ")
target_port = int(input("Enter target port (e.g., 80): "))

# Crear el objeto socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar algunos datos
client.sendto(b"Hello, UDP Server!", (target_host, target_port))

# Recibir algunos datos
response, addr = client.recvfrom(4096)
print(response.decode())