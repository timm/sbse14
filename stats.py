from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True
from base import *



def a12(lst1,lst2):
  """how often is lst1 often more than y in lst2?
  assumes lst1 nums are meant to be greater than lst2"""
  def loop(t,t1,t2): 
    while t1.m < t1.n and t2.m < t2.n:
      h1 = t1.l[t1.m]
      h2 = t2.l[t2.m]
      h3 = t2.l[t2.m+1] if t2.m+1 < t2.n else None 
      if h1 > h2:
        t1.m  += 1; t1.gt += t2.n - t2.m
      elif h1 == h2:
        if h3 and gt(h1,h3) < 0:
            t1.gt += t2.n - t2.m  - 1
        t1.m  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1,reverse=True)
  lst2 = sorted(lst2,reverse=True)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = o(l=lst1,m=0,eq=0,gt=0,n=n1)
  t2   = o(l=lst2,m=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)

def _ab12():
  random.seed(1)
  l1 = [random.random() for x in range(1000)]
  more = [random.random()*2 for x in range(1000)]
  l2 = [random.random()  for x in range(1000)]
  less = [random.random()/2.0 for x in range(1000)]
  t1 = msecs(lambda : a12(l1,more))
  print t1,a12(l2,less)

    

def scottknott(data,cohen=0.3,small=3, useA12=False,epsilon=0.01):
  """Recursively split data, maximizing delta of
  the expected value of the mean before and 
  after the splits. 
  Reject splits with under 3 items"""
  def minMu(parts,all,big,epsilon):
    """Find a cut in the parts that maximizes
    the expected value of the difference in
    the mean before and after the cut.
    Reject splits that are insignificantly
    different or that generate very small subsets.
    """
    cut,left,right = None,None,None
    before, mu     =  0, all.mu
    for i,l,r in leftRight(parts,epsilon):
      if big(l.n) and big(r.n):
        n   = all.n * 1.0
        now = l.n/n*(mu- l.mu)**2 + r.n/n*(mu- r.mu)**2  
        if now > before:
          before,cut,left,right = now,i,l,r
    return cut,left,right
  def leftRight(parts,epsilon=0.01):
    """Iterator. For all items in 'parts',
    return everything to the left and everything
    from here to the end. For reasons of
    efficiency, take a first pass over the data
    to pre-compute and cache right-hand-sides
    """
    rights = {}
    n = j = len(parts) - 1
    while j > 0:
      rights[j] = parts[j]
      if j < n: rights[j] += rights[j+1]
      j -=1
    left = parts[0]
    for i,one in enumerate(parts):
      if i> 0: 
        if parts[i]._median - parts[i-1]._median > epsilon:
          yield i,left,rights[i]
        left += one
  def rdiv(data,  # a list of class Nums
         all,   # all the data combined into one num
         div,   # function: find the best split
         big,   # function: rejects small splits
         same, # function: rejects similar splits
         epsilon): # small enough to split two parts
    """Looks for ways to split sorted data, 
    Recurses into each split. Assigns a 'rank' number
    to all the leaf splits found in this way. 
    """
    def maybeIgnore((cut,left,right), same,parts):
      if cut:
        if same(sum(parts[:cut],Num('upto')),
                sum(parts[cut:],Num('above'))):    
          cut = left = right = None
      return cut,left,right  
    def recurse(parts,all,rank=0):
      "Split, then recurse on each part."
      cut,left,right = maybeIgnore(div(parts,all,big,
                                       epsilon),
                                   same,parts)
      if cut: 
        # if cut, rank "right" higher than "left"
        rank = recurse(parts[:cut],left,rank) + 1
        rank = recurse(parts[cut:],right,rank)
      else: 
        # if no cut, then all get same rank
        for part in parts: 
          part.rank = rank
      return rank
    recurse(sorted(data),all)
    return data
  all  = reduce(lambda x,y:x+y,data)
  same = lambda l,r: abs(l.median() - r.median()) <= all.s()*cohen
  if useA12: 
    same = lambda l, r:   not different(l.all,r.all) 
  big  = lambda    n: n > small    
  return rdiv(data,all,minMu,big,same,epsilon)

if __name__ == "__main__" : eval(cmd())


