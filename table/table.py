from __future__ import division
from lib import *
sys.dont_write_bytecode = True
from header import *

class Table(o):
  def __init__(i,header=[],data=[]):
    i.cols  = i.headers(header)
    i._data = map(i.log, data)
    i.header= header
  def headers(i,header):
    d = o(all = [])
    what = None
    for c,h in enumerate(header):
      words = re.split(':',h)
      if not words[0]:
        name = words[-1]
      else:
        what,name = words[0],words[-1]
      if not what in Ako.keys():
        print h
        print "Do not know [%s]." % what
        exit()
      it = klass = Ako[what]()(name)
      if it.skip: 
        continue
      it.col = c
      d["all"] += [it]
      for ako in it.ako():
        d[ako] = d.has().get(ako,[]) + [it]
    return d
  def clone(i): 
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

def dist(tbl,row1,row2):
  cols = The.cluster.using(tbl)
  miss = The.misc.missing
  d, n = 0.0, 0.000001
  for header in cols:
    r  = header.col
    v1 = row1[r]
    v2 = row2[r]
    if v1 == v2 == miss: continue
    if v2 != miss: v2 = header.norm(v2)
    if v1 != miss: v1 = header.norm(v1)
    if v1 == miss: v1 = header.far(v2)
    if v2 == miss: v2 = header.far(v1)
    n += header.w
    d += header.dist(v1,v2)
  return d**0.5 / n**0.5

if __name__ == '__main__': eval(cmd())
