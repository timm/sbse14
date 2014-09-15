"""

## Optimize

### Standard Header

"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True

from log  import *
"""


## @study: Simulation Experiment Control

The code adds a set of cliches onto
to some optimization call:

+ **TRAP THE SEED**. I cannot stress this enough.
  When debugging or reproducing old code, it is vital
  you can access the old seed.
+ When generating output, add a date stamp and
  any available information about the function being
  called.
+ Show the runtimes of the call.
+ Show the options used by the call.

For example, suppose this was your 
main call to an optimizer:

    @study
    def saDemo(model='Schaffer'):
      "Basic study."
      model = eval(model + '()')
      print "\n",model.name()
      sb,eb = sa(model)
      x= g3(sb.x)
      y= g3(sb.y)
      print "\n------\n:e",eb,"\n:y",y,"\n:x",x

When run, this generates the following output:

    >>>> saDemo(ZDT1())

    ### saDemo ##################################################
    # 2014-09-02 10:40:00
    # Basic study.
    
    ZDT1
    
    , 0000, :0.2,  !?+?!??++?+?++.!?++.....?
    , 0025, :0.8,  !?+?+?+.+..+....?.+.?++.+
    , 0050, :1.0,  ?+?..?+?+.+.....+.+...?..
    , 0075, :1.0,  ?++?......?+.+....?..?++.
    , 0100, :1.0,  +.......?..?+.+.......?.+
    , 0125, :1.0,  ++?+.....................
    , 0150, :1.0,  ?++...?..?+.+.?+++..?+..+
    , 0175, :1.0,  +...............?......+.
    , 0200, :1.0,  .........................
    , 0225, :1.0,  ....?++.+......?+........
    , 0250, :1.0,  .
    ------
    :e 1 
    :y 0.125, 4.186 
    :x 0.125, 0.407, 0.137, 0.079, 0.154, 0.301, 
       0.999, 0.479, 0.109, 0.454, 0.395, 0.333, 
       0.268, 0.196, 0.926, 0.322, 0.133, 0.470, 
       0.043, 0.134, 0.755, 0.859, 0.156, 0.318, 
       0.196, 0.416, 0.133, 0.089, 0.386, 0.618
    
    --------------------------------------------------
    
    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 
    
    # Runtime: 0.020 secs


Code:

"""
def study(f):
  def wrapper(**lst):
    rseed() # reset the seed to our default
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
    f(**lst)          # run the function
    t2 = time.time() # show how long it took to run
    print "\n" + ("-" * 72)
    showd(The)       # print the options
    print "\n# Runtime: %.3f secs" % (t2-t1)
  return wrapper
"""

## Model Definition

Over the years, I've learned to tease apart
several aspects of optimization; specifically:

+ how to make candidate values
+ how to change candidate values
+ how to record the candidate values.
+ and all that is separate to where I store the 
  current candidate. 


The thing that weaves
all those aspects together is the _Model_ class.
Such a  _Model_ 
  does not store an individual candidate. Rather
  it stores information _about_ the candidate
  including how to make, log and change it.

In the following:

+ Those candidates are called _it_.
+ The generators are called _of_,
+ The things that record values are called _log_.

All of _(it, of, log)_ are stored in the same pair of dependent
and independent variables. So many times in the following
code is some container:

     o(x= Independents, y= Dependents)

WARNING: my code is a little nervous about always scoring the dependent
variables every time I change the independent variables (lest that evaluation
makes the whole process too slow). Which means that my _it_ things often
contain nulls for the dependent variables. This can lead to bugs of the form:

    TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'

So, two solutions to this:

+ _Always_ score the dependents when the independents change;
+ But if the evaluation process is slow, then just more code carefully around the null problem.


### Code

That said, say hello to my little friend:

"""
class Model:
  def name(i): 
    return i.__class__.__name__
  def __init__(i):
    "Initialize the generators and loggers."
    i.of = i.spec()
    i.log= o(x= [of1.log() for of1 in i.of.x],
             y= [Num()     for _   in i.of.y])
  def better(news,olds):
    def worsed():
      return  ((same     and not betterIqr) or 
               (not same and not betterMed))
    def bettered():
      return not same and betterMed
    out = False
    for new,old in zip(news.log.y, olds.log.y):
      betterMed, same, betterIqr = new.better(old)
      if worsed()  : return False # never any worsed
      if bettered(): out= out or True # at least one bettered
    return out
  def cloneIT(i):
    return i.__class__()
  def indepIT(i):
    "Make new it."
    return o(x=[generate() for generate in i.of.x])
  def depIT(i,it):
    "Complete it's dep variables."
    it.y = [generate(it) for generate in i.of.y]
    return it
  def logIT(i,it):
    "Remember what we have see in it."
    for val,log in zip(it.x, i.log.x): log += val
    for val,log in zip(it.y, i.log.y): log += val
  def aroundIT(i,it,p=0.5):
    "Find some place around it."
    def n(val,generate): 
      return generate() if rand() < p else val
    old = it.x
    new = [n(x,generate) for 
                       x,generate in zip(old,i.of.x)]
    return o(x=new)
  def ish(i,it):
    return o(x= [of1.ish() for of1 in i.of.x])
"""

Given the above, it is now very succinct to specify
a _Model_. For example, here's a model with 30 independent
variables and 2 dependent ones:

    class ZDT1(Model):
      def spec(i):
        return o(x= [In(0,1,z) for z in range(30)],
                 y= [i.f1,i.f2])
      def f1(i,it):
        return it.x[0]
      def f2(i,it):
        return 1 + 9*sum(it.x[1:]) / 29

Note that to completely understand the above
example you need to read up on the _In_ class
in [models.py](modelspy), But it is easy to get the general
idea: _In_ is something that ranges from zero to one.

## Optimization Control

"""
class Watch(object):
  def __iter__(i): 
    return i
  def __init__(i,model,history=None):
    i.early   = The.misc.early  
    i.history = {} if history == None else history
    i.log     = {}
    i.most, i.model = The.sa.kmax, model
    i.step, i.era  = 1,1
  def logIT(i,result):
    """ Each recorded result is one clock tick.
        Record all results in log and history"""
    both = [i.history, i.log]     
    for log in both:
      if not i.era in log:
        log[i.era] = i.model.cloneIT()
    i.step += 1
    for log in both:
      log[i.era].logIT(result)
  def stop(i):
    """if more than two eras, suggest
       stopping if no improvement."""
    if len(i.log) >= The.misc.early:
      #print 3
      now = i.era
      before = now - The.misc.era
      beforeLog = i.log[before]
      nowLog    = i.log[now]
      if not nowLog.better(beforeLog):
        #print 4
        return True
    return False
  def next(i):
    "return next time tick, unless we need to halt."
    if i.step > i.most: # end of run!
      raise StopIteration()
    if i.step >= i.era:   # pause to reflect
      #print 1, i.step, i.era
      if i.early > 0:     # maybe exit early
        #print 2
        if i.stop():        
           raise StopIteration()
      i.era += The.misc.era   # set next pause point
    return i.step,i

def optimizeReport(m,history):
  for z,header in enumerate(m.log.y):
    print "\nf%s" % z
    for era in sorted(history.keys()):
      log = history[era].log.y[z]
      log.has()
      print str(era-1).rjust(7),\
            xtile(log._cache,
                  width=33,
                  show="%5.2f",
                  lo=0,hi=1)

if __name__ == "__main__": eval(cmd())
