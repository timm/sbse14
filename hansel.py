class Close:
  enough = 20
  tiny   = 0.05
  def __init__(i):
    i.sum = [0.0] * 32
    i.pop = [0.0] * 32
  def keep(i,x):
    for j in xrange(len(i.sum)):
      i.sum[j] += x
      i.pop[j] += 1
      mu   = i.sum[j] / i.pop[j]
      here = i.pop[j] / i.pop[0]
      if i.pop[j] < Close.enough:
        return False
      if here < Close.tiny:
        return True
      if x > mu:
        return False 

def _close():
  import random
  rand=random.random
  c=Close()
  for _ in xrange(1000):
    c.keep(rand())
  n=10000
  lst = [1.0 for _ in xrange(n) 
         if c.keep(rand())]
  print sum(lst)/n

_close()
