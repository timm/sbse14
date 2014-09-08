

"""

## Analysis of Experimental Data

This page is about the non-parametric a12 test. It is also a chance for us to discuss a little
statistical theory.

### Standard Header

"""
from __future__ import division
import  sys
sys.dont_write_bytecode = True
from base  import *
"""

## Background


For the most part, we are concerned with very high-level issues that
strike to the heart of the human condition:

-   What does it mean to find controlling principles in the world?
-   How can we find those principles better, faster, cheaper?

But sometimes we have to leave those lofty heights to discuss more
pragmatic issues. Specifically, how to present the results of an
optimizer and, sometimes, how to compare and rank the results from
different optimizers.

Note that there is no best way, and often the way we present results
depends on our goals, the data we are procesing, and the audience we are
trying to reach. So the statistical methods discussed below are more
like first-pass approximations to something you may have to change
extensively, depending on the task at hand.

In any case, in order to have at least one report that that you quickly
generate, then....

### Theory


The test that one optimizer is better than another can be recast as four
checks on the *distribution* of performance scores.

1.  Visualize the data, somehow.
2.  Check if the central tendency of one distribution is *better* than
    the other; e.g. compare their median values.
3.  Check the different between the central tendencies is not some
    *small effect*.
4.  Check if the distributions are *significantly different*;


The first step is very important. Stats should always be used as sanity
checks on intuitions gained by other means. So look at the data before
making, possibly bogus, inferences from it. For example, here are some
charts showing the effects on a population as we apply more and more of
some treatment. Note that the mean of the populations remains unchanged,
yet we might still endorse the treatment since it reduces the
uncertainty associated with each population.

[[etc/img/index_customers_clip_image002.jpg]]

Note that 2 and 3 and 4 must be all be true to assert that one thing
generates better numbers than another.  For example, one bogus
conclusion would be to just check median values (step2) and ignore
steps3 and steps4. _BAD IDEA_. Medians can be very misleading unless
you consider the overall distributions (as done in step3 and step4).

(As an aside, note that the above requests a check for _median_,
not _mean_. This is required since, all things considered,
means do not mean much, especially for highly skewed distributions.
For example, Bill Gates and 35 homeless people are in the same room.
Their mean annual income is over a billion dollars each- which is
a number that characterized neither Mr. Gates or the homeless people.
On the other hand, the median income of that population is close to zero-
which is a number that characterizes most of that population. )

In practice, step2,step3,step4 are
listed in increasing order of effort (e.g. the _bootstrap sample_ method
discussed later in this subject is an example of step4, and this
can take a while to compute). So pragmatically, it is useful
to explore the above in the order step1 then step2 then step3 then step4 (and _stopping_
along the way if any part fails). For example, 
one possible bogus inference would be to apply step4 without
the step3 since if the *small effect* test fails, then the third
*significance* test is misleading.
 For example, returning to the above distributions, note the large
overlap in the top two curves in those plots. When distributions exhibit
a very large overlap, it is very hard to determine if one is really
different to the other. So large variances can mean that even if the
means are *better*, we cannot really say that the values in one
distribution are usually better than the other.

### Step1: Visualization


Suppose we had two optimizers which in a 10 repeated runs generated
performance from two models:

        1:       def _tile2():
        2:         def show(lst):
        3:            return xtile(lst,lo=0, hi=1,width=25,
        4:                         show= lambda s:" %3.2f" % s)
        5:         print "one", show([0.21, 0.29, 0.28, 0.32, 0.32, 
        6:                            0.28, 0.29, 0.41, 0.42, 0.48])
        7:         print "two", show([0.71, 0.92, 0.80, 0.79, 0.78, 
        8:                            0.9,  0.71, 0.82, 0.79, 0.98])

When faced with new data, always chant the following mantra:

-   *First* visualize it to get some intuitions;
-   *Then* apply some statistics to double check those intuitions.

That is, it is *strong recommended* that, prior doing any statistical
work, an analyst generates a visualization of the data. Percentile
charts a simple way to display very large populations in very little
space. For example, here are our results from *one*, displayed on a
range from 0.00 to 1.00.

    one         * --|            , 0.28,  0.29,  0.32,  0.41,  0.48
    two             |    -- * -- , 0.71,  0.79,  0.80,  0.90,  0.98

In this percentile chart, the 2nd and 3rd percentiles as little dashes
left and right of the median value, shown with a *"\*"*, (learner
*two*'s 3rd percentile is so small that it actually disappears in this
display). The vertical bar *"|"* shows half way between the display's
min and max (in this case, that would be (0.0+1.00)/2= 0.50)


#### Xtile

The advantage of percentile charts is that we can show a lot of data in
very little space. 

For example, here's an example where the _xtile_ Python function
shows 2000 numbers on two lines:

-   Quintiles divide the data into the 10th, 30th, 50th, 70th, 90th
    percentile.
-   Dashes (*"-"*) mark the range (10,30)th and (70,90)th percentiles;
-   White space marks the ranges (30,50)th and (50,70)th percentiles.

Consider two distributions, of 1000 samples each: one shows square root
of a *rand()* and the other shows the square of a *rand()*.

       10:       def _tile() :
       11:         import random
       12:         r = random.random
       13:         def show(lst):
       14:           return xtile(lst,lo=0, hi=1,width=25,
       15:                        show= lambda s:" %3.2f" % s)
       16:         print "one", show([r()*0.5 for x in range(1000)])
       17:         print "two", show([r()2   for x in range(1000)])

In the following quintile charts, we show these distributions:

-   The range is 0 to 1.
-   One line shows the square of 1000 random numbers;
-   The other line shows the square root of 1000 random numbers;

Note the brevity of the display:

    one        -----|    *  ---  , 0.32,  0.55,  0.70,  0.84,  0.95
    two --    *     |--------    , 0.01,  0.10,  0.27,  0.51,  0.85

As before, the median value, shown with a *"\*"*; and the point half-way
between min and max (in this case, 0.5) is shown as a vertical bar
*"|"*.

### Step2: Check Medians

The median of a list is the middle item of the sorted values, if the list is of an odd size.
If the list size is even, the median is the two values either side of the middle:

    def median(lst,ordered=False):
      lst = lst if ordered else sorted(lst)
      n   = len(lst)
      p   = n // 2
      if (n % 2):  return lst[p]
      p,q = p-1,p
      q   = max(0,(min(q,n)))
      return (lst[p] + lst[q]) * 0.5

### Step3: Effect size

An _effect size_ test is a sanity check that can be summarizes as follows:

* Don't  sweat the small stuff; 

I.e. ignore small differences between items in the samples.

 My
preferred test for *small effect* has:

-   a simple intuition;
-   which makes no assumptions about (say) Gaussian assumptions;
-   and which has a solid lineage in the literature.

Such a test is [Vargha and Delaney][vd00]'s A12 statistic.
 The statistic was
proposed in Vargha and Delaney's 2000 paper was endorsed in many places
including in [Acruci and Briad][ab11]'s ICSE 2011 paper.
After I describe it to you, you will wonder why anyone would ever want
to use anything else.

[vd00]: http://jeb.sagepub.com/content/25/2/101.short   "A. Vargha and H. D. Delaney. A critique and improvement of the CL common language effect size statistics of McGraw and Wong. Journal of Educational and Behavioral Statistics, 25(2):101-132, 2000"

[ab11]: http://goo.gl/4N34gk   "Andrea Arcuri, Lionel C. Briand: A practical guide for using statistical tests to assess randomized algorithms in software  engineering. ICSE 2011: 1-10"

 Given a performance measure seen in *m* measures
of *X* and *n* measures of *Y*, the A12 statistics measures the
probability that running algorithm *X* yields higher values than running
another algorithm *Y*. Specifically, it counts how often we seen larger
numbers in *X* than *Y* (and if the same numbers are found in both, we
add a half mark):

     a12= #(X.i > Y.j) / (n*m) + .5#(X.i == Y.j) / (n*m)

According to Vargha and Delaney, a small, medium, large difference
between two populations is:

-   *large* if `a12` is over 71%;
-   *medium* if `a12` is over 64%;
-   *small* if `a12` is 56%, or less.

A naive version of this code is shown here in the _ab12slow_ function. While simple to
code, this _ab12slow_ function runs in polynomial time (since for each item in _lst1_,
it runs over all of _lst2_):

"""
def _ab12():
  def a12slow(lst1,lst2):
    more = same = 0.0
    for x in sorted(lst1):
      for y in sorted(lst2):
        if   x==y : 
          same += 1
        elif x > y : 
          more += 1
    return (more + 0.5*same) / (len(lst1)*len(lst2))
  random.seed(1)
  l1 = [random.random() for x in range(5000)]
  more = [random.random()*2 for x in range(5000)]
  l2 = [random.random()  for x in range(5000)]
  less = [random.random()/2.0 for x in range(5000)]
  for tag, one,two in [("1less",l1,more), 
                       ("1more",more,less),("same",l1,l2)]:
    t1  = msecs(lambda : a12(l1,less))
    t2  = msecs(lambda : a12slow(l1,less))
    print "\n",tag,"\n",t1,a12(one,two)
    print t2, a12slow(one,two)
