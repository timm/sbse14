"""

## Models

## Standard Header

"""
from __future__ import division
import sys
sys.dont_write_bytecode = True

from optimize import *
"""

## Classes

The instance created by (say) _In(0,10)_
can be queried to return numbers in the range 0 to 10.
For example:

    >>> x = In(0,10)
    >>> lst = sorted([x() for _ in xrange(32)])
    >>> print g2(lst)
    >>> 0.00, 0.03, 0.36, 0.75, 0.95, 1.02, 
        1.21, 2.07, 2.38, 2.87, 2.97, 3.19, 
        3.35, 3.50, 3.67, 3.97, 4.33, 4.77, 
        5.72, 5.76, 5.99, 6.14, 6.70, 7.55, 
        7.91, 8.36, 8.42, 8.50, 8.72, 8.79, 
        9.25, 9.48

Code:

"""


class In:
  def __init__(i,lo=0,hi=1,txt=""):
    i.txt,i.lo,i.hi = txt,lo,hi
  def __call__(i): 
    return i.lo + (i.hi - i.lo)*rand()
  def log(i): 
    return Num()

"""

Note the brevity of this code. Lesson:
you can write your own variants of the _In_ generator
to handle different distributions.
These variants can be used to create generators for 
model attribute values (see below).

### Models

The following models return generators for attribute values
divided into independent values (in "_x_") and
dependent values (in "_y_").

"""

class Schaffer(Model):
  def spec(i):
    return o(x= [In(-5,5,0)],
             y= [i.f1,i.f2])
  def f1(i,it):
    x=it.x[0]; return x**2
  def f2(i,it):
    x=it.x[0]; return (x-2)**2

class ZDT1(Model):
  def spec(i):
    return o(x= [In(0,1,z) for z in range(30)],
              y= [i.f1,i.f2])
  def f1(i,it):
    return it.x[0]
  def f2(i,it):
    return 1 + 9*sum(it.x[1:]) / 29

if __name__ == "__main__": eval(cmd())
