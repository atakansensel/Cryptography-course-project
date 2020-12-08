import random
import sys
from ecpy.curves import Curve
from Crypto.Hash import SHA3_256

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


def KeyGen(curve):
    n = curve.order
    P = curve.generator
    sA = random.randint(2,n-1)
    QA = sA * P
    return sA,QA

def SignVer(message, s, r, E, QA):
    
    h = SHA3_256.new(message).digest()
    h_num = int.from_bytes(h, byteorder = 'big')
    n = E.order
    P = E.generator

    v = modinv(h_num,n)
    z1 = (v * s)% n
    z2 = (v * r)% n

    z1 = n - z1 # -z1
    u = ((z1 * P) + (z2 * QA)).x % n
    if u == r%n:
        return 0
    else:
        return 1


def SignGen(message, E, sA):
        n = E.order
        P = E.generator
        h = SHA3_256.new(message).digest()
        h = int.from_bytes(h, "big") % n
        k = random.randint(1, n - 2)
        r = (k * P)
        r = (r.x) % n
        s = ((sA * r) - (k * h)) % n
        return (s, r)



