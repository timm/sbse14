"""
lib.py: misc python tricks
Copyright (c) 2014 tim.menzies@gmail.com

/\_ \    __ /\ \       
\//\ \  /\_\\ \ \____  
  \ \ \ \/\ \\ \ '__`\ 
   \_\ \_\ \ \\ \ \L\ \
   /\____\\ \_\\ \_,__/
   \/____/ \/_/ \/___/ 
                       
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and
associated documentation files (the "Software"), to
deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission
notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.""" 

from __future__ import division
import sys,re,random,math,datetime,re,time
sys.dont_write_bytecode = True
from life import *
from options import *

### unit tests #####################################
def test(f=None,cache=[]):
  "Unit test decorator."
  if f: # called as decorator @test above a function
    cache += [f]
    return f
  else: # called as just test(), so run tests
    ok = no = 0
    for t in cache: 
      print '#',t.func_name ,t.__doc__ or ''
      prefix, n, found = None, 0, t() or []
      while found:
        this, that = found.pop(0), found.pop(0)
        if this == that:
          ok, n, prefix = ok+1, n+1,'CORRECT:'
        else: 
          no, n, prefix = no+1, n+1,'WRONG  :'
        print prefix,t.func_name,'test',n
    if ok+no:
      print '\n# Final score: %s/%s = %s%% CORRECT' \
          % (ok,(ok+no),int(100*ok/(ok+no)))

### Math stuff  ###############################
def first(x): return x[0]
def second(x): return x[1]
def third(x): return x[2]
def fourth(x): return x[3]
def fifth(x): return x[4]
def last(x): return x[-1]

def lt(x,y): return x < y
def gt(x,y): return x > y

### Random stuff  ###############################

def shuffle(lst) : 
  random.shuffle(lst)
  return lst

def rseed(n=None):
  n = n or The.math.seed
  random.seed(n)

rand = random.random
def any(x,y):
  return x + (y-x)*rand()

### Interation #####################################

def item(items):
  "return all items in a nested list"
  if isinstance(items,(list,tuple)):
    for one in items:
      for x in item(one):
        yield x
  else:
    yield items

def pairs(lst):
  "Return all pairs of items i,i+1 from a list."
  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i

### Printing #######################################
def nl(): print ""

# printing numbers
def g1(x)    : return round(x,1)
def g2(x)    : return round(x,2)
def g3(x)    : return round(x,3)
def gs1(lst) : return map(g1,lst)
def gs2(lst) : return map(g2,lst)
def gs3(lst) : return map(g3,lst)

# printing nested dictionaries

def prettyd(i,name=None):
  "show public keys, in sorted order"
  def public(key): 
      return not key[0] == "_"
  me    = i.__dict__
  name = name or i.__class__.__name__
  order = sorted(k for k in me.keys() 
                 if public(k))
  pairs = [':%s %s' % (k,me[k]) for k in order]
  return name+'{'+ ', '.join(pairs) +'}'

# succinct printing tricks
def saysln(*lst): 
  says(*lst); nl()
def says(*lst)  : 
  say(', '.join(map(str, lst)))
def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()



### xtiles #################################

### xtile: Pretty Print  Distributions


def xtile(lst,lo=0,hi=100,width=50,
             chops=[0.1 ,0.3,0.5,0.7,0.9],
             marks=["-" ," "," ","-"," "],
             bar="|",star="*",show=" %3.0f"):
  """The function _xtile_ takes a list of (possibly)
  unsorted numbers and presents them as a horizontal
  xtile chart (in ascii format). The default is a 
  contracted _quintile_ that shows the 
  10,30,50,70,90 breaks in the data (but this can be 
  changed- see the optional flags of the function).
  """
  def pos(p)   : return ordered[int(len(lst)*p)]
  def place(x) : 
    return int(width*float((x - lo))/(hi - lo))
  def pretty(lst) : 
    return ', '.join([show % x for x in lst])
  ordered = sorted(lst)
  lo      = min(lo,ordered[0])
  hi      = max(hi,ordered[-1])
  what    = [pos(p)   for p in chops]
  where   = [place(n) for n in  what]
  out     = [" "] * width
  for one,two in pairs(where):
    for i in range(one,two): 
      out[i] = marks[0]
    marks = marks[1:]
  out[int(width/2)]    = bar
  out[place(pos(0.5))] = star 
  return ''.join(out) +  "," +  pretty(what)

def _tileX() :
  import random
  random.seed(1)
  nums = [random.random()**2 for _ in range(100)]
  print xtile(nums,lo=0,hi=1.0,width=25,show=" %3.2f")

  
### Misc stuff #############################

def noop(*lst): return lst

def div(x,y) : 
  "avoid div/0 errors"
  return x/(y+The.math.tiny)
  
def intrapolate(x, points):
  """find adjacent points containing 'x',
   return 'y', extrapolating over neighbor 'x's.
   e.g. interpolate(1.5, [(1,10),(2, 20),(3, 30)])
   returns 15"""
  lo, hi = points[0], points[-1]
  x1, y1 = lo[0], lo[1]
  if x < x1: return y1
  for x2,y2 in points[1:]:
    if x1 <= x < x2:
      deltay = y2 - y1
      deltax = (x- x1)/(x2- x1)
      return y1 + deltay * deltax
    x1,y1 = x2,y2
  return hi[1]

### experiments for header ########################

def study(f):
  """All outputs have date,time, notes,
  a reset of the options,  settings, runtimes."""
  def wrapper():
    what = f.__name__
    doc  = f.__doc__ 
    if doc:
      doc= re.sub(r"\n[ \t]*","\n# ",doc)
    show = datetime.datetime.now().strftime
    print "\n###",what,"################################"
    print "#", show("%Y-%m-%d %H:%M:%S"),"\n"
    if doc: print "#",doc
    settings()
    t1 = time.time()
    print "\n",The
    f()
    t2 = time.time() 
    print The
    print "# Runtime: %.3f secs" % (t2-t1)
  return wrapper

### Coercion  #####################################
def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError: return x

### Command line processing ########################
def cmd(com="life(seed=1)"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

if __name__ == '__main__': eval(cmd())
