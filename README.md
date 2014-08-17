![Rules](etc/rules.png "Timm's rules")
 
tim.menzies@gmail.com  
Aug 9 2014

This code is an instantiation   of the following ideas.

FIRST PRINCIPLES
=================

TISTF: Truth is Shorter than Fiction
-------------------------------------

If you do not understand it, you cannot code it succinctly.
So to check if you understand it, try to code it.

BeValued:
---------

The real worth of a machine is what added value it
gives back to the community. Be valued. Give of
yourself- your wisdom, your tricks, your tips,
captured in code, shared in a publicly accessible repo, 
available for
all.

No man is an _Iland_,  
intire of it selfe;   
every man is a peece of the _Continent_,   
a part of the _maine_;  
if a _Clod_ bee washed away by the _Sea,   
Europe_ is the lesse,   
as well as if a _Promontorie_ were,   
as well as if a _Mannor_ of thy _friends_ or of _thine owne_ were;   
any mans _death_ diminishes _me_,   
because I am involved in _Mankinde_;   
And therefore never send to know for whom the _bell_ tolls;   
It tolls for _thee_.  
-- John Donne, 1623

DOOR SOURCE: OpenSource, OpenDoor, SpecialSauce
---------------------------------------------------

For years and years, I made my money by what I could
give away. I made my code open source so it open
doors to people who, otherwise, might not care
to. Once inside those doors, I earned a living
configuring (adding the special sauce) those the
open tools since, for the tools I created, I was one
of the few people who really understoof the crucial tweaks
that make all the difference.

SHOW OFF:
--------

Code should know how to show off. All files end in

    if __name__ == '__main__': doSomethingCool();

See also _YCYR_.

TTS: Teach the Source:
----------------------

Teach from the code. One lecture = what you can show
students in one hour.

YCYR: Your Code = Your Resume
------------------------------

When going for jobs, imagine sending prospective
employees your Github repo containing impressive
code. Think how much more interested that would make
them.

PYTHON RULES
============

2.7: Two point seven 
--------------------

Use Python 2.7+, not Python 3, since many useful
libraries are NOT yet ported to Python 3. 

Hopefully,  this rule will soon change.
 
ATMC: Add the missing code.
---------------------------

All python files should start with 

    from __future__ import division 
    import sys 
    sys.dont_write_bytecode = True
    """ some copyright notice """
	
Also, as said in _SHOW OFF_, all files should end
with:

	if __name__ == '__main__': doSomethingCool();

BCD: Beware container defaults 
------------------------------

Default params to functions, methods are evaluated
at load time. Which means that N calls to a function
with an argument that defaults to, say, an empty
list will always be talking to the *same* list,
every time you call the function.

IRU: Iterators 'r us
---------------------

Don't understand the following? Then work it out!

    def item(items):
      if isinstance(items,(list,tuple)):
        for one in items:
          for x in item(one):
            yield x
      else:
        yield items


LRU: Lambdas 'r us
-------------------

Anonymous functions (lambdas) rule. Allows for simple
implementation of generics, just by passing in a lambda
body. And stuff like the following is just wicked cool:

    tree = lambda: collections.defaultdict(tree)
    root = tree()
    root['menu']['id'] = 'file'
    root['menu']['value'] = 'File'
    root['menu']['menuitems']['new']['value'] = 'New'
    root['menu']['menuitems']['new']['onclick'] = 'new();'

NO W: No Wraps
---------------

Sooner or later, your code will be added to some print out,
perhaps even in a two-column format. When it does, you still
want it to look beautiful. So:

+ All code <= 52 characters. 
+ Not "self" but "i". 
+ Indents using 2 spaces. 
+ Try to keep functions, classes, under 60 lines 
  (and much less is much better).

STACK OVERFLOW
---------------

Any Python question you want answered has already
been asked and answered already on
stackoverflow.com. Read it!

CODING RULES
============

BBB: Burn baby burn
-------------------

_"Perfection is achieved, not when there is nothing
more to add, but when there is nothing left to take
away."_   
-- Antoine de Saint-Exupery

Once it starts works, burn some of it away.
Benchmark it against a simpler option.  Throw away
what does not improve performance. Note: often, you
can throw away a lot of superfluous stuff

CA: Constants Aren't:
----------------------

Put the code in a function where the 'constants' are
defaults to function arguments (so later, you can
call it another way).

HAIL REPO: 
----------

The code repo is your off-site backup, your undo
facility, your sharing tool. Use it. Always.  Many
times a day.

IDM: It doesn't matter.
-----------------------

