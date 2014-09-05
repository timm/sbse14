"""

## Basic Stuff

General utils- should be useful for all Python programs.

## Standard Header

"""
from __future__ import division
import sys, random, math, datetime, time,re
sys.dont_write_bytecode = True
"""
## Misc Stuff

### Options Handling

Place to store things and stuff.

_IDIOM_: every time you run an optimizer, show a
dump of the options used in that run.  

_TRICK_: store the options in a nested anonymous
container.

"""
class o: 
  "Peter Norvig's trick for anonymous containers."
  def __init__(i,**d): i.__dict__.update(d)
"""

For example, here are the options used in this code.

"""
The= o(cache = 
          o(keep    = 128 # size of sample sace
           ,pending = 4
          ),
       sa =   
          o(cooling = 0.6  # cooling schedule
           ,kmax    = 1000 # max evals
           ,patience= 250  # run for at least this long
           ,baseline= 100  # initial sample size 
          ),
       misc = 
          o(verbose = True # show stuff?
           ,epsilon = 1.01 # where is close, close enough
           ,seed    = 1    # random number seed
           ,era     = 25   # pause every end of era
           ,copyleft = """                                     _
                                    (_)
              |    .
          .   |L  /|   .          _
      _ . |\ _| \--+._/| .       (_)
     / ||\| Y J  )   / |/| ./
    J  |)'( |        ` F`.'/        _
  -<|  F         __     .-<        (_)
    | /       .-'. `.  /-. L___       
    J \      <    \  | | O\|.-'  _   
  _J \  .-    \/ O | | \  |F    (_) 
 '-F  -<_.     \   .-'  `-' L__    
__J  _   _.     >-'  )._.   |-'  
`-|.'   /_.           \_|   F    
  /.-   .                _.<     
 /'    /.'             .'  `\     
  /L  /'   |/      _.-'-\ 
 /'J       ___.---'\|
   |\  .--' V  | `. `
   |/`. `-.     `._)
      / .-.\ 
VK    \ (  `\ 
       `.\ 

SEARCH-BASED SE Tools
(c) 2014, copyright BSD-3, Tim Menzies

"""
          )
       )
"""

Here's code to dump nested containers:

"""
def showd(d,lvl=0): 
  d = d if isinstance(d,dict) else d.__dict__
  after, line,gap = [], '', '    ' * lvl
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
"""

The above code displays _showd(The)_ as follows:

    :cache
        :keep 128 :pending 4 
    :misc
        :epsilon 1.01 :era 25 :seed 1 :verbose True 
    :sa
        :baseline 100 :cooling 0.6 :kmax 1000 :patience 250 

### Random Stuff

"""
rand=  random.random # generate nums 0..1
any=   random.choice # pull any from list

def rseed(seed = None):
  seed = seed or The.misc.seed
  random.seed(seed)
"""

The above example shows a use of a global option.
Note that the following alternative for _rseed()_ 
would be buggy (since this alternate _rseed_ 
could very well use the 
_The.misc.seed_ known at load time and not some
seed you change at run time).

    def rseed(seed = The misc.seed): # do not
      random.seed(seed)              # do this

### Maths Stuff

"""
def log2(num): 
  "Log base 2 of number"
  return math.log(num)/math.log(2)

def norm(x,lo,hi):
  "Generate a num 0..1 for lo..hi"
  tmp = (x - lo) / (hi - lo + 0.00001) 
  return max(0,min(tmp,1))

def mron(x,lo,hi):
  "Generate a num 1..0 for lo..hi"
  return 1 - norm(x,lo,hi)
"""

### Printing stuff

"""
def burp(*lst):  
  "If verbose enabled, print a list of things."
  The.misc.verbose and say(
    ', '.join(map(str,lst)))

nl="\n"
def says(*lst):
  say(' '.join(map(str,lst)))

def say(x): 
  "Print something with no trailing new line."
  sys.stdout.write(str(x)); sys.stdout.flush()

def gn(lst,n):
  "Function to print floats in short form"
  fmt = '%.' + str(n) + 'f'
  return ', '.join([(fmt % x) for x in lst])

def x(n):
  "Shorthand for short floats"
  return ':%3.1f' % n
"""

The following convenience functions print a list
of floats to  0, 2, or 3 decimal places (useful for condensing old reports).

"""
def g0(lst): return gn(lst,0)
def g2(lst): return gn(lst,2)
def g3(lst): return gn(lst,3)
"""

## Coercion

"""
def atom(x):
  "String to number."
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError: return x
"""

### Command line processing ########################

The following code lets you call any function with keyword
defaults.

For example, consider the following function:

"""

def cmdDemo(who='Tim', when=2015, where='Raleigh'):
  says(':who',who,':when',when,':where',where,nl)

"""If this function is in a file with the last line:

    if __name__ == "__main__": eval(cmd())

Then this function can be called as follows:

    % python base.py  when 2010 who Jane

this would print 

    $ python base.py cmdDemo when 1990 who Jane
    :who Jane :when 1990 :where Raleigh 

Note that the arguments are supplied in a different
order to those seen in the function header.  Also,
if you do not mention some argument, it is filled in
from the function defaults.

"""
def cmd(com='say(The.misc.copyleft)'):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(atom(x)) else str(x)  
  thing=None; chars=""; sep=""; keyp=True
  for word in sys.argv[2:]:
    if keyp:
      thing = word
    else:
      chars = chars+sep+thing+' = '+wrap(word)+' '
      sep = ","
    keyp = not keyp
  chars = sys.argv[1] + '( **dict(' + chars + '))'
  print chars
  return chars

def cmdDemo(who='Tim', when=2015, where='Raleigh'):
  says(':who',who,':when',when,':where',where,nl)

if __name__ == "__main__": eval(cmd())
