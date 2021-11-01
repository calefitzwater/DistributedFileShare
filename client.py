import socket
import os
import pickle
import math


ledgerDict = dict()
availableAddr = []
storeDir = ""


def get_available_addresses():
    return [1234, 5678, 9101]


def update_ledger():
    with open('./fileLedger.pickle', 'wb') as ledgerFile:
        pickle.dump(ledgerDict, ledgerFile)
    print(ledgerDict)


def check_files():
    for num, filename in enumerate(ledgerDict.keys()):
        print(num + ". " + filename)


def store_socket(file, chunk):
    file.write(chunk)


def store_file(filedir, filename):
    port = ""
    path = ""
    file_partition = []
    addresses = get_available_addresses()
    file_size = os.stat(filedir)
    chunk_size = int(math.ceil(file_size.st_size/len(addresses)))
    file_number = 0
    with open(filedir, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            with open(filename + "_" + str(file_number), 'wb') as chunk_file:
                store_socket(chunk_file, chunk)
                file_partition.append(
                    [addresses[file_number], port, path, file_number])
            file_number += 1
            chunk = f.read(chunk_size)

    # Ledger
    ledgerDict[filename] = file_partition
    update_ledger()
    print(filename + " has been stored!")


def retrieve_file(filedir):
    pass


def remove_file(filedir):
    pass


if __name__ == "__main__":
    if os.path.exists('./fileLedger.pickle'):
        with open('./fileLedger.pickle', 'rb') as ledgerFile:
            ledgerDict = pickle.load(ledgerFile)

    store_file("C:/Users/stefa/Desktop/corgi.jpg", "corgi")
