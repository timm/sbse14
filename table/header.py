from __future__ import division
import re,sys,random
sys.dont_write_bytecode = True
from lib import *

def Skip(x):
  x.skip=True
  return x


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

class Num(Header): 
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
    if i.illegal(x):
      print "# num [%s] not in range (%s,%s)" \
             % (x,i.lo,i.hi)
      exit()
    i.cache += x
    return x
  def any(i): return i.cache.any()
  def has(i): return i.cache.has()

class Less(Num):
  def ako(i): return ['nums','less','depen']
class More(Num):
  def ako(i): return ['nums','more','depen']
 

class Sym(Header):
  def __init__(i,name=None,items=[]):
    super(Sym,i).__init__(name=name)
    i.m, i.n,i.counts,i.most,i.mode=0, 0,{},0,None
    i._report=None
    i.items=items
  def clone(i):
    return Sym(name=i.name,items=i.items)
  def ako(i): return ['syms','indep']
  def log(i,x):
    if i.skip: return x
    if dull(x): return x
    if not x in i.items:
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
  def ako(i): return ['syms','depen']

def dull(x):
  return x == None or x == The.misc.missing

class Cache():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[]):
    i._lst,i.m, i.n,i._report = [],0,0,None
    map(i.__iadd__,inits)
  def __iadd__(i,x): 
    if dull(x): return x
    i.n += 1
    changed = False
    if len(i._lst) < The.cache.keep: # not full
      changed = True
      i._lst += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._lst[int(rand()*The.cache.keep)] = x
    if changed:   
      if i.n > i.m * The.cache.update:
        i._report = None
        i.m = i.n
    return i
  def any(i):  
    return  any(i._lst)
  def has(i):
    if i._report == None: i._report = i.report()
    return i._report
  def norm(i,x):
    lo, hi = i.has().lo, i.has().hi
    return (x - lo) / (hi - lo + 0.00001)
  def report():
    i._lst = sorted(i._lst)
    n   = len(lst)     
    return o(
      median= median(i._lst),
      iqr = i._lst[int(n*.75)] - i._lst[int(n*.5)],
      lo  = i._lst[0], 
      hi  = i._lst[-1])

