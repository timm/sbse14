from __future__ import division
import re
sys.dont_write_bytecode = True
from lib import *
from header import *

class Table(o):
  def __init__(i,header=[],data=[]):
    i.cols  = i.headers(header)
    i._data = map(i.log, data)
    i.header = header
  def headers(i,header):
    d = o(all = [])
    for c,h in enumerate(header):
      h.col = c
      d["all"] += [h]
      for ako in h.ako():
        d[ako]  = d.has().get(ako,[]) + [h]
    return d
  def clone(i): 
    header = [h.clone() for h in i.cols.all]
    return Table(header=header)
  def log(i,row):
    return [h.log(row[h.col]) for h in i.cols.all]
  def __iadd__(i,row):
    i._data += [i.log(row)]
    return i
  def any(i):
    out = [None]* len(i.cols.all)
    for h in i.cols.indep:
      out[h.col] =  h.any()
    return out


