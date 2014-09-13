from __future__ import division
import re,sys,random
sys.dont_write_bytecode = True

logo="""
        _.._.-..-._
     .-'  .'  /\  \`._
    /    /  .'  `-.\  `.
        :_.'  ..    :       _.../\ 
        |           ;___ .-'   //\\.
         \  _..._  /    `/\   //  \\\ 
          `-.___.-'  /\ //\\       \\:
               |    //\V/ :\\       \\ 
                \      \\/  \\      /\\ 
                 `.____.\\   \\   .'  \\ 
                   //   /\\---\\-'     \\ 
             fsc  //   // \\   \\       \\ 

 DeadAnt (c) 2014, Tim Menzies
 Tabu-based ant colony optimizer.
 """

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

The = o(cache = o(keep=256),
        misc= o(fred=1,
                jane=2,
                maths=o(ll=1,
                        mm=3)))

def pretty(d, indent=0):
  for key, value in d.items():
    if key[0] != "_":
      print '    ' * indent + str(key)
      if isinstance(value, (dict,o)):
         pretty(value, indent+1)
      else:
         print '    ' * (indent+1) + str(value)

rand = random.random
any  = random.choice
def say(*lst):
  sys.stdout.write(','.join(lst))

nl="\n"

def cmd(com="say(logo)"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  def value(x):
    try:    return eval(x)
    except: return x
  def pair(x):
    lst = re.split("=",x)
    return lst[0] +"="+ wrap(value(lst[1]))
  words = map(pair, sys.argv[2:])
  return sys.argv[1]+'(**dict('+ ','.join(words)+'))'

class Close():
  big, tiny = 20, 0.05
  def __init__(i):
    i.sum, i.n = [0.0]*32, [0.0]*32
  def keep(i,x):
    for j in xrange(len(i.sum)):
      i.sum[j] += x
      i.n[j]   += 1
      mu        = i.sum[j] / i.n[j]
      here      = i.n[j]  / i.n[0]
      if i.n[j] < Close.big  : return False
      if here   < Close.tiny : return True
      if x > mu              : return False 

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

class Header(o): 
  id=0
  def __init__(i,name=None):
    if not name:
      id   = Header.id = Header.id + 1
      name = 'var%s' % id
    i.skip, i.name = False, name
  def __repr__(i):
    return i.__class__.__name__+'('+i.name+')'
  def clone(i):
    return i.__class__(name=i.name)
class Num(Header): 
  def __init__(i, name=None):
     super(Num,i).__init__(name=name)
     i.lo, i.hi = 10**32, -10**32
     i.cache = Cache()
  def log(i,x):
    i.lo = min(i.lo,x)
    i.hi = max(i.hi,x)
    i.cache += x
    return x
  def ako(i): 
    return ['nums','indep']
  def any(i):
    return i.lo + (i.hi - i.lo)*rand()
class Less(Num):
  def ako(i): return ['nums','less','depen']
class More(Num):
  def ako(i): return ['nums','more','depen']
 
def Skip(x):
  x.skip=True
  return x

class Sym(Header):
  def __init__(i,name=None,items=[]):
    super(Sym,i).__init__(name=name)
    i.n,i.counts,i.most,i.mode=0,{},0,None
    i._report=None
    i.items=items
  def clone(i):
    return Sym(name=i.name,items=i.items)
  def ako(i): return ['syms','indep']
  def log(i,x):
    i.n += 1
    n= i.counts[x] = i.counts.get(x,0) + 1
    if n > i.most:
      i.most, i.mode = n, x
    return x
  def any(i):
    return any(i.counts.keys())
  def has(i):
    if i._report == None: i._report = i.report()
    return i._report
  def report(i):
    lst = [(v/i.n,k) for k,v in i.counts.items()]
    i._report = sorted(lst,reverse=True)
    
class Klass(Sym):
  def ako(i): return ['syms','depen']

class Cache():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[]):
    i._lst,i.n,i._report = [],0,None
    map(i.__iadd__,inits)
  def __iadd__(i,x): 
    if x == None: return x 
    i.n += 1
    changed = False
    if len(i._lst) < The.cache.keep: # not full
      changed = True
      i._lst += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._lst[int(rand()*The.cache.keep)] = x
    if changed:      
      i._report = None
    return i
  def any(i):  
    return  any(i._lst)
  def has(i):
    if i._report == None: i._report = i.report()
    return i._report
  def norm(i,x):
    lo, hi = i.has().lo, i.has().hi
    return (x - lo) / (hi - lo + 0.00001)
  def report():
    i._lst = sorted(i._lst)
    n   = len(lst)     
    return o(
      median= median(i._lst),
      iqr = i._lst[int(n*.75)] - i._lst[int(n*.5)],
      lo  = i._lst[0], 
      hi  = i._lst[-1])

def median(lst):
  n = len(lst)
  p = n // 2
  if (n % 2):  return lst[p]
  q = p + 1
  q = max(0,(min(q,n)))
  return (lst[p] + lst[q])/2

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

class Lh(Sym):
  def __init__(i,name=None):
    super(Lh,i).__init__(name=name,
                         items=[1,2,3,4,5,6])
def nasa93():
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return Table(
    header = [ 
     # 0..8
     Lh('Prec'), Lh('Flex'), Lh('Resl'), Lh('Team'),  
     Lh('Pmat'), Lh('rely'), Lh('data'), Lh('cplx'),  
     Lh('ruse'), Lh('docu'), Lh('time'), Lh('stor'),  
     Lh('pvol'), Lh('acap'), Lh('pcap'), Lh('pcon'),  
     Lh('aexp'), Lh('plex'), Lh('ltex'), Lh('tool'),  
     Lh('site'), Lh('sced'), Num('kloc'),Less('effort'),  
     Skip(Less('defects')),  Skip(Less('months'))
    ],
    data=[
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
	[h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28.0],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16.0],
	[h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
	[h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12.0],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
	[h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
	[h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
	[h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
	[h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
	[h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
	[h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
	[h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
	[h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
	[h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
	[h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
	[h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
	[h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
	[h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
	[h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25.0],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
	[h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
	[h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
	[h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
	[h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
	[h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
	[h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
	[h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
	[h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
	[h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
	[h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
	[h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23.0],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
	[h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
	[h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  6.2, 12,477,15.4],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0]	
  ])



print nasa93().any()
print "why the ignored filled in"


if __name__ == '__main__': eval(cmd())
