"""
options.py: option management (setting and sharing
and printing options) 
Copyright (c) 2014 tim.menzies@gmail.com

             /\ \__  __                             
  ___    _____ \ \ ,_\/\_\     ___     ___      ____  
 / __`\ /\ '__`\\ \ \/\/\ \   / __`\ /' _ `\   /',__\ 
/\ \L\ \\ \ \L\ \\ \ \_\ \ \ /\ \L\ \/\ \/\ \ /\__, `\
\ \____/ \ \ ,__/ \ \__\\ \_\\ \____/\ \_\ \_\\/\____/
 \/___/   \ \ \/   \/__/ \/_/ \/___/  \/_/\/_/ \/___/ 
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
import sys
sys.dont_write_bytecode = True

### Defining 'Things' ##############################
class Thing(object):
  def __init__(i,**dict): i.update(dict)
  def also(i,**dict)    : i.update(dict); return i
  def update(i,dict)    : i.__dict__.update(dict)
  def __repr__(i)  : return dump(i.__dict__,'',0)

def dump(d,s='',lvl=0):
  later = []
  s += '# '+'   ' * lvl
  for k,v in sorted(d.items()):
    if isinstance(v,Thing): 
      later += [(k,v.__dict__)]
    elif isinstance(v,dict):
      later += [(k,v)]
    else:
      s += ':%s %s ' % (k,
           v.__name__ if callable(v) else v)
  s += '\n'
  for k,v in later:
    s += '# '+('   ' *  lvl) + ':%s' % k + '\n'
    s= dump(v,s,lvl+1)
  return s

### Defining Settings (nested 'Things') ############
The = Thing()
def settings(f=None,cache=[]):
  """Adds 'f' to the things; if called with no args,
   reset all options back to original values."""
  if f : 
    what = f.func_name[:-4]
    The.__dict__[what] = f() 
    cache += [(what,f)]
  else : 
    for key,f in cache: The.__dict__[key] = f()
  return f

### Begin the actual settings ######################
@settings
def mathings(): return Thing(
  inf = float("inf"),
  ninf = float("-inf"),
  seed = 1,
  tiny = 10**-32,
  centralLimitThreshold=20)

@settings
def brinkings(): return Thing(
  tconf=0.95,
  hot = 102)

@settings
def symings(): 
  def nums(z): return z.nums
  def syms(z): return z.syms
  def more(z): return z.more
  def less(z): return z.less
  def depen(z): return z.depen
  def indep(z): return z.indep
  def about(z): return z.about
  return Thing(
    missing="?",
    numc     ='$',
    patterns = {
      '\$'            : nums,
      '\.'            : syms,
      '>'             : more,
      '<'             : less,
      '[=<>]'         : depen,
      '^[^=<>].*[^!]$': indep,
      '.'             : about})

@settings
def optimizeings():
  def noImprovementBin(betters,worses):
    return not binaryDomination(betters,worses)
  return Thing(epsilon = 0.01,
               era     = 30,
               runs    = 50,
               repeats = 10,
               noImprovement= noImprovementBin)

@settings
def saings():
  return Thing(p       = 0.33,
               stagger = 1.0,
               baseline = 100)

if __name__ == "__main__": print The
