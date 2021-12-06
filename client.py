import socket
import os
import pickle
import math

# Global Variabes
ledgerDict = dict()

# Socket Functions


def get_available_addr():
    # Connect to hub and retrieve a list of available IP Addresses to send/retrieve data
    addr = []
    host = '127.0.0.1'
    port = 9090
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cc.connect((host, 9090))
    data = 'fetch'
    cc.send(data.encode())
    res = cc.recv(1024)
    while(res.decode() != 'end'):
        addr.append(res.decode())
        print(addr)
        res = cc.recv(1024)

    cc.close()
    return addr


def store_file_in_addr(address, chunk, file_path, file_size):
    # Store partial file at a given address
    print(address)
    send_host = address
    send_port = 1010
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cc.connect((send_host, send_port))
    cc.send('store'.encode())
    res = cc.recv(1024)
    cc.send(str(file_size).encode())
    res = cc.recv(1024)
    cc.send(file_path.encode())
    res = cc.recv(1024)
    cc.send(chunk)
    cc.close()


def retrieve_file_from_addr(address):
    send_host = address[0]
    send_port = 1010
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cc.connect((send_host, send_port))
    cc.send('retrieve'.encode())
    res = cc.recv(1024)
    cc.send(address[1].encode())
    file = cc.recv(address[3])
    cc.close()
    return file


def remove_file_from_addr(address):
    send_host = address[0]
    send_port = 1010
    cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cc.connect((send_host, send_port))
    cc.send('remove'.encode())
    res = cc.recv(1024)
    cc.send(address[1].encode())
    cc.close()
# Local functions


def update_ledger():
    # Update the local file_ledger
    with open('./fileLedger.pickle', 'wb') as ledgerFile:
        pickle.dump(ledgerDict, ledgerFile)
    print('Ledger updated')


def check_ledger_files():
    # Check files that have been stored in ledger
    for num, filename in enumerate(ledgerDict.keys()):
        print(str(num+1) + ". " + filename)


def split_file_and_store(filedir, filename):
    # Split file into n partial files and store in available addresses
    file_partition = []
    port = ""
    file_path = ""
    addr = get_available_addr()
    file_number = 0
    file_size = os.stat(filedir)
    file_size = file_size.st_size
    chunk_size = int(math.ceil(file_size/len(addr)))
    with open(filedir, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            file_path = filename + "_" + str(file_number)
            #Store in address
            store_file_in_addr(addr[file_number], chunk, file_path, file_size)
            # Add to ledger
            file_partition.append(
                [addr[file_number], file_path, file_number, file_size])
            file_number += 1
            chunk = f.read(chunk_size)

    ledgerDict[filename] = file_partition
    update_ledger()
    print(filename + " has been stored!")


def retrieve_stored_file(filename):
    chunks = []
    for address in ledgerDict[filename]:
        chunks.append(retrieve_file_from_addr(address))
    with open("copy_"+filename, 'wb') as file:
        file.write(b''.join(chunks))


def remove_stored_file(filename):
    for address in ledgerDict[filename]:
        remove_file_from_addr(address)
    ledgerDict.pop(filename)
    update_ledger()


def print_menu():
    print("""
    Client Menu
    1. Check files
    2. Retrieve file
    3. Store file
    4. Delete file
    5. Exit
    """)


if __name__ == "__main__":
    # Fetch ledger
    if os.path.exists('./fileLedger.pickle'):
        with open('./fileLedger.pickle', 'rb') as ledgerFile:
            ledgerDict = pickle.load(ledgerFile)

    while(True):
        print_menu()
        choice = input()
        if choice == '1':
            check_ledger_files()
        if choice == '2':
            while(True):
                print('Enter the file name: ', end='')
                filename = input()
                if filename not in ledgerDict.keys():
                    print(
                        "%s doesn't exist! Please select a different name" % filename)
                else:
                    break
            retrieve_stored_file(filename)
        if choice == '3':
            while(True):
                print('Enter the file name: ', end='')
                filename = input()
                if filename in ledgerDict.keys():
                    print(
                        '%s already exists! Please select a different name' % filename)
                else:
                    break
            print('Enter the file dir: ', end='')
            filedir = input()
            split_file_and_store(filedir, filename)
        if choice == '4':
            while(True):
                print('Enter the file name: ', end='')
                filename = input()
                if filename not in ledgerDict.keys():
                    print(
                        "%s doesn't exist! Please select a different name" % filename)
                else:
                    break
            remove_stored_file(filename)
        if choice == '5':
            break
