import socket, threading

bind_ip = "0.0.0.0"

bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print(f"[*] Listening on {bind_ip}:{bind_port}")

def handle_client(client_socket):
    with client_socket:
        print(f"[*] Accepted connection from {client_socket.getpeername()}")
        client_socket.send(b"Hello! You are connected to the server.\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[*] Received: {data}")
            client_socket.send(data)
        print(f"[*] Connection closed from {client_socket.getpeername()}")
while True:
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()