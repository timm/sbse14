"""

## SA2 : Standard SA + Control tricks

"""
from __future__ import division
import sys
sys.dont_write_bytecode = True

from models import *

def sa(m):
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
    for k,log in Watch(m, history):
      sn = m.aroundIT(s,p=1)
      en = mron(energy(m,sn), base.lo, base.hi)
      log.logIT(sn)
      t = (k/The.sa.kmax)**The.sa.cooling
      if en > (eb * The.misc.epsilon):
        sb,eb = sn,en
      if en >  (e * The.misc.epsilon):
        s,e = sn,en
      elif maybe(e,en,t):
        s,e = sn,en
     
  return optimizeReport(m,history)

@study
def saDemo(model='Schaffer'):
  "Basic study."
  #The.misc.era=25
  model = eval(model + '()')
  print "\n",model.name()
  sa(model)

if __name__ == "__main__": eval(cmd())
