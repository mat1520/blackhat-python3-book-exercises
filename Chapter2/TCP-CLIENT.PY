import socket

target_host = input("Enter target host (IP or domain): ")
target_port = int(input("Enter target port (e.g., 80): "))

#Crear el socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conectar al cliente
client.connect((target_host, target_port))

#Enviar algunos datos
client.send(b"GET / HTTP/1.1\r\nHost: " + target_host.encode() + b"\r\n\r\n")

#Recibir algunos datos
response = client.recv(4096)
print(response.decode())