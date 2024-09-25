import socket
import threading

# List to keep track of connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, current_client):
    for client in clients:
        if client != current_client:  # Don't send the message back to the sender
            try:
                client.sendall(message)
            except:
                clients.remove(client)  # Remove client if sending fails

# Function to handle individual client connections
def handle_client(client_socket, address):
    print(f"New connection from {address}")
    clients.append(client_socket)

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if not message:
                break
            # Broadcast the message to all other clients
            broadcast(message, client_socket)
        except:
            break

    # Remove client if the connection is closed
    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection from {address} closed")

# Main function to set up the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))  # Bind to localhost and port 5555
    server.listen()

    print("Server is listening for connections...")

    while True:
        # Accept incoming client connections
        client_socket, address = server.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if _name_ == "_main_":
    main()
