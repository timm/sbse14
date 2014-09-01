"""

## Log Stuff

"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True
"""

### "Log"-ging

This is a little advanced.

"""
class Log():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],label=''):
    i.label = label
    i._cache,i.n,i._report = [],0,None
    i.setup()
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    if x == None: return x
    i.n += 1
    changed = False
    if len(i._cache) < The.cache.keep:
      changed = True
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._cache[int(rand()*The.cache.keep)] = x
    if changed:      
      i._report = None # wipe out 'what follows'
      i.change(x)
    return i
  def any(i):  
    return  any(i._cache)
  def has(i):
    i._report = i._report or i.report()
    return i._report
  def setup(i): pass
"""

### Num

A _Num_ is a _Log_ for numbers.

"""
class Num(Log):
  def setup(i):
    i.lo, i.hi = 10**32, -10**32
  def change(i,x):
    i.lo = min(i.lo, x)
    i.hi = max(i.hi, x)
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 0.000001)
  def report(i):
    lst = i._cache = sorted(i._cache)
    n   = len(lst)     
    return o(
      median= i.median(),
      iqr   = lst[int(n*.75)] - lst[int(n*.5)],
      lo    = i.lo, 
      hi    = i.hi)
  def ish(i,f=0.1): 
    return i.any() + f*(i.any() - i.any())
  def median(i):
    n = len(i._cache)
    p = n // 2
    if (n % 2):  return i._cache[p]
    q = p + 1
    q = max(0,(min(q,n)))
    return (i._cache[p] + i._cache[q])/2
"""

### Sym

A _Sym_ is a _Log_ for non-numerics.

"""
class Sym(Log):
  def setup(i):
    i.counts,i.mode,i.most={},None,0
  def change(i,x):
    c= i.counts[x]= i.counts.get(x,0) + 1
    if c > i.most:
      i.mode,i.most = x,c
  def report(i):
     return o(dist= i.dist(), 
              ent = i.entropy(),
              mode= i.mode)
  def dist(i):
    n = sum(i.counts.values())
    return sorted([(d[k]/n, k) for 
                   k in i.counts.keys()], 
                  reverse=True)
  def ish(i):
    r,tmp = rand(),0
    for w,x in i.has().dist:
      tmp  += w
      if tmp >= r: 
        return x
    return x
  def entropy(i,e=0):
    for k in i.counts:
      p = i.counts[k]/len(i._cache)
      e -= p*log2(p) if p else 0
    return e    
