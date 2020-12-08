import math
import random
import string
import warnings
import sympy
import DS  # This is the file from Phase I
import Tx  # This is the first file you have to submit in the second phase
import os.path
import sys

from Crypto.Hash import SHA3_256


def MerkleTreeHash(Hash):
    newValues = []
    for i in range(0, int(len(Hash)/2)):
        Hash2 = (Hash[2*i]) + (Hash[(2*i)+1])
        hashed = SHA3_256.new(Hash2).digest()
        newValues.append(hashed)
    return newValues




def CheckPow(p, q, g, powLen, TxCnt, filename):
    Hr, nonce = findHR(TxCnt, filename)
    newHash = Hr + str(nonce).encode('UTF-8')
    proof = SHA3_256.new(newHash).hexdigest()
    return proof


def PoW(powLen, q, p, g, TxCnt, filename):

    check = True
    rootHash = findHR(TxCnt, filename)[0]
    while check:
        nonce = random.getrandbits(128)
        newHash = rootHash + (str(nonce) + '\n').encode("UTF-8")
        hashed = SHA3_256.new(newHash).hexdigest()
        if hashed[0:powLen] == "0" * powLen:
            check= False

    f1 = open(str(filename), "r")
    trans = f1.readlines()
    f1.close()
    trans.append("Nonce: " + str(nonce) + "\n")
    msg = ""
    for i in trans:
        msg+=i
    return msg


def findHR(TxCnt, filename):
    f = open(str(filename), "r")

    T = []
    for i in range(0, TxCnt):
        msg1 = f.readline()
        msg2 = f.readline()
        msg3 = f.readline()
        msg4 = f.readline()
        msg5 = f.readline()
        msg6 = f.readline()
        msg7 = f.readline()
        m = ''.join([msg1, msg2, msg3, msg4, msg5, msg6, msg7])

        shake = SHA3_256.new(m.encode("UTF-8"))
        T.append(shake.digest())
    nonce = f.readline()
    nonce = nonce[7:len(nonce)]
    f.close()

    while(len(T)>1):
        T=MerkleTreeHash(T)

    root = T[0]
    #print(rootHash)
    return root, nonce




