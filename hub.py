import socket
import os

available_addr = set()
host = ''
port = 9090
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind((host, port))
ss.listen()


def add_server(ip):
    available_addr.add(ip)
# Remove server


def remove_server(ip):
    available_addr.remove(ip)
# Retrieve available servers


def fetch_servers():
    pass


while(True):
    (c, addr) = ss.accept()
    print("%s(%s) has connected." %
          (addr[0], addr[1]))
    req = c.recv(1024)
    req = req.decode()
    if(req == 'add'):
        add_server(addr[0])
        res = "%s added" % (addr[0])
        c.send(res.encode())
    elif(req == 'remove'):
        remove_server(addr[0])
        res = "%s removed" % (addr[0])
        c.send(res.encode())
    elif(req == 'fetch'):
        for ip in list(available_addr):
            c.send(ip.encode())
        c.send('end'.encode())

    print(available_addr)
