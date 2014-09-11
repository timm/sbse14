class o():
  def __init__(i,**d): i.has().update(d)
  def has(i)         : return i.__dict__
  def __repr__(i)    : return showd(i.has(),
                                i.__class__.__name__)
   
def showd(d,name=""):
   def show(i): return [k for k in sorted(d.keys()) 
                        if not "_" in k]
   return name+'{'+' '.join([ ':%s %s' % (k,i.d[k])
                           for k in i.show()])) + '}'
 
class Close():
  enough = 20
  tiny   = 0.05
  def __init__(i):
    i.sum = [0.0] * 32
    i.pop = [0.0] * 32
  def keep(i,x):
    for j in xrange(len(i.sum)):
      i.sum[j] += x
      i.pop[j] += 1
      mu   = i.sum[j] / i.pop[j]
      here = i.pop[j] / i.pop[0]
      if i.pop[j] < Close.enough:
        return False
      if here < Close.tiny:
        return True
      if x > mu:
        return False 

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

def lohi(tbl):
  def keep(col,x):
    lo[col] = min(lo[col], x)
    hi[col] = max(hi[col], x)
    return n
  def norm(col,x):
    return (x - lo[col])/(hi[col] - lo[col] + 0.0001)
  lo = [ 10**32] * len(tbl.indep)
  hi = [-10**32] * len(tbl.indep)
  for n,row in enumerate(tbl.data):
    tbl.data[n] = [keep(col,x) 
                   for col,x in enumerate(row)] 
  for n,row in enumerate(tbl.data):
    tbl.data[n] = [norm(col,x) 
                   for col,x in enumerate(row)] 
  return tbl

@lohi
def nasa93():
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return o(
    sfem  = 21,
    kloc  = 22,
    klass = 23,
    indep = range(klass)
    names = [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc', 'effort', '?defects', '?months'],
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
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0],
	])



_close()
