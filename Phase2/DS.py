import math
import random
import string
import warnings
import pyprimes
import os.path
import sys
import pathlib
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

def egcd(a, b):
  x,y, u,v = 0,1, 1,0
  while a != 0:
    q, r = b//a, b%a
    m, n = x-u*q, y-v*q
    b,a, x,y, u,v = a,r, u,v, m,n
  gcd = b
  return gcd, x, y

def modinv(a, m):
  if a < 0:
    a = a+m
  gcd, x, y = egcd(a, m)
  if gcd != 1:
    return None
  else:
    return x % m

def random_prime(bitsize):
  warnings.simplefilter('ignore')
  chck = False
  while chck == False:
    p = random.randrange(2**(bitsize-1), 2**(bitsize)-1)
    chck = pyprimes.isprime(p)
  warnings.simplefilter('default')
  return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        chck = pyprimes.isprime(p)
    warnings.simplefilter('default')
    return p

def GenerateOrRead(fileName):

   try:
    f = open(fileName, "r")
    q = int(f.readline())
    p = int(f.readline())
    g = int(f.readline())
    f.close()
    return q, p, g
   except:
    (q, p, g) = Param_Gen(224, 2048)
    file = open("pubparams", "w")
    file.write(str(q) + '\n')

    file.write(str(p) + '\n')
    file.write(str(g) + '\n')
    file.close()
    return q, p, g

def random_string(stringLength):
  letters = string.ascii_lowercase
  rand_str = ''
  for i in range(stringLength):
    rand_str.join(random.choice(letters))
  return rand_str

def Param_Gen(qbit, pbit):
    q = random_prime(qbit)
    p = large_DL_Prime(q, pbit - qbit)
    tmp = (p - 1) // q
    if p.bit_length() != 2048:
        return Param_Gen(qbit, pbit)
    else:
        g = 1
        while g == 1:
            alpha = random.randrange(1, p)
            g = pow(alpha, tmp, p)
        return q, p, g



def KeyGen(q, p, g):
  a = random.randint(1, q - 2)
  b = pow(g, a, p)

  return a, b


def SignGen(message, q, p, g, a):

  hash = SHA3_256.new(message)

  h = int.from_bytes(hash.digest(), byteorder='big')
  k = random.randint(1, q - 2)
  r = pow(g, k, p) % q
  s = ((a * r) - (k * h)) % q
  return s, r

def SignVer(message, s, r, q, p, g, beta):
  shake = SHA3_256.new(message)
  h = int.from_bytes(shake.digest(), byteorder='big')
  v = modinv(h, q)
  z1 = (s * v) % q
  z2 = (r * v) % q
  a = pow(g, z1, p)
  b= pow(beta, z2, p)
  u = ( (a * b) %p) % q

  if u == r:
    return True
  else:
    return False