"""

## SA2 : Standard SA + Control tricks

### Standard Headers
"""
from __future__ import division
import sys
sys.dont_write_bytecode = True

from models import *

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
  history = {}
  for _ in xrange(The.misc.repeats): 
    sb = s = m.indepIT()
    eb = e = mron(energy(m,s), base.lo, base.hi)
    k = 0
    for k,log in Watch(The.sa.kmax,
                       m, history):
      if not k % The.misc.era: 
        burp("\n", str(k).zfill(4),x(eb), ' ') 
      mark = "."
      sn = m.aroundIT(s,p=1)
      en = mron(energy(m,sn), base.lo, base.hi)
      if en >  (e * The.misc.epsilon):
        s,e = sn,en
        mark = "+"
        log.logIT(s)
      elif maybe(e,en, 
                 k/The.sa.kmax**The.sa.cooling):
        s,e = sn,en
        mark = "?"
      if en > (eb * The.misc.epsilon):
        sb,eb = sn,en
        mark = "!"
      burp(mark)
  return optimzeReport(m,history)
"""

## Example

Defining a study using _sa_.

"""
@study
def saDemo(model='Schaffer'):
  "Basic study."
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
