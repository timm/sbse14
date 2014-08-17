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
import sys,re,random,math,datetime
sys.dont_write_bytecode = True
from lib import *

# def study(klass, repeats=The.optimize.repeats, 
#           reset=noop, run=noop,report=noop,):
#   logs = {}                #use same log on all runs
#   for _ in xrange(repeats): #repeat for a few times
#     reset()                # reset optimzer
#     watch=Watch(klass,logs)
#     for tick in watch:
#       run(tick,watch)  
#   report(logs) # report results in all repeats

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
 
def fromHell(klass,lst):
  "Euclidean distance from worst goal; a.k.a. hell"
  scores = n = 0 
  normed = lambda z: z.norm(lst[z.col])
  for x in klass.less:
    n += 1
    scores += (1 - normed(x))**2
  for x in klass.more:
    n += 1
    scores += normed(x)**2
  return div(scores**0.5, n**0.5)
            
class Watch(object):
  def __iter__(i): return i
  def __init__(i,most,klass,history=None):
    i.early = The.optimize.early  
    i.history = {} if history == None else history
    i.log  = {}
    i.most, i.klass = most,klass
    i.step, i.era  = 1,1
  def record(i,result):
    """ Each recorded result is one clock tick.
        Record all results in log and history"""
    both = [i.history, i.log]     
    for log in both:
      if not i.era in log:
        log[i.era] = i.klass()
    i.step += 1
    for log in both:
      log[i.era].record(result)
  def stop(i):
    """if more than two eras, suggest
       stopping if no improvement."""
    if len(i.log) >= The.optimize.early:
      now = i.era
      before = now - The.optimize.era
      if The.optimize.noImprovement(
                           i.log[now],
                           i.log[before]):
        return True
    return False
  def next(i):
    "return next time tick, unless we need to halt."
    if i.step > i.most: # end of run!
      raise StopIteration()
    if i.step >= i.era:     # pause to reflect
      if i.early > 0:     # maybe exit early
        if i.stop():        
           raise StopIteration()
      i.era += The.optimize.era   # set next pause point
    return i.step,i

