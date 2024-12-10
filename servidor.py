import socket
import threading

# Configuración del servidor
HOST = '127.0.0.1'  # Localhost
PORT = 5000         # Puerto del servidor

# Inicializar el socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
aliases = []

def broadcast(message, sender_socket=None):
    """Envía mensajes a todos los clientes excepto al remitente."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    """Maneja la comunicación con un cliente específico."""
    while True:
        try:
            message = client.recv(1024)  # Recibir mensaje
            broadcast(message, sender_socket=client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f"{alias} ha salido del chat.".encode('utf-8'))
            aliases.remove(alias)
            break

def receive_connections():
    """Acepta nuevas conexiones de clientes."""
    print("Servidor escuchando...")
    while True:
        client, address = server.accept()
        print(f"Conexión establecida con {address}")
        
        client.send("ALIAS".encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        
        print(f"El alias del cliente es {alias}")
        broadcast(f"{alias} se ha unido al chat.".encode('utf-8'))
        client.send("Conexión exitosa al servidor.".encode('utf-8'))
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
