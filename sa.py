"""

## SA (plus tricks)

This file shows some
of Timm's tricks for building an optimization.

To illustrate the tricks, they are applied to 
build a simulated annealer.

In sumamry, those tricks are:

+ [Some basic Python tricks](basepy);
+ [Tricks for logging values](logpy);
+ [Tricks for succinctly specifying models](modelspy);
+ [Tricks for running optimization studies](optimizepy).

Share and enjoy.


### Standard Headers
"""
from __future__ import division
import sys
sys.dont_write_bytecode = True

from models import *
"""

### Code

The following code assumes that _energy_ is the 
sum of the dependent variables.

The _m_ variable is an instance of class [Model](modelspy).

This code seeks to maximize the energy
so we normalize energies
in the range lo..hi  to 1..0 .

A baseline study collects standard values for these
dependent values: see the _base_ variable, which calls the
model The.sa.baseline number of times. 

These baseline is
used to learn the _lo,hi_ values of the energy
which is then used to normalize all future energies
one to zero, min to max.

In the following, we terminate early if we fall within
_The.misc.epsilon_ of best energy or we do more
that _The.sa.kmax_ iterations.
 
Finally, the _burp_ function prints some output- which can
suppressed via _The.misc.verbose=False_.

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
  eb = e = mron(energy(m,s), base.lo, base.hi)
  k = 0
  while k <  The.sa.kmax and more(k,eb):
    if not k % The.misc.era: 
      burp("\n", str(k).zfill(4),x(eb), ' ') 
    k += 1
    mark = "."
    sn = m.aroundIT(s,p=1)
    en = mron(energy(m,sn), base.lo, base.hi)
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

## Example

Defining a study using _sa_.

"""
@study
def saDemo(model='Schaffer'):
  "Basic study."
  The.misc.verbose= True
  The.misc.era = 25
  print "!!!",model
  model = eval(model + '()')
  print "\n",model.name()
  sb,eb = sa(model)
  x= g3(sb.x)
  y= g3(sb.y)
  print "\n------\n:e",eb,"\n:y",y,"\n:x",x
"""

Output from the first call:


    ### saDemo ##################################################
    # 2014-09-02 11:19:58
    # Basic study.
    
    Schaffer
    
    , 0000, :0.2,  !.?+?+??.+?.++?+.++...?.+
    , 0025, :1.0,  .?+..?+?+..+..?++..??+.?.
    , 0050, :1.0,  +....?+.?+.+.?++++?+.?.+.
    , 0075, :1.0,  .?+......?+..?+......+...
    , 0100, :1.0,  .+........?+.?++++?.+?+..
    , 0125, :1.0,  ..+...?+.................
    , 0150, :1.0,  ................?++...+?.
    , 0175, :1.0,  +++...?+.+.?++.......?.+.
    , 0200, :1.0,  ...?+..+.+..?+.+.+.......
    , 0225, :1.0,  ...?+..............+...?+
    , 0250, :1.0,  .
    ------
    :e 0.997611905488 
    :y 0.490, 1.690 
    :x 0.700
    
    --------------------------------------------------
    
    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 
    
    # Runtime: 0.007 secs
    
Output from the second call:

    ### saDemo ##################################################
    # 2014-09-02 11:19:58
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
    
    # Runtime: 0.011 secs
"""

if __name__ == "__main__": eval(cmd())
