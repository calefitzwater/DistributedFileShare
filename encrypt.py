import os, random, struct, pickle
from Crypto.Cipher import AES

def encrypt_file(key, filename, chunksize=64*1024):
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    store(filename, key, iv, os.path.getsize(filename))

    with open(filename, 'rb') as infile:
        with open(filename + '.enc', 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += str.encode(' ' * (16 - len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def store(filename, key, iv, filesize):
    if os.path.exists('passLedger.pickle'):
        passfile = open('passLedger.pickle', 'rb')
        ps = pickle.load(passfile)
        passfile.close()
    else:
        ps = dict()

    with open('./passLedger.pickle', 'wb') as passFile:
        ps[filename] = [key, iv, filesize]
        pickle.dump(ps, passFile)


if __name__ == "__main__":
    encrypt_file(os.urandom(16), 'testFile')