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