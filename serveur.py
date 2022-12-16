import socket
import threading
import os
import sys
import subprocess
import platform
import psutil

host = 'localhost'
if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    port = 50

def Serveur(data):
    if sys.platform == 'win32':
        commande = data.split(' ')[0]
        if commande == "ram":
            rep = str(f'RAM utilisé :{psutil.virtual_memory().percent}% \nMémoire vive Total :{psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB \nMémoire libre restante :{psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB')
            conn.send(rep.encode())
            print("Information de la ram envoyé au client")

        elif commande == "cpu":
            rep = str(f'{psutil.cpu_percent()}% du CPU utilisé.')
            conn.send(rep.encode())
            print("Information du CPU envoyé au client")

        elif commande == "ping":
            rep = subprocess.getoutput(data)
            conn.send(rep.encode())
            print(f"ping")

        elif data == "ip":
            hostname = socket.gethostname()
            rep = str(f"{socket.gethostbyname(hostname)}")
            conn.send(rep.encode())
            print("ip envoyé au client")

        elif data == "os":
            rep = platform.platform()
            conn.send(rep.encode())
            print("Information sur l'os envoyé au client")

        elif data == "name":
             rep = socket.gethostname()
             conn.send(rep.encode())
             print("hostname envoyé")

        elif data == "python --version":
             rep = str(subprocess.check_output('python --version', shell=True))
             output = rep.replace('b', '').replace('\\r', "").replace('\\n', "")
             conn.send(output.encode())
             print("Version de python envoyé")


        elif data[0:4].lower() == 'dos:':
            try:
                cmd = data.split(':', 1)[1]
                output = subprocess.getoutput(cmd)
                conn.send(output.encode())
            except:
                conn.send(f'erreur avec la commande : {data}'.encode())

        elif data[0:11].lower() == 'powershell:':
            try:
                cmd = data.split(":", 1)[1]
                output = subprocess.getoutput('PowerShell -command "' + cmd + '"')
                conn.send(output.encode())
            except:
                conn.send(f'erreur avec la commande : {data}'.encode())
        else:
            conn.send('COMMANDE NON RECONNUE!!!'.encode())

    if data[0:6].lower() == 'linux:':
        if sys.platform == "linux" or sys.platform == "linux2":
                try:
                    cmd = data.split(":", 1)[1]
                    output = subprocess.getoutput(cmd)
                    conn.send(output.encode())
                except:
                    conn.send(f'erreur avec la commande : {data} / Essayer avec une commande Linux précédé par <linux'.encode())
        else:
            conn.send('COMMANDE NON RECONNUE!!!'.encode())

data = ""
try:
    print("serveur en attente")
    while data != "kill":
        serv_socket = socket.socket()
        serv_socket.bind((host, port))
        serv_socket.listen(5)
        data = ''
        while data != "reset" and data != 'kill':
                conn, address = serv_socket.accept()
                data = ''
                print("client connecté")
                while data != "disconnect" and data != 'kill' and data != 'reset':
                    try:
                        data = conn.recv(1024).decode().lower()
                        Serveur(data)
                    except:
                        pass
                try:
                    conn.send("DISCONNECT".encode())
                    print("deconnexion du client")
                except:
                    pass
                conn.close()
        serv_socket.close()
except ConnectionResetError:
    print("")