"""

A faster way is to first sort the two lists in descending order. Then, if it is found that an item
is bigger that one item, it is by definition bigger than the rest of the items in that list (so
we can stop there): 

"""
def a12(lst1,lst2):
  """how often is lst1 often more than y in lst2?
  assumes lst1 nums are meant to be greater than lst2"""
  def loop(t,t1,t2): 
    while t1.m < t1.n and t2.m < t2.n:
      h1 = t1.l[t1.m]
      h2 = t2.l[t2.m]
      h3 = t2.l[t2.m+1] if t2.m+1 < t2.n else None 
      if h1 > h2:
        t1.m  += 1; t1.gt += t2.n - t2.m
      elif h1 == h2:
        if h3 and gt(h1,h3) < 0:
            t1.gt += t2.n - t2.m  - 1
        t1.m  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1,reverse=True)
  lst2 = sorted(lst2,reverse=True)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = o(l=lst1,m=0,eq=0,gt=0,n=n1)
  t2   = o(l=lst2,m=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)
"""

Note that the test code \__ab12_ shows that our fast and slow method generate the same A12 score, but the
fast way does so thousands of times faster. The following tests show runtimes for lists of 5000 numbers:

    experimemt  msecs(fast)  a12(fast)  msecs(slow)  a12(slow)
    1less          13        0.257      9382           0.257  
    1more          20        0.868      9869           0.868
    same           11        0,502      9937           0.502


### Statistical Tests

Next time!

"""

if __name__ == "__main__": eval(cmd())
