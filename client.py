import socket
import threading
import os

client_socket = socket.socket()
client_socket.connect(('localhost', 5500))

def receive(client_socket):
    try:
        data = ""
        while data != "disconnect" and data != "kill":
            data = client_socket.recv(1024).decode()
            print(f" Reçu par le serveur {data}")
        client_socket.close()
    except ConnectionAbortedError:
         print("Socket fermé")

t2 = threading.Thread(target=receive, args=[client_socket])
t2.start()

message = ""
while message != "disconnect" and message != "kill":
    message = input("\n Message à envoyer au serveur:")
    client_socket.send(message.encode())
client_socket.close()

t2.join()
client_socket.close()
