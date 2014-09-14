from __future__ import division
import sys
sys.dont_write_bytecode = True
from lib import *
  
class Cache():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],label=''):
    i.label = label
    i._cache,i.n,i.m,i._report = [],0,0,None
    map(i.__iadd__,inits)
  def __iadd__(i,x): #  magic method for "+="
    if x == None: return x # skip nothing
    i.n += 1
    changed = False
    if len(i._cache) < The.cache.keep: # not full
      changed = True
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._cache[int(rand()*The.cache.keep)] = x
    if changed:      
      if i.n > i.m* The.cache.update:
        i._report = None # wipe out 'what follows'
        i.m = i.n
    return i
  def any(i):  
    return  any(i._cache)
  def has(i):
    if i._report == None: i._report =  i.report()
    return i._report
  def norm(i,x):
    lo, hi = i.has().lo, i.has().hi
    return (x - lo) / (hi - lo + 0.00001)
  def report(i):
    lst  = sorted(i._cache)
    n    = len(lst)
    q1,q2= int(n*0.25), int(n*0.75)
    return o(median= median(lst),
             iqr   = lst[q2] - lst[q1],
             lo    = lst[0],
             hi    = lst[-1])

if __name__ == '__main__': eval(cmd())
