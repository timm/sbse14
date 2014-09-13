from __future__ import division
import sys
sys.dont_write_bytecode = True
from o import *
from the import *

def pretty(d, indent=0):
  for key, value in d.items():
    if key[0] != "_":
      print '    ' * indent + str(key)
      if isinstance(value, (dict,o)):
         pretty(value, indent+1)
      else:
         print '    ' * (indent+1) + str(value)

rand = random.random
any  = random.choice
def say(*lst):
  sys.stdout.write(','.join(lst))

nl="\n"

def median(lst):
  n = len(lst)
  p = n // 2
  if (n % 2):  return lst[p]
  q = p + 1
  q = max(0,(min(q,n)))
  return (lst[p] + lst[q])/2

def cmd(com="say(logo)"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  def value(x):
    try:    return eval(x)
    except: return x
  def pair(x):
    lst = re.split("=",x)
    return lst[0] +"="+ wrap(value(lst[1]))
  words = map(pair, sys.argv[2:])
  return sys.argv[1]+'(**dict('+ ','.join(words)+'))'


