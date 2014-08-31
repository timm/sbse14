"""
# SA (plus tricks)

Timm tricks for building an optimization.

To illustrate the tricks, they are applied to 
build a simulated annealer.

## Standard Headers

Here we see some standard Pythin file startups

"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True


"""
Place to store things and stuff 
"""

class o: 
  def __init__(i,**d): i.__dict__.update(d)

"""
Place to store options 
"""


The = o(cache= o(keep    = 128,
                 pending = 4),
        misc = o(verbose = True,
                 epsilon = 1.01,
                 seed    = 1,
                 era     = 25),
        sa =   o(cooling = 0.6,
                 kmax    = 1000,
                 patience= 250,
                 baseline= 100))

### Misc utils #####################################
rand=  random.random
any=   random.choice
rseed= random.seed

def log2(x): return math.log(x)/math.log(2)
def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()

def showd(d,lvl=0): 
  d = d if isinstance(d,dict) else d.__dict__
  after, line,gap = [], '', '\t' * lvl
  for k in sorted(d.keys()):
    if k[0] == "_": continue
    val = d[k]
    if isinstance(val,(dict,o)):
       after += [k]
    else:
      if callable(val):
        val = val.__name__
      line += (':%s %s ' % (k,val))
  print gap + line
  for k in after: 
      print gap + (':%s' % k)
      showd(d[k],lvl+1)

def g3(lst): return gn(lst,3)
def g2(lst): return gn(lst,2)
def g0(lst): return gn(lst,0)

def gn(lst,n):
  fmt = '%.' + str(n) + 'f'
  return ', '.join([(fmt % x) for x in lst])

def norm(x,lo,hi):
  tmp = (x - lo) / (hi - lo + 0.00001) 
  return 1 - max(0,min(tmp,1))

def x(n): return ':%3.1f' % n

def burp(*lst):  
  The.misc.verbose and say(
    ', '.join(map(str,lst)))

def study(f):
  """All outputs have date,time, notes,
  a reset of the options,  settings, runtimes."""
  def wrapper(*lst):
    what = f.__name__
    doc  = f.__doc__ 
    if doc:
      doc= re.sub(r"\n[ \t]*","\n# ",doc)
    show = datetime.datetime.now().strftime
    print "\n###",what,"#" * 50
    print "#", show("%Y-%m-%d %H:%M:%S")
    if doc: print "#",doc
    t1 = time.time()
    f(*lst)
    t2 = time.time() 
    print "\n" + ("-" * 50)
    showd(The)
    print "\n# Runtime: %.3f secs" % (t2-t1)
  return wrapper

### Classes ########################################

class Log():
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],label=''):
    i.label = label
    i._cache,i.n,i._report = [],0,None
    i.setup()
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    if x == None: return x
    i.n += 1
    changed = False
    if len(i._cache) < The.cache.keep:
      changed = True
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._cache[int(rand()*The.cache.keep)] = x
    if changed:      
      i._report = None # wipe out 'what follows'
      i.change(x)
    return i
  def any(i):  
    return  any(i._cache)
  def has(i):
    i._report = i._report or i.report()
    return i._report
  def setup(i): pass

class Num(Log):
  def setup(i):
    i.lo, i.hi = 10**32, -10**32
  def change(i,x):
    i.lo = min(i.lo, x)
    i.hi = max(i.hi, x)
  def norm(i,x):
    return (x - i.lo)/(i.hi - i.lo + 0.000001)
  def report(i):
    lst = i._cache = sorted(i._cache)
    n   = len(lst)     
    return o(
      median= i.median(),
      iqr   = lst[int(n*.75)] - lst[int(n*.5)],
      lo    = i.lo, 
      hi    = i.hi)
  def ish(i,f=0.1): 
    return i.any() + f*(i.any() - i.any())
  def median(i):
    n = len(i._cache)
    p = n // 2
    if (n % 2):  return i._cache[p]
    q = p + 1
    q = max(0,(min(q,n)))
    return (i._cache[p] + i._cache[q])/2

class Sym(Log):
  def setup(i):
    i.counts,i.mode,i.most={},None,0
  def change(i,x):
    c= i.counts[x]= i.counts.get(x,0) + 1
    if c > i.most:
      i.mode,i.most = x,c
  def report(i):
     return o(dist= i.dist(), 
              ent = i.entropy(),
              mode= i.mode)
  def dist(i):
    n = sum(i.counts.values())
    return sorted([(d[k]/n, k) for 
                   k in i.counts.keys()], 
                  reverse=True)
  def ish(i):
    r,tmp = rand(),0
    for w,x in i.has().dist:
      tmp  += w
      if tmp >= r: 
        return x
    return x
  def entropy(i,e=0):
    for k in i.counts:
      p = i.counts[k]/len(i._cache)
      e -= p*log2(p) if p else 0
    return e    

### Classes ########################################

class In:
  def __init__(i,lo=0,hi=1,txt=""):
    i.txt,i.lo,i.hi = txt,lo,hi
  def __call__(i): 
    return i.lo + (i.hi - i.lo)*rand()
  def log(i): 
    return Num()

class Model:
  def name(i): 
    return i.__class__.__name__
  def __init__(i):
    i.of = i.spec()
    i.log= o(x= [z.log() for z in i.of.x],
              y= [Num()   for _ in i.of.y])
  def indepIT(i):
    "Make new it."
    return o(x=[z() for z in i.of.x])
  def depIT(i,it):
    "Complete it's dep variables."
    it.y = [f(it) for f in i.of.y]
    return it
  def logIT(i,it):
    "Remember what we have see in it."
    for val,log in zip(it.x, i.log.x): log += val
    for val,log in zip(it.y, i.log.y): log += val
  def aroundIT(i,it,p=0.5):
    "Find some place around it."
    def n(val,f): 
      return f() if rand() < p else val
    old = it.x
    new = [n(x,f) for x,f in zip(old,i.of.x)]
    return o(x=new)

#XY = a pair of related indep,dep lists
#it = actual values
#of = meta knowledge of members of it
#log = a record of things seen in it

#seperate (1) guesses indep variables (2) using them to
#calc dep values (3) logging what was picked



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
  sb = s = m.indepIT()
  eb = e = norm(energy(m,s), base.lo, base.hi)
  k = 0
  while k <  The.sa.kmax and more(k,eb):
    if not k % The.misc.era: 
      burp("\n", str(k).zfill(4),x(eb), ' ') 
    k += 1
    mark = "."
    sn = m.aroundIT(s,p=1)
    en = norm(energy(m,sn), base.lo, base.hi)
    if en >  (e * The.misc.epsilon):
      s,e = sn,en
      mark = "+"
    elif maybe(e,en, 
               k/The.sa.kmax**The.sa.cooling):
      s,e = sn,en
      mark = "?"
    if en > (eb * The.misc.epsilon):
      sb,eb = sn,en
      mark = "!"
    burp(mark)
  return sb,eb    

@study
def saDemo(m):
  "Basic study."
  rseed(The.misc.seed)
  print "\n",m.name()
  sb,eb = sa(m)
  x= g3(sb.x)
  y= g3(sb.y)
  print "\n------\n:e",eb,"\n:y",y,"\n:x",x

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


saDemo(Schaffer())
saDemo(ZDT1())
