"""
sa101.py: simulated annealling
Copyright (c) 2014 tim.menzies@gmail.com

/\  _`\ /\  _  \              /' \  /'__`\  /' \    
\ \,\L\_\ \ \L\ \      __    /\_, \/\ \/\ \/\_, \   
 \/_\__ \\ \  __ \    /\_\   \/_/\ \ \ \ \ \/_/\ \  
   /\ \L\ \ \ \/\ \   \/_/_     \ \ \ \ \_\ \ \ \ \ 
   \ `\____\ \_\ \_\    /\_\     \ \_\ \____/  \ \_\
    \/_____/\/_/\/_/    \/_/      \/_/\/___/    \/_/                                                    
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
steps=Steps() # <== keep point,same steps across all repeats
for _ in xrange(20):
  resetLearner()
  for step in steps:
    do stomeing with step
    steps.seen(newThing)
report(steps.logs)
"""

def study(model=model, repeats=The.optimize.repeats, 
          reset=noop, run=noop,report=noop,):
  logs = {} # important. same log over all runs
  for _ in range(repeats): # repeat n times
    reset() # reset the optimzer
    for tick in Watch(model,logs): 
      results = run(tick)   # offer some guesses
      watch.record(results) # record what you saw
  report(logs) # report results in all repeats

def binaryDomination(header1,header2):
  for now,then in zip(nows.less,thens.less):
        if not now.same(then):
          if now.mu < then.mu:
            return False
  for now,then in zip(nows.more, thens.more):
        if not now.same(then):
          if now.mu > then.mu:
            return False

class Watch(object):
  def __iter__(i): return i
  def __init__(i,model,logs=None,earlyStop=True):
    i.logs = logs or {}
    i.thisLog  = {}
    i.model,i.earlyStop = model,earlyStop
    i.step, i.era  = 0, 0
  def record(i,results):   
    for log in [i.logs, i.thisLog]:
      if not i.era in log:
        log[i.era] = i.model.clone() 
    here = i.thisLog[i.era]
    there= i.logs[i.era]
    for result in item(results):
      here.seen(result)
      there.seen(result)
  def stop(i):
    if not i.earlyStop: 
      return False
    if len(i.thisLog)> 1:
      nows  = i.thisLog[i.era]
      thens = i.thisLog[i.era - The.sa.era]
    
      return True
    else:
      return False
  def next(i):
    i.step += 1
    stop = True
    if i.step >= i.era: 
      stop = i.canStop()
      if not stop:
        i.era += The.sa.era          
    if stop: 
      return StopIteration()
    elif i.step <= The.sa.max:
      return StopIteration()
    else:
      return i.step

w = Watch(10)
for x in w: 
  print x
  w.tick()
  w.tick()
  w.tick()

exit()

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
