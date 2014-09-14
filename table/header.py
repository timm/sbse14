from __future__ import division
import re,sys,random
sys.dont_write_bytecode = True
from lib import *
from cache import *

def Skip(x):
  x.skip=True
  return x

Ako={}

class Header(o): 
  id=0
  def __init__(i,name=None,w=1):
    if not name:
      id   = Header.id = Header.id + 1
      name = 'var%s' % id
    i.skip, i.name, i.w  = False, name,w
    i._report = None
  def __repr__(i): 
    return  i.__class__.__name__+'('+i.name+')'
  def has(i):
    if i._report == None: i._report = i.report()
    return i._report

class Ignore(Header):
  Ako["?"] = lambda:Ignore
  def ako(i): return []
  def __init__(i, name=None,*dull):
     super(Ignore,i).__init__(name=name)
     i.skip = True
  def log(i,x):
    return x

class Num(Header): 
  Ako["$"] = lambda:Num
  def ako(i): return ['nums','indep']
  def __init__(i, name=None,lo=-10**32,hi=10**32):
     super(Num,i).__init__(name=name)
     i.cache = Cache()
     i.lo, i.hi = lo,hi
  def illegal(i,x):
    return not i.lo <= x <= i.hi
  def log(i,x):
    if i.skip : return x
    if dull(x): return x
    x=float(x)
    if The.misc.nervous and i.illegal(x):
      print "# num [%s] not in range (%s,%s)" \
             % (x,i.lo,i.hi)
      exit()
    i.cache += x
    return x
  def any(i)      : return i.cache.any()
  def has(i)      : return i.cache.has()
  def norm(i,x)   : return i.cache.norm(x)
  def dist(i,x,y) : return (x-y)**2
  def far(i,x)    : return x if x > 0.5 else 1 - x
  
class Less(Num):
  Ako["<"] = lambda:Less
  def ako(i): 
    return ['nums','less','depen']

class More(Num):
  Ako[">"] = lambda:More
  def ako(i): 
    return ['nums','more','depen']
 
class Sym(Header):
  Ako["+"] = lambda:Sym
  def __init__(i,name=None,items=[]):
    super(Sym,i).__init__(name=name)
    i.m, i.n,i.counts,i.most,i.mode=0, 0,{},0,None
    i._report=None
    i.items=items
  def clone(i):
    return Sym(name=i.name,items=i.items)
  def norm(i,x): return x
  def ako(i): return ['syms','indep']
  def far(i,x):
    return "SomeCRAZYsyMbOL"
  def dist(i,x,y): 
    return 0 if x==y else 1
  def illegal(i,x):
    return  i.items and not x in i.items
  def log(i,x):
    if i.skip: return x
    if dull(x): return x
    if The.misc.nervous and i.illegal(x):
      print "# sym %s not in %s" % (x,i.items)
      exit()
    i.n += 1
    n= i.counts[x] = i.counts.get(x,0) + 1
    if n > i.most:
      i.most, i.mode = n, x
    if i.n > i.m * The.cache.update:
      i.m = i.n
      i._report = None
    return x
  def any(i):
    r,tmp = rand(),0
    for w,k in i.has().dist:
      tmp += w
      if tmp >= r : return k
    return k
  def report(i):
    lst = [(v/i.n,k) for k,v in i.counts.items()]
    return o(dist=sorted(lst,reverse=True))
    
class Klass(Sym):
  Ako["="] = lambda:Klass
  def ako(i): return ['syms','depen']

def dull(x):
  return x == None or x == The.misc.missing

if __name__ == '__main__': eval(cmd())

