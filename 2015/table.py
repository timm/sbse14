from __future__ import division
import sys,random,math,re
sys.dont_write_bytecode = True

class o():
  "Anonymous container"
  def __init__(i,**fields): i.has().update(fields)
  def has(i)              : return i.__dict__
  #def __getattr__(i,k)    : return i.__dict__[k]
  #def __setattr__(i,k,v)  : i.__dict__[k] = v; return v
  def __repr__(i):
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,i.has()[k]) 
                     for k in i.public()])+ '}'
  def public(i):
    return [k for k in sorted(i.has().keys()) 
            if not "_" in k]

about = classmethod

akos = dict(nums   = r'^[\$<>]',
            syms   = r'^[^\$<>]',
            klass  = r'^[=]',
            indep  = r'^[^<>=]',
            dep    = r'^[=<>]',
            less   = r'^[<]',
            more   = r'^[>]',
            ignore = r'^[/]')

class Log:
  def __repr__(i): return '%s(%s,%s)' % (i.__class__.__name__,i.txt,i.col)
  def log(i,val): pass
  def __init__(i,txt="",col=None,w=1):
    i.txt, i.col,i.w=txt,col,w
class Num(Log): pass
class Thing(Num): pass
class Sym(Log): pass

class Row:
  fields = {'gender'    :Sym,
            'age'       :Num,
            '$shoesize' :Num,
            '>lifeExpectancy':Thing}
  
seen=re.match

def complete(klass):
  skip="\?"
  klass.cols = o()
  cols = klass.cols.has()
  for ako in akos.keys(): 
    cols[ako]=[]
  cols["eden"] = []
  for c,(name,klass) in enumerate(klass.fields.items()):
    if not seen(skip, name):
      cols["eden"] += [(c,name,klass)]
      for ako,pattern in akos.items():
        if seen(pattern,name):
          cols[ako] += [c]
  return klass

class Table:
  def __init__(i,about):
    i.about   = complete(about)
    i.rows    = []
    i.cols = i.headers0(about.cols.eden)
  def headers0(i,pairs):
    return [klass(name,c) for 
            c,name,klass in pairs]
  def cellhead(i,row,*whats):
    for what in whats:
      return row[c],i.headers[c]
  def log(i,row):
    for h in i.headers:
      h.log(row[h.col])
        
tbl = Table(Row)
print tbl.cols
print tbl.about.cols
