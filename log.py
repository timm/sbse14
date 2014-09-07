"""## Log Stuff

Logs are places to store records of past events. There are two types of logs:

+ _Num_ : for numbers
+ _Sym_ : for everything else. 

Those logs can be queried to find e.g. the highest
and lowest value of the number seen so far. Alternatively,
they can be queried to return values at the same probability
as the current log contents.

### Max Log Size

To avoid logs consuming all memory, logs store at
most _The.cache.keep_ entries (e.g. 128):

+ If more
than that number of entries arrive, then some old
entry (selected at random) will be deleted.
+ The nature of this cache means that some rare
events might be missed. To check for that, running
the code multiple times and, each time, double the
cache size. Stop when doubling the cache size stops
changing the output.

Just as an example of that process, here we are logging 1,000,000 numbers in a log with a cache of size 16.
Note that the resulting cache is much smaller than 1,000,000 items. Also, the contents of the cache
come from the entire range one to one million (so our log is not biased to just the first few samples:

     % python -i log.py
     >>> The.cache.keep = 16
     >>> log = Num()  
     >>> for x in xrange(1000000): log += x 
     >>> sorted(log._cache)
     [77748, 114712, 122521, 224268, 
     289880, 313675, 502464, 625036, 
     661881, 663207, 680085, 684674, 
     867075, 875594, 922141, 945896]
     >>> 

### Caching Slow Reports

Some of the things we want to report from these logs take a little while to calculate (e.g. finding the median
requires a sort of a numeric cache):

+ Such reports should be run and cached so they can be accessed many time without the need
for tedious recalculation. 
+ These reports become outdated if new log information arrives so the following
code deletes these reports if ever new data arrives.
+ The protocol for access those reports is to call _log.has().x_ where "x" is a field
  generated by the report.  Log subclasses generate reports using the special _report()_ method
  (see examples, below).

Just as an example of reporting, after the above run (where we logged 1,000,000 numbers), the following reports are available:

     >>> log.has().lo
     0 
     >>> log.has().hi
     945896
     >>> print log.has().median # 50th percentile
     662544.0
     >>> print log.has().iqr # (75-25)th percentile
     205194

Note that our median is not as expected (it should be around half a million). Why? Well, clearly a cache of size 16 is
too small to track a million numbers. So how many numbers do we need? Well, that depends on the distribution being explored
but here's how the median is effected by cache size for uniform distributions:

    >>> for size in [16,32,64,128,256]:
    ...     The.cache.keep=size
    ...     log = Num()
    ...     for x in xrange(1000000): log += x
    ...     print size, ":" log.has().median
    ... 
     16 : 637374.5
     32 : 480145.5
     64 : 520585.5
    128 : 490742.0
    256 : 470870.5


Note that we get pretty close to half a million with cache sizes at 32 or above. And the lesson: sometimes, a limited
sample can offer a useful approximation to a seemingly complex process.

## Standard Header
"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True
from base  import *
from stats import *
"""
## Classes

### Base Class: "Log"

"""
class Log():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],label=''):
    i.label = label
    i._cache,i.n,i._report = [],0,None
    i.setup()
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
      i._report = None # wipe out 'what follows'
      i.change(x)
    return i
  def any(i):  
    return  any(i._cache)
  def has(i):
    if i._report == None: i._report =  i.report()
    return i._report
  def setup(i): pass
  def change(i,x): pass
"""

### Num

A _Num_ is a _Log_ for numbers. 

+ Tracks _lo_ and _hi_ values. 
+ Reports median and the IQR the (75-25)th range.
+ Generates numbers from the log by a three-way interpolation (see _ish()_).


"""
class Num(Log):
  def setup(i):
    i.lo, i.hi = 10**32, -10**32
  def change(i,x): # update lo,hi
    i.lo = min(i.lo, x)
    i.hi = max(i.hi, x)
  def norm(i,x): # turn "x" into 0..1
    return (x - i.lo)/(i.hi - i.lo + 0.000001)
  def report(i): 
    lst = i._cache = sorted(i._cache)
    n   = len(lst)     
    return o(
      median= i.median(),
      iqr   = lst[int(n*.75)] - lst[int(n*.5)],
      lo    = i.lo, 
      hi    = i.hi)
  def ish(i,f=0.1): # return a num from  logged dist 
    return i.any() + f*(i.any() - i.any())
  def better(new,old):
    new.has()
    old.has()
    a       = a12(old._cache,new._cache)
    iDelta  = new.has().iqr - old.has().iqr
    newLess = a >= The.misc.a12
    lessVar = iDelta < 0
    print ":a12",a,":iDelta",iDelta,":newLess",newLess,";lessVar",lessVar
    if newLess   : return True
    elif lessVar : return True
    else         : return False
  def median(i):
    n = len(i._cache)
    p = n // 2
    if (n % 2):  return i._cache[p]
    q = p + 1
    q = max(0,(min(q,n)))
    return (i._cache[p] + i._cache[q])/2

def _num():
  i = Num([rand()      for _ in xrange(1000)])
  j = Num([rand()*1.25 for _ in xrange(1000)])
  print j.same(i)

"""

WARNING: the call to _sorted_ in _report()_ makes this code
a candidate for a massive CPU suck (it is always sorting newly arrived data).
So distinguish between _adding_ things to a log in the _last_ era and 
using that information in the _next_ era (so the log from the last era
is staple in the current).

### Sym

A _Sym_ is a _Log_ for non-numerics.

+ Tracks frequency counts for symbols, and the most common symbol (the _mode_);
+ Reports the entropy of the space (a measure of diversity: lower values mean fewer rarer symbols);
+ Generated symbols from the log by returning symbols at the same probability of the frequency counts (see _ish()_).

"""
class Sym(Log):
  def setup(i):
    i.counts,i.mode,i.most={},None,0
  def report(i):
    for x in i._cache:
      c = i.counts[x] = i.counts.get(x,0) + 1
      if c > i.most:
        i.mode,i.most = x,c
    return o(dist= i.dist(), 
              ent = i.entropy(),
              mode= i.mode)
  def dist(i):
    d = i.counts
    n = sum(d.values())
    return sorted([(d[k]/n, k) for k in d.keys()], 
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
"""

#### Sym, Example

As an example of generating numbers from a distribution, consider the following code.
The logged population has plus, grapes and pears in the ration 2:1:1.
From that population, we can generate another distribution that is nearly the same:

    >>> symDemo()
    (0.5, 'plums'), (0.265625, 'grapes'), (0.234375, 'pears')]
    {'plums': 64, 'grapes': 34, 'pears': 30}

"""
def symDemo(n1=10,n2=1000):
  rseed()
  log= Sym((['plums']*(n1*2)) + ['grapes']*n1 + ['pears']*n1)
  found= Sym([log.ish() for _ in xrange(n2)])
  print found.has().dist
  print found.counts
  print sum(found.counts.values())

if __name__ == "__main__": eval(cmd()) 