Don't waste time arguing in theory about some tuning
issue. Just try it out. It probably won't matter in
practice.

JDI: Just do it.
----------------

Systems are not written; they grow. So find the
smallest next thing and just do that. Repeat.

KISS: 
-----

keep it simple stupid.

LIB: Leave it Broken:
---------------------

At the end of the day, leave behind a broken test
(this is where you can start back up, tomorrow).

NoGo: Globals are Evil:
-----------------------

N-1 globals is better than N globals.


NBO: No Buried Options
----------------------

Keep all 'The' settings. Print 'The' settings in
front of all output.

R: Refactor:
------------

To code it once, just do it.  If you code it twice,
wince.  But if you code it thrice, refactor.

RESUMABLE: 
----------

An anytime computation is stoppable and resumable.
 
For long computations, implement occasional "dump to
disk" and "restart from part-way". That way, if the
long computation crashes, you can restart from some
interim point (and not redo it all).

TAG: 'Things' Are Good
---------------------

Consider not defining a new class if a simple 'Thing'
will do (useful for named access to data only
classes).

TDD: Test Driven Development:
-----------------------------

Write a test.
Write the code.
Fix the fault.
Run all tests
Fix the faults.
Repeat.

YAGNI: 
------

You aren't gonna need it. Only code stuff that is
needed for your latest test. All other
generalizations are hallucinations.

SCIENCE RULES
==============

ESM: Effect size matters.
-------------------------

Statistical significance tests can condone very small
variations in large computations. So always use an effect
size test with the significance test to avoid small
number bullsh*t.

NET: Nine equals ten
--------------------

Minor numeric differences in performance are usually
unstable and disappear when you run the experiment
again. So don't fret the small deltas. 
Always seek the "big a*s" differences.

FSSS: Fast stats, slow stats.
-----------------------------

Two kinds of statistical tests: fast and slow.
Fast tests (parametric, e.g. t-tests) are used as heuristics
during a run to check for (say) early stopping. Slow tests
(non-parametric, e.g. bootstraps) are used after the run
to confirm some experimental hypothesis.

KTS: Keep the seed.
-------------------

To allow for reproduction, keep the seed and print
it as part of the options.

NAN: Normal ain't normal
------------------------

Much reasoning assumes a standard bell shaped
"normal" distribution.  But normal distributions are
not normally found in real world data. So favor
non-parametric distributions over trite normal
descriptions of data.

RNC: Random not crazy 
---------------------

Often the stochastic version is simpler, or scales
better, or both.

MOEA rules
==========

MaxSmarter
----------

Never show users something minimizing something. This
is America! Always maximize!

Klass to Meta to Example
---------------------------

At its core, my MOEAs manipulate a table of data:

+ Each column of that table is a feature and each row is one
  example.
+ The _i-th_ cell of each example
  is the _i-th_ _value_ of the _i-th_ feature

Internally, the features divide into:

+ Dependent features  (aka _depen_) we are trying to minimize or mazimize
  (internally, these are known as the  _less_ and the _more_, respectively).
+ Independent (aka _indep_) features we can control;
		
Our meta-knowledge of those examples is kept in a
high-level _meta_ variable.  
Each item in  _meta_ knows about

+ what values that *might* be added to an example;
+ what values that *were* found in the examples.

Using that knowledge,  _meta_  can:

- _Guess_ possible values for the variables in a example;
- Check if a new example is _ok_; i.e. is valid;
- _Score_ a example; i.e. using a list's independent variables,
  it can set the dependent variables.
- _Record_ a example's content; i.e. incrementally update counters
  in _meta_ showing what values were found in the examples.

Note that there is one _meta_ per feature.
So if we make 1000 examples,
where each list is a example of size 5, then there
exists *one* _meta_ that is a list of size 5 (and the _i-th_ meta
refers to the _i-th_ value in all the examples).

Recursively, there is also a _meta_ that holds a list of _meta_.
So to mutate all the values in
one example, the holding _meta_ asks each of the held _meta_s to
mutate one value.

The lifecycle of example is:

1. At design time, we build a _klass_ that defines how to generate a _meta_.
2. At runtime, we start by using that _klass_ to build a particular _meta_.
3. From that particular _meta_, we generate  independent values;
      + And, at this stage, all the dependent values are null.
4. Optionally, we can use those independent values to compute the dependent values.
      + Note it is invalid to guess dependent variables since these
	    should be computed from the independent variables.
5. Optionally, we can  add those values to a synopsis of values
   seen so far.


  
