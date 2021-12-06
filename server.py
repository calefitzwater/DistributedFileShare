import socket
import os


def sendToHub(msg):
    send_host = '127.0.0.1'
    send_port = 9090
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cc.connect((send_host, send_port))
    data = msg
    cc.send(data.encode())
    res = cc.recv(1024)
    print(res.decode())
    cc.close()


sendToHub('add')
host = ''
port = 1010
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((host, port))
ss.listen()
while(True):
    (c, addr) = ss.accept()
    print("%s(%s) has connected." %
          (addr[0], addr[1]))
    req = c.recv(1024)
    req = req.decode()
    if(req == 'store'):
        c.send('accepted'.encode())
        file_size = c.recv(1024)
        file_size = int(file_size.decode())
        c.send('accepted'.encode())
        name = c.recv(1024)
        name = name.decode()
        c.send('accepted'.encode())
        data = c.recv(file_size)
        with open(name, 'wb') as file:
            file.write(data)
    if(req == 'remove'):
        c.send('accepted'.encode())
        name = c.recv(1024)
        name = name.decode()
        os.remove(name)
    if (req == 'retrieve'):
        c.send('accepted'.encode())
        name = c.recv(1024)
        print(1)
        name = name.decode()
        print(2)
        with open(name, 'rb') as file:
            c.send(file.read())

ss.close()
sendToHub('remove')
