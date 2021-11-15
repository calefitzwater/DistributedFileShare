import socket
import os
import pickle
import math

# Global Variabes
ledgerDict = dict()

# Socket Functions


def get_available_addr():
    # Connect to hub and retrieve a list of available IP Addresses to send/retrieve data
    addresses = ['1234', '5678', '9101']
    return addresses


def store_file_in_addr(port, address, chunk, file_path):
    # Store partial file at a given address
    pass


def retrieve_file_from_addr():
    pass


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
    chunk_size = int(math.ceil(file_size.st_size/len(addr)))
    with open(filedir, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            file_path = filename + "_" + str(file_number)
            #Store in address
            store_file_in_addr(port, addr[file_number], chunk, file_path)
            # Add to ledger
            file_partition.append(
                [addr[file_number], port, file_path, file_number])
            file_number += 1
            chunk = f.read(chunk_size)

    ledgerDict[filename] = file_partition
    update_ledger()
    print(filename + " has been stored!")


# GUI
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
            pass
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
            pass
        if choice == '5':
            break
