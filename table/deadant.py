from __future__ import division
import re,sys,random
sys.dont_write_bytecode = True
from lib import *
from table import *


class Close():
  big, tiny = 20, 0.05
  def __init__(i):
    i.sum, i.n = [0.0]*32, [0.0]*32
  def keep(i,x):
    for j in xrange(len(i.sum)):
      i.sum[j] += x
      i.n[j]   += 1
      mu        = i.sum[j] / i.n[j]
      here      = i.n[j]  / i.n[0]
      if i.n[j] < Close.big  : return False
      if here   < Close.tiny : return True
      if x > mu              : return False 

def _close():
  import random
  rand=random.random
  c=Close()
  for _ in xrange(1000):
    c.keep(rand())
  n=10000
  lst = [1.0 for _ in xrange(n) 
         if c.keep(rand())]
  print sum(lst)/n



print nasa93().any()
print "why the ignored filled in"


if __name__ == '__main__': eval(cmd())
