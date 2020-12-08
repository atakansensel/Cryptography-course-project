import math
import random
import string
import warnings
import pyprimes
import sympy
import os.path
import sys
import DS

def Func(q, p, g):
  alpha = random.randint(1, q - 2)
  beta = pow(g, alpha, p)
  return alpha, beta



def gen_random_tx(q, p, g):
    serialNo = random.getrandbits(128)
    payerA, payerB = Func(q, p, g)
    payeeB = Func(q, p, g)[1]
    amount = random.randint(1, 1000000)
    Msg1 = '*** Bitcoin transaction ***'
    Msg2 = 'Serial number: ' + str(serialNo)
    Msg3 = 'Payer public key (beta): ' + str(payerB)
    Msg4 = 'Payee public key (beta): ' + str(payeeB)
    Msg5 = 'Amount: ' + str(amount)

    m = '\n'.join([Msg1, Msg2, Msg3, Msg4, Msg5])
    s, r = DS.SignGen(m.encode('UTF-8'), q, p, g, payerA)
    sMsg = 'Signature (s): ' + str(s)
    rMsg = 'Signature (r): ' + str(r)
    realMsg = '\n'.join([m, sMsg, rMsg])
    return realMsg

def gen_random_txblock(q, p, g, TxCnt, filename):
   file1= open(filename,"w+")
   for i in range(0,TxCnt):
       serialNo = random.getrandbits(128)
       payerA, payerB = Func(q, p, g)
       payeeB = Func(q, p, g)[1]
       amount = random.randint(1, 1000000)
       Msg1 = '**** Bitcoin transaction ****'
       file1.write(Msg1+"\n")
       Msg2 = 'Serial number: ' + str(serialNo)
       file1.write(Msg2 + "\n")
       Msg3 = 'Payer public key (beta): ' + str(payerB)
       file1.write(Msg3 + "\n")
       Msg4 = 'Payee public key (beta): ' + str(payeeB)
       file1.write(Msg4 + "\n")
       Msg5 = 'Amount: ' + str(amount)
       file1.write(Msg5 + "\n")
       m = '\n'.join([Msg1, Msg2, Msg3, Msg4, Msg5])
       s, r = DS.SignGen(m.encode('UTF-8'), q, p, g, payerA)
       Msg6 = 'Signature (s): ' + str(s)
       file1.write(Msg6 + "\n")
       Msg7 = 'Signature (r): ' + str(r)
       file1.write(Msg7 + "\n")




   file1.close()
