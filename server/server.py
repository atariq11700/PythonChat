import socket
import threading
import time
import queue
import random
import select

socNumber = []
threadNameDict = {}
def connections():
    host = "127.0.0.1"
    port = 8880
    serverSoc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSoc.bind((host,port))
    serverSoc.listen(4)
    count = 0
    while True:
        print("Waiting for connection")
        clientSocket, clientAddress = serverSoc.accept()
        clientIp , clientPort = str(clientAddress[0]),str(clientAddress[1])
        print("Received connection from IP:",clientIp,"on port:",clientPort)
        count = len(socNumber)
        socNumber.append(Client(clientSocket,clientAddress,clientIp,clientPort))
        print(socNumber)
        print(type(socNumber[0]))
        socNumber[count].start()



class Client(threading.Thread):
    def __init__(self,cSocket,cAddress,cIp,cPort):
        threading.Thread.__init__(self)
        self.isActive = True
        self._cSocket = cSocket
        self.cAddress = cAddress
        self._cIp = cIp
        self._cPort = cPort
        self.maxBuffer = 1024
        self.name = ""

    def run(self):
        self.clientSocketThread()


    def clientSocketThread(self):
        self.name = self._cSocket.recv(1024).decode("utf-8")
        threadNameDict[threading.get_ident()] = str(self.name)
        self._cSocket.send(bytes("Connected to host","utf-8"))

        quitByMsg = False
        while self.isActive == True:
            try:
                input1 = self.receiveInput()
                if input1 == "quit()":
                    print("Closing socket")
                    print("Terminated by quit command by user")
                    quitByMsg = True
                    for x in range(len(socNumber)):
                        if socNumber[x]._cSocket == self._cSocket:
                            socNumber.pop(x)

                    self._cSocket.close()
                    break

                else:
                    print(self.name, "says", input1)
            except:
                print("In thread", threadNameDict[threading.get_ident()], "socket/connection terminated")
                self._cSocket.close()
                break

            try:
                for clients in range(len(socNumber)):
                    if socNumber[clients]._cSocket != self._cSocket:
                        socNumber[clients]._cSocket.send(bytes(self.name + " says " + input1,"utf-8"))
            except:
                print("yeah no")

        if quitByMsg == False:
            self._cSocket.close()


    def receiveInput(self):
        connectionInput = self._cSocket.recv(self.maxBuffer).decode("utf-8")
        return connectionInput

connections()
