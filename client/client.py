import socket
import threading

quitting = False
def main():
    host = "127.0.0.1"
    port = 8880
    name = input("Enter your name:")
    clientSideSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSideSocket.connect((host,port))
    clientSideSocket.send(bytes(name,"utf-8"))
    intialResponse = clientSideSocket.recv(1024).decode("utf-8")
    print(intialResponse)

    threading.Thread(target=sendMSG,args=(clientSideSocket,host,port,name)).start()
    threading.Thread(target=receiveMSG, args=(clientSideSocket, host, port, name)).start()

def sendMSG(clientSideSocket,host,port,name):
    global quitting
    activeSend = True
    while activeSend and not quitting:
        msg = input(host + "@" + name + ":")
        if msg == "quit()":
            clientSideSocket.send(bytes(msg,"utf-8"))
            quitting = True
            clientSideSocket.close()
            break
        else:
            clientSideSocket.send(bytes(msg, "utf-8"))
    print("BYE")

def receiveMSG(clientSideSocket,host,port,name):
    global quitting
    activeReceive = True
    while activeReceive and not quitting:
        try:
            input1 = clientSideSocket.recv(1024).decode("utf-8")
            print("\n")
            print(input1)
            print("\n")
            print(host+"@"+name+":")
        except:
            print("Connection Terminated")

main()


