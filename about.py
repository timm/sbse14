"""
about.py: meta-knowledge of variables
Copyright (c) 2014 tim.menzies@gmail.com
 ______      __                          __      
/\  _  \    /\ \                        /\ \__   
\ \ \L\ \   \ \ \____    ___    __  __  \ \ ,_\  
 \ \  __ \   \ \ '__`\  / __`\ /\ \/\ \  \ \ \/  
  \ \ \/\ \   \ \ \L\ \/\ \L\ \\ \ \_\ \  \ \ \_ 
   \ \_\ \_\   \ \_,__/\ \____/ \ \____/   \ \__\
    \/_/\/_/    \/___/  \/___/   \/___/     \/__/
 
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
import sys,re,random,math
sys.dont_write_bytecode = True
from lib import *
                                  
"""
Bout
|-- About
|-- |-- Schaffer
|-- About1
|-- |-- Id
|-- |-- Fixed
|-- |-- Sym
|-- |-- Num
"""             

class Bout(object): 
  def ok(i,x)   : pass
  def guess(i,old,control=None): pass
  def __repr__(i): return prettyd(i)
  
class About(Bout):
  def __init__(i,cols=[]):
    i.depen, i.indep,  i.nums, i.syms= [],[],[],[] 
    i.more,  i.less, i.about, i.where = [],[],[],{}
    i.names=[]
    i.cols(cols)
  def cols(i,lst):
    for col,header in enumerate(lst): 
      header.col = col
      i.where[header.name] = header
      i.name += [header.name]
      for pattern,val in The.sym.patterns.items():
        if re.search(pattern,header.name):
          val(i).append(header)
  def clone(i):
    return i.__class__()
#numc=The.sym.numc
 #   for one in i.about:
  #    what = Num if numc in one.name else Sym
   #   out += [what(name=one.name)]
    #return About(out)
  def seen(i,lst):
    for header,item in zip(i.about,lst):
      if not item == None:
        header.seen(item)
  def ok(i,lst):
    for about,x in zip(i.about(),lst):
      if not about.ok(x):
        return False
    return True
  def guess(i,olds=None,control=None):
    lst = olds or [None] * len(i.about)
    for header,old in zip(i.indep,lst):
      lst[header.col] = header.guess(old)
    return lst
  def score(i,lst): return lst
  def instance(i):
    lst = i.score(i.guess())
    i.seen(lst)
    return lst
  def set(i,name,lst, val):
    lst[i.where[name].col] = val
    return val
  def get(i,lst,name):
    return lst[i.where[name].col]

class Model(About): 
  def __init__(i):
    super(Model,i).__init__()
    i.cols(i.spec())

class About1(Bout): pass

class Sym(About1) : pass

class Num(About1):
  """Num has 'bounds' of legal (min,max) values as well
   as well as observed 'lo','hi' nums seen so far."""
  def __init__(i,inits=[],name='',
               bounds=(The.math.ninf, The.math.inf)):
    i.zero()
    i.name = name
    i.bounds = bounds
    for x in inits: i.inc(x)
  def ok(i,n):
    "Legal if in bounds (or unknown)"
    if n == The.sym.missing:
      return True
    if n == i.bounds: return True
    return i.bounds[0] <= n < i.bounds[1]
  def guess(i,old):
    lo,hi = i.bounds[0], i.bounds[1]
    return any(lo,hi)
  def zero(i):
    "Reset all knowledge back to Eden."
    i.lo,i.hi = The.math.inf,The.math.ninf
    i.n = i.mu = i.m2 = 0
  def __lt__(i,j): 
    "Sorting function."
    return i.mu < j.mu
  def __iadd__(i,x): i.inc(x); return i
  def __isub__(i,x): i.sub(x); return i
  def inc(i,x):
    "Remember 'x'."
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    "Forget 'x'."
    if i.n < 2:  return i.zero()
    i.n  -= 1
    delta = x - i.mu
    i.mu -= delta/(1.0*i.n)
    i.m2 -= delta*(x - i.mu) 
  def sd(i) :
    "Diversity around the mean"
    if i.n < 2: return 0 
    return (max(0,i.m2)/(i.n - 1))**0.5
  def norm(i,x):
    "Map 'x' to 0..1 for lo..hi"
    return (x - i.lo)/ (i.hi - i.lo + 0.00001)
  def t(i,j):
    "Difference in means, adjusted for sd."
    signal = abs(i.mu - j.mu)
    noise  = (i.sd()**2/i.n + j.sd()**2/j.n)**0.5
    return signal / noise
  def same(i,j,
           conf=The.brink.tconf,
           threshold={.95:((  1, 12.70 ),( 3, 3.182),
                           (  5,  2.571),(10, 2.228),
                           ( 20,  2.086),(80, 1.99 ),
                           (320,  1.97 )),
                      .99:((  1, 63.657),( 3, 5.841),
                           (  5,  4.032),(10, 3.169),
                           ( 20,  2.845),(80, 2.64 ),
                           (320,  2.58 ))}):
    "Test for statistically significant difference"
    v     = i.n + j.n - 2
    pairs = threshold[conf]
    delta = intrapolate(v,pairs)
    return delta >= i.t(j)

@test
def numed():
  "check the Num class"
  rseed(1)
  def push(x,n=0.2):
    return x*(1 + n*rand())
  n1=Num(x    for x in range(30))
  n2=Num(30+x for x in range(30))
  lst1 = [x   for x in range(30)]
  n3, n4 = Num(lst1), Num()
  for x in lst1:  n4 += x
  for x in lst1: n4 -= x
  n5 = Num(0.0001+x for x in range(30))
  return [14.5, n1.mu
         ,8.80, g2(n1.sd())
         ,30,   n2.lo
         ,59,   n2.hi
         ,True, n3.sd() == n4.sd()
          ,0,    n4.sd()
         ,0,    n4.n
         ,True, n5.same(n1)
         ,False,n5.same(n2)
         ]

if __name__ == "__main__": eval(cmd())
