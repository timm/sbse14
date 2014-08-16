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

def sa(about=Schaffer):
  model = None
  def maybe(old,new,t):
    return math.e**((old - new)*1.0/t) < rand(); ###
  def baseline(model):
    for _ in xrange(The.sa.baseline):
      model.instance()
  def energy(lst):
    return fromHell(model,lst)
  def neighbor(old):
    new = old[:]
    for num in model.num:
      if rand() > The.sa.p:
        new[header.col] = any(num.lo,num.hi)
    if not model.ok(new):
      return old
    else:
      new = model.score(new)
      model.seen(new)
      return new
  def report():
    for k in sorted(history.keys()):
      print history[k]
  kmax    = The.sa.max
  history = {}  ##
  for _ in xrange(The.optimize.repeats): ##
    model = about()
    baseline(model) # initialize 
    sb = s = model.instance()
    eb = e = energy(s)
    for k,log in Watch(kmax,about,history): ##
      sn = neighbor(s)
      en = energy(sn)
      if en > eb:
        sb,eb = sn,en
      if en > e 
        s,e = sn,en
      elif maybe(e,en,k/kmax**The.sa.stagger):
        s,e = sn,en
      log.record(e) ##
  report()
  
if __name__ == '__main__': eval(cmd())
