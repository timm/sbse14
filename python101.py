"""## Some Python Tricks

Some of my fav short Python tricks. No real theme, just added
if brief and cool.

Code comes with test samples (see the _@test_ entries, below).


## Code for Demonstrations and Tesing

### Demo

Trapping a set of demos.

If called with no arguments, it runs all the trapped
demos.

If called with no arguments _demo('-h')_, then it is
prints a list of the demos.

If called as a decorator, it traps the decorated
function. e.g.

    @demo
    def demoed(show=1):
      "Sample demo."
      print show/2

"""
def demo(f=None,demos=[]): 
  def demoDoc(d):
    return '# '+d.__doc__+"\n" if d.__doc__ else ""  
  if f == '-h':
    for d in demos: 
      print d.func_name+'()', demoDoc(d)
  if f: demos.append(f); return f
  s='|'+'='*40 +'\n'
  for d in demos: 
    print '\n==|',d.func_name,s,demoDoc(d),d()
"""

### Test

Run a set of tests, each of which returns a pair of
_want,got_.  Counts the number of time a test
is "passed" (i.e. _want == got_) or "failed"
(i.e. _want != got_).

If called with no arguments, it runs all the tests.

If called as a decorator, it traps the test.

"""
def test(f=None,cache=[]):
  if f: 
    cache += [f]
    return f
  ok = no = 0
  for t in cache: 
    print '#',t.func_name ,t.__doc__ or ''
    prefix, n, found = None, 0, t() or []
    while found:
      this, that = found.pop(0), found.pop(0)
      if this == that:
        ok, n, prefix = ok+1, n+1,'# CORRECT :'
      else: 
        no, n, prefix = no+1, n+1,'# WRONG   :'
      print prefix,t.func_name,'test',n
  if ok+no:
    print '\n# Final score: %s/%s = %s%% CORRECT' \
           % (ok,(ok+no),int(100*ok/(ok+no)))
"""

E.g.

"""
@test
def tested0():
  "Demo of a failing test"
  return [False,True]

@test
def tested1():
  "Demo of basic testing."
  return [True,True,  # should pass
          1, 2/2]     # should pass
"""

If the _test()_ is called after the above then we will see

     tested1 Demo of basic testing.
     CORRECT: tested1 test 1
     WRONG  : tested1 test 2
     CORRECT: tested1 test 3
     # tested2 Yet another demo of basic testing.
     WRONG  : tested2 test 1
      
     # Final score: 2/4 = 50% CORRECT

## Type Coercion

### Atom

Converts strong to an int or a float.

"""
def atom(x):  
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x

@test
def atomed():
  return [1,atom("1")]
"""

## Maths Stuff

"""
def median(lst,ordered=False):
  lst = lst if ordered else sorted(lst)
  n   = len(lst)
  p   = n // 2
  if (n % 2):  return lst[p]
  p,q = p-1,p
  q   = max(0,(min(q,n)))
  return (lst[p] + lst[q]) * 0.5

@test
def _median():
  print median([1,2,3,4,5])
  print median([1,2,3,4])

"""

## Random Stuff

Standard headers for random stuff

"""
import random,re
any = random.uniform 
seed  = random.seed
"""

### Sometimes

Returns True at probability 'p'.

"""
def sometimes(p) : 
  return p > any(0,1)
"""

### Some

Returns 'p'% of a list,selected at random.

"""
def some(lst,p=0.5)  : 
  return [x for x in lst if sometimes(p)]
"""

### One

Returns one item in a list, selected at random.

"""
def one(lst): 
  return lst[  int(any(0,len(lst) - 1)) ] 
"""

Random tests:

"""
@test
def randomed():
  seed(1)
  lst = list("mkbcdefgh")
  return ["k",one(lst)
         ,['b', 'c', 'd', 'g', 'h'], some(lst)
         ]

"""

## Iterators

### Item

Return all non-list items in a nested list.

"""
def item(x) : 
  if isinstance(x,(tuple,list)):
    for y in x:
      for z in item(y): yield z
  else: yield x

@test
def itemed():
  return [19,
          sum(x for x in item([1,[[3,4],5],[6]]))]
"""

### Cycle

Returns an infinite number of items from a list, 
in a random order. Warning: never terminates!
 
"""
def cycle(lst,max=10**32):
  while True and max > 0:
    random.shuffle(lst)
    for i in lst:
      yield i
      max -= 1
      if max < 0: break

@test
def cycled():
  seed(1)
  return [[2,5,3,4,1,2,1,4,5,3,1,5,4,3,2,2,4,5,1,3]
        ,[x for x in cycle([1,2,3,4,5],20)]]
"""

### Pairs

Returns first and second item,
   then second and third, 
   then third and fourth...
 
e.g. to track changes in slopes

    for now,next in pairs([1,2,3,4,5]): 
        print "Delta", (now-next)/now

Code:
"""
def pairs(lst):
  last=lst[0]
  for i in lst[1:]:
    yield last,i
    last = i

@test
def paired():
  return [2.5,
          sum([(y-x)*1.0/x for x,y 
               in pairs([10,20,20,20,10,30])])]
"""

### Rows

Iterator file. Skips blanks likes. Splits
     other lines into one list per line (dividing on
     commas. Removes all whitespace. Filters
     all cells via 'wrapper'.  

E.g. to read a csv file
    that may contain numbers 

    for n,cells in rows("mediate.csv",atom): 
             print cells[0]+ cells[-1]

Code:
"""
def noop(x): return x

def rows(file, n=0, bad=r'["\' \t\r\n]',sep=',',wrapper=noop) :
  for line in open(file,'r') :
    n += 1
    line = re.sub(bad,"",line).split(sep)
    if line: 
        yield n,map(wrapper,line)
"""

### Often

Generate often seen things most often 
while generating rarer this more rarely.

Given a dictionary d{k1=n1, k2=n2, ...},
  return enough keys ki at probability 
  pi = ni/n where n = n1+n2+..
  e.g.

     for key in some({'box':30,'circle':20,'line':10},20)
         print key
  
will return around twice as many boxes as anything else,
  circles 1/3rd of the time and lines 1/6th of the time. 


"""
def often(d,enough=10**32):
  n, lst = 0, []
  for x in d: 
    n   += d[x]
    lst += [(d[x],x)]
  lst = sorted(lst, reverse=True)
  while enough > 0:
    r = random.random()
    for freq,thing in lst:
      r -= freq*1.0/n
      if r <= 0:
        yield thing
        enough -= 1
        break

@test
def oftend():
  seed(1)
  return [['box','line',  'circle','box','box', 
           'box','circle','circle','box','box'],
          [x for x in 
           often({'box':30,'circle':20,'line':10},
                 10)]]
"""

### And Finally...

Lets see how all that runs:

"""
test()
