import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication
import csv
import threading
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.resize(450,400)
        self.__connection_active = False
        self.client_socket = None

        self.__ip = QLineEdit("")
        self.__ip.setPlaceholderText("Entrez l'adresse IP de votre serveur")
        self.__port = QLineEdit("")
        self.__port.setPlaceholderText("Entrez le Port")
        self.__commande = QLineEdit("")
        self.__commande.setPlaceholderText("Entrez une commande")
        self.__connection = QPushButton('Connect')
        self.__connection.clicked.connect(self.__connect)
        self.__ip.returnPressed.connect(self.__connect)
        self.__port.returnPressed.connect(self.__connect)
        self.__send = QPushButton('Send')
        self.__send.clicked.connect(self.envoi)
        self.__cmd = QLabel('')
        self.affichage = QTextEdit(self)
        self.affichage.setReadOnly(True)
        self.__csv = QLabel('')
        self.__connection.clicked.connect(self.__fichier)

        grid.addWidget(self.__ip, 0, 1)
        grid.addWidget(self.__port, 0, 2)
        grid.addWidget(self.__connection, 0, 3)
        grid.addWidget(self.__cmd, 4, 1)
        grid.addWidget(self.affichage, 5,1,1,5)
        grid.addWidget(self.__commande, 3, 1)
        grid.addWidget(self.__send, 3, 2)


    def __connect(self):
        try:
            if not self.__connection_active:
                host = self.__ip.text()
                port = int(self.__port.text())
                self.client_socket = socket.socket()
                self.client_socket.connect((host, port))
                self.affichage.append(f"Vous êtes dès à présent connecté à {host} port : {port}")
                self.__connection_active = True
                self.ecoute_thread = threading.Thread(target=self.ecoute)
                self.ecoute_thread.start()
            else:
                self.affichage.append("Veuillez d'abbord vous déconnecter du server avant de lancer une nouvelle connection!")
        except:
            self.affichage.append(f'Erreur lors de la connection vers le server!!!')

    def envoi(self):
        commande = self.__commande.text()
        if len(commande) > 0:
            self.__commande.setText('')
            self.client_socket.send(commande.encode())

    def ecoute(self):
        while self.__connection_active:
            try:
                data = self.client_socket.recv(1024).decode()
                self.affichage.append(f"{data}")
                if data == 'DISCONNECT':
                    self.__connection_active = False
                    self.client_socket.close()
                    self.affichage.append(f'Déconnecté du serveur')
            except:
                self.affichage.append(f'erreur au niveau de la connection!!!')

    def __fichier(self):
        self.__csv.setText(f"{self.__ip.text()}, {self.__port.text()}")
        serv = ['Ip du serveur ' , 'Port']
        data = [f" {self.__ip.text()}, {self.__port.text()}"]
        with open('machine.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(serv)
            writer.writerow(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
