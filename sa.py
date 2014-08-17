"""
sa.py: generics for all optimizers
Copyright (c) 2014 tim.menzies@gmail.com

/\  _`\ /\  _  \    
\ \,\L\_\ \ \L\ \   
 \/_\__ \\ \  __ \  
   /\ \L\ \ \ \/\ \ 
   \ `\____\ \_\ \_\
    \/_____/\/_/\/_/

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
import sys,math
sys.dont_write_bytecode = True
from lib import *
from models import *
from optimize import *

def sa(klass=Schaffer):
  summary = None
  show = The.sa.verbose
  kmax    = The.sa.max
  cooling = The.sa.cooling
  def burp(x):
    if show: say(x)
  def maybe(old,new,t):
    r=rand()
    k= math.e**(-1*(old - new)/t) 
    return k < r
  def baseline(summary):
    for _ in xrange(The.sa.baseline): 
      summary.example()
  def energy(lst):
    return fromHell(summary,lst)
  def neighbor(old):
    new = old[:]
    for num in summary.nums:
      if rand() > The.sa.p:
        new[num.col] = any(num.lo,num.hi)
    if not summary.ok(new):
      return old
    else:
      new = summary.score(new)
      summary.record(new)
      return new
  def report():
    for k in sorted(history.keys()):
      print history[k]
  def num(x): return str(int(100*x))
  history = {}  ##
  for _ in xrange(The.optimize.repeats): ##
    burp("\n")
    summary = klass()
    baseline(summary) # initialize 
    sb = s = summary.example()
    eb = e = energy(s)
    print "EB0>",num(eb),map(g3,sb)
    for k,log in Watch(kmax,klass,history): ##
      burp(".")
      sn = neighbor(s)
      en = energy(sn)
      if en > eb:
        sb,eb = sn,en
        burp("!")
      if en > e: 
        s,e = sn,en
        burp("+")
      elif maybe(e,en,k/kmax**cooling):
        s,e = sn,en
        burp("?")
      log.record(s) ##
      if not k % The.optimize.era: burp(num(eb) + " \n")
    print ":eb",num(eb),":sb",map(g3,sb),":k",k
  report()

def _sa(seed=1):
  
  settings()
  The.math.seed=seed
  rseed()
  sa()
  print The

if __name__ == '__main__': eval(cmd())
