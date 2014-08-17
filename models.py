"""
models.py: models (to be optimized)
Copyright (c) 2014 tim.menzies@gmail.com
                     __          ___             
 /'\_/`\            /\ \        /\_ \            
/\      \    ___    \_\ \     __\//\ \     ____  
\ \ \__\ \  / __`\  /'_` \  /'__`\\ \ \   /',__\ 
 \ \ \_/\ \/\ \L\ \/\ \L\ \/\  __/ \_\ \_/\__, `\
  \ \_\\ \_\ \____/\ \___,_\ \____\/\____\/\____/
   \/_/ \/_/\/___/  \/__,_ /\/____/\/____/\/___/
                            
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
import sys
sys.dont_write_bytecode = True
from about import *

class Schaffer(Model):
  def spec(i):
    return [ Num(name='$x', 
                 bounds = (-100,100))
             ,Num(name='<f1')
             ,Num(name='<f2')
           ]
  def score(i,lst):
    x = i.get(lst, "$x")
    i.set("<f1", lst, x**2       )
    i.set("<f2", lst, (x - 2)**2 )
    #print i.get(lst, "$x"),i.get(lst,"<f2")
    return lst
  
def _schaffered1():
  summary = Schaffer()
  _schaffered0(summary)

def _schaffered0(summary):
  def show(txt,lst):
    print txt
    for one in lst: print "\t",one
  show(":about",summary.about)
  show(":indep",summary.indep)
  show(":depen",summary.depen)
  
def _schaffered2(seed=1):
  rseed(seed)
  summary = Schaffer()
  tbl = []
  for _ in range(10):
    eg = summary.guess()
    summary.score(eg)
    tbl += [eg]
  for one in sorted(tbl):
    print one

def _schaffered3(seed=1):
  rseed(seed)
  summary = Schaffer()
  for _ in range(10):
    eg = summary.guess()
    summary.score(eg)
    summary.record(eg)
    print eg
  nl()
  _schaffered0(summary)

class ZDT1(Model):
  def spec(i):
    lst = [Num(name='$'+str(n), bounds=(0,1))
           for n in enumerate(range(30))]
    return lst + [Num(name='<f1')
                  ,Num(name='<f2')]
  def score(i,lst):
    n       = 30
    g       = 1 + 9*sum(lst[1:-3])/(n-1)
    one     = lst[0]
    f1      = one
    f2      = g * (1 - (one/g)**0.5)
    lst[-2] = f1
    lst[-1] = f2
    return lst

if __name__ == "__main__": eval(cmd())
