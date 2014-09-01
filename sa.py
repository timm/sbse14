"""

## SA (plus tricks)

This file shows some
of Timm's tricks for building an optimization.

To illustrate the tricks, they are applied to 
build a simulated annealer.

Share and enjoy.

## Standard Headers

Here we see some standard Python file headers.

"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True

from base import *
from log  import *
"""


## Simulation Experiment Control

The code adds a set of cliches onto
to some optimization call.

"""
def study(f):
  def wrapper(*lst):
    what = f.__name__# print the function name
    doc  = f.__doc__ # print the function doc
    if doc:
      doc= re.sub(r"\n[ \t]*","\n# ",doc)
    # print when this ran
    show = datetime.datetime.now().strftime 
    print "\n###",what,"#" * 50
    print "#", show("%Y-%m-%d %H:%M:%S")
    if doc: print "#",doc
    t1 = time.time()
    f(*lst)          # run the function
    t2 = time.time() # show how long it took to run
    print "\n" + ("-" * 50)
    showd(The)       # print the options
    print "\n# Runtime: %.3f secs" % (t2-t1)
  return wrapper
"""

## Parts of a Simulation

There are several parts of a simulation many of which 
have a similar form; i.e. some _x-y_ pair where _"x"_
is the independent variable and _"y"_ is the dependent variable.
of indepene

+ _It_ : some current candidate


## "Of"-ing

"""
class In:
  def __init__(i,lo=0,hi=1,txt=""):
    i.txt,i.lo,i.hi = txt,lo,hi
  def __call__(i): 
    return i.lo + (i.hi - i.lo)*rand()
  def log(i): 
    return Num()

class Model:
  def name(i): 
    return i.__class__.__name__
  def __init__(i):
    i.of = i.spec()
    i.log= o(x= [z.log() for z in i.of.x],
              y= [Num()   for _ in i.of.y])
  def indepIT(i):
    "Make new it."
    return o(x=[z() for z in i.of.x])
  def depIT(i,it):
    "Complete it's dep variables."
    it.y = [f(it) for f in i.of.y]
    return it
  def logIT(i,it):
    "Remember what we have see in it."
    for val,log in zip(it.x, i.log.x): log += val
    for val,log in zip(it.y, i.log.y): log += val
  def aroundIT(i,it,p=0.5):
    "Find some place around it."
    def n(val,f): 
      return f() if rand() < p else val
    old = it.x
    new = [n(x,f) for x,f in zip(old,i.of.x)]
    return o(x=new)
"""

XY = a pair of related indep,dep lists

it = actual values

of = meta knowledge of members of it

log = a record of things seen in it

seperate (1) guesses indep variables (2) using them to

calc dep values (3) logging what was picked

"""
def sa(m):
  def more(k,e):
    if k > The.sa.patience:
      if e > 1/The.misc.epsilon:
        return False
    return True
  def energy(m,it): 
    m.depIT(it)
    return sum(it.y) 
  def maybe(old,new,temp): 
    return math.e**((new - old)/temp) < rand()  
  base = Num([energy(m, m.indepIT()) 
             for _ in xrange(The.sa.baseline)])
  sb = s = m.indepIT()
  eb = e = norm(energy(m,s), base.lo, base.hi)
  k = 0
  while k <  The.sa.kmax and more(k,eb):
    if not k % The.misc.era: 
      burp("\n", str(k).zfill(4),x(eb), ' ') 
    k += 1
    mark = "."
    sn = m.aroundIT(s,p=1)
    en = norm(energy(m,sn), base.lo, base.hi)
    if en >  (e * The.misc.epsilon):
      s,e = sn,en
      mark = "+"
    elif maybe(e,en, 
               k/The.sa.kmax**The.sa.cooling):
      s,e = sn,en
      mark = "?"
    if en > (eb * The.misc.epsilon):
      sb,eb = sn,en
      mark = "!"
    burp(mark)
  return sb,eb    
"""

Defining a study using _sa_.

"""
@study
def saDemo(m):
  "Basic study."
  rseed()
  print "\n",m.name()
  sb,eb = sa(m)
  x= g3(sb.x)
  y= g3(sb.y)
  print "\n------\n:e",eb,"\n:y",y,"\n:x",x
"""

## Models

"""
class Schaffer(Model):
  def spec(i):
    return o(x= [In(-5,5,0)],
              y= [i.f1,i.f2])
  def f1(i,it):
    x=it.x[0]; return x**2
  def f2(i,it):
    x=it.x[0]; return (x-2)**2

class ZDT1(Model):
  def spec(i):
    return o(x= [In(0,1,z) for z in range(30)],
              y= [i.f1,i.f2])
  def f1(i,it):
    return it.x[0]
  def f2(i,it):
    return 1 + 9*sum(it.x[1:]) / 29
"""

## Demo Code

"""
saDemo(Schaffer())
saDemo(ZDT1())
