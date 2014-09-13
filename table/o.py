from __future__ import division
import sys
sys.dont_write_bytecode = True

class o(object):
  def __init__(i,**d): 
    i.has().update(d)
  def has(i)  : return i.__dict__
  def items(i): return i.has().items()
  def __getitem__(i, k): return i.has()[k]
  def __setitem__(i, k, v): i.has()[k]=v
  def __repr__(i):
    return i.__class__.__name__+str(i.has())
  def show(i) : 
    print i.__class__.__name__
    pretty(i.has(),1)
