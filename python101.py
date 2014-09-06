"""

## Some Python Tricks

Some of my fav short Python tricks. No real theme, just added
if brief and cool.

Warning: dumped in quickly, not tested.

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

## Iterators

### Item

Return all non-list items in a nested list.

"""
def item(x) : 
  if isinstance(x,(tuple,list)):
    for y in x:
      for z in item(y): yield z
  else: yield x
"""

### Cycle

Returns an infinite number of items from a list, 
in a random order. Warning: never terminates!
 
"""
def cycle(lst):
  while True:
    random.shuffle(lst)
    for i in lst:
      yield i
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

### Some

Given a dictionary d{k1=n1, k2=n2, ...},
  return enough keys ki at probability 
  pi = ni/n where n = n1+n2+..
  e.g.

     for key in some({'box':30,'circle':20,'line':10},20)
         print key
  
will return around twice as many boxes as anything else,
  circles 1/3rd of the time and lines 1/6th of the time. 


"""
def some(d,enough=10**32):
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
