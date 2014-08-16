"""
lib.py: misc python tricks
Copyright (c) 2014 tim.menzies@gmail.com

/\_ \    __   /'___\         
\//\ \  /\_\ /\ \__/    __   
  \ \ \ \/\ \\ \ ,__\ /'__`\ 
   \_\ \_\ \ \\ \ \_//\  __/ 
   /\____\\ \_\\ \_\ \ \____\
   \/____/ \/_/ \/_/  \/____/
                       
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and
associated documentation files (the "Software"), to
deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission
notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.""" 

# embarrassment: this is based on a version of life
# i found on the web... but now I can't recall the 
# source. Anyone care to take credit?

def life(seed=1,generations=500,
         width=40,height=40,
         prob=0.15,wait=0.1):
  import numpy,os,time,random
  if seed: random.seed(seed)
  def pause(): time.sleep(wait)
  def clear(): os.system('cls' if 
               os.name == 'nt' else 'clear')
  def stars(x): return "*" if x==1 else " "
  def play_life(a,width=10,height=10):
    xmax, ymax = a.shape
    sum=numpy.sum
    b = a.copy() # copy grid & Rule 2
    for x in range(xmax):
      for y in range(ymax):
        n = sum(a[max(x-1,0):min(x+2,xmax), 
                  max(y-1,0):min(y+2,ymax)]
                ) - a[x, y]
        if a[x, y]:
          if n < 2 or n > 3:
            b[x, y] = 0 # Rule 1 and 3
        elif n == 3:
          b[x, y] = 1 # Rule 4
    return(b)
  def randoms(p):
    for line in life:
      for n in range(len(line)):
        if line[n] != 1:
          line[n] = (0 if random.random() > p 
                     else 1)
  life = numpy.zeros((width, height), 
                     dtype=numpy.byte)
  randoms(prob)
  for i in range(generations+1):
    clear()
    print "generation:", i,"of",\
          generations,"from",seed,"\n"
    life = play_life(life)
    print ""
    for line in life: 
      print ' '.join(map(stars,line))
    randoms(prob/1000.0) 
    pause()

if __name__ == '__main__': life()
