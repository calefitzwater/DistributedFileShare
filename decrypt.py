import os, random, struct, pickle
from Crypto.Cipher import AES

def decrypt_file(in_filename, chunksize=24*1024):
    ps = load(in_filename)

    with open(in_filename + ".enc", 'rb') as infile:
        iv = ps[1]
        decryptor = AES.new(ps[0], AES.MODE_CBC, iv)

        with open(in_filename + ".dec", 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(ps[2])

def load(in_filename):
    passfile = open('passLedger.pickle', 'rb')
    return pickle.load(passfile).get(in_filename)

if __name__ == "__main__":
    decrypt_file('testFile')