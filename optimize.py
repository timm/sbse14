"""
optimze.py: generics for all optimizers
Copyright (c) 2014 tim.menzies@gmail.com

/\  __`\        /\ \__  __              __                  
\ \ \/\ \  _____\ \ ,_\/\_\    ___ ___ /\_\  ____      __   
 \ \ \ \ \/\ '__`\ \ \/\/\ \ /' __` __`\/\ \/\_ ,`\  /'__`\ 
  \ \ \_\ \ \ \L\ \ \ \_\ \ \/\ \/\ \/\ \ \ \/_/  /_/\  __/ 
   \ \_____\ \ ,__/\ \__\\ \_\ \_\ \_\ \_\ \_\/\____\ \____\
    \/_____/\ \ \/  \/__/ \/_/\/_/\/_/\/_/\/_/\/____/\/____/
             \ \_\                                          
              \/_/                                       

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

def study(about, repeats=The.optimize.repeats, 
          reset=noop, run=noop,report=noop,):
  logs = {}                #use same log on all runs
  for _ in xrange(repeats): #repeat for a few times
    reset()                # reset optimzer
    watch=Watch(about,logs)
    for tick in watch:
      run(tick,watch)  
  report(logs) # report results in all repeats

def binaryDomination(goods,bads):
  "checks that at least one better, and no worse"
  better = 0
  for good,bad in zip(goods.less,bads.less):
    if good.same(bad)   : break
    if good.mu < bad.mu : better += 1
    if good.mu > bad.mu : return False
  for good,bad in zip(goods.more, bads.more):
    if good.same(bad)   : break
    if good.mu > bad.mu : good += 1
    if good.mu < bad.mu : return False
  return better > 0
 
def fromHell(about,lst):
  "Euclidean distance from worst goal; a.k.a. hell"
  scores = n = 0 
  normed = lambda z: z.norm(lst[z.col])
  for x in about.less:
    n += 1
    scores += (1 - normed(x))**2
  for x in about.more:
    n += 1
    scores += normed(x)**2
  return div(scores**0.5, n**0.5)
            
class Watch(object):
  def __iter__(i): return i
  def __init__(i,most,about,logs=None,earlyStop=True):
    i.logs = logs or {}
    i.thisLog  = {}
    i.most, i.about,i.earlyStop = most,about,earlyStop
    i.step, i.era  = 0, 0
  def record(i,result):
    """ Each recorded result is one clock tick.
        Record all results in both  logs"""
    both = [i.logs, i.thisLog]     
    for log in both:
      if not i.era in log:
        log[i.era] = i.about()
    i.step += 1
    for log in both:
      log[i.era].seen(result)
  def stop(i):
    """if more than two eras, suggest
       stopping if no improvement."""
    if len(i.thisLog) > 1:
      now = i.era
      before = now - The.sa.era
      if The.optimize.noImprovement(
                           i.thisLog[now],
                           i.thisLog[then]):
        return True
    return False
  def next(i):
    "return next time tick, unless we need to halt."
    if i.step > i.most: # end of run!
      return StopIteration()
    if i.step >= i.era:     # pause to reflect
      if i.earlyStop():     # maybe exit early
        if i.stop():        
           return StopIteration()
      i.era += The.sa.era   # set next pause point
    return i.step,i

# def watch(report=f):
#   k = knext = 0
#   while k < (kmax):
#     k += 1
#     if k >= knext:
#       knext +=  The.sa.era 
#     log = Num()
#     logs = [log]+ logs
#     yield k,log,logs
#     if len(log) > 1:
#       if log[0].same(log[1]):
#         break
#   report(logs)
 
# def sa(model=Schaffer, p=The.sa.p, kmax=The.sa.kmax,
#        epsilon=The.sa.epsilon, seed=The.
#        runs=The.sa.runs,
#        stagger=The.sa.stagger): 
#   "Simulated annealing."
#   def baseline(): 
#     for _ in range(100): m.guess() 
#   def maybe(old,new,t): 
#     return math.e**((old - new)*1.0/max(1,t)) < rand()
#   def neighbor(lst):
#     for h in m.t.nums:
#       if rand() < p:
#         lst[h.pos] = any(h.lo,h.hi)
#     if m.valid(lst):
#       return m.seen(lst)
#     else:
#       return lst
#   def logs(lst=[]):
#     return  [Num()] + lst
  
#   #--------------------
  
#   rseed(seed)
#   for k,log, in xrange(kmax):
#     log = 
#     say('.')
#     m   = model()
#     baseline()
#     sb  = s = m.any()
#     eb  = e = fromhell(s, m.t)
#     for k,inner in do(range(kmax),
#                       epsilon,"best",era,also=outer):
#       sn = neighbor(s[:])
#       en = fromhell(sn,m.t)
#       if en > eb: 
#         sb,eb = sn,en
#       if en > e:
#         s,e = sn,en
#       elif maybe(e, en, k*1.0/kmax**stagger) :
#         s,e = sn,en
#       inner.seen(k, best=eb, every=e)
#   done(outer, 0,1,
#        key   = lambda z: '%2d'   % z,
#        value = lambda z: '%4.2f' % z)
