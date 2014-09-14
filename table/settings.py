import sys
sys.dont_write_bytecode = True
from o import *

The = o(cache = o(keep=256,
                  update=1.1),
        cluster=o(using= lambda tbl: tbl.cols.indep),
        misc= o(missing='?',
                nervous= True,
                _logo= """
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
 """))

