/^"""</,/^>"""/ { next }

/^"""/ { In = 1 - In
         if (In) 
	     print "````python"
         else
	     print "````"
         next
       }
In  { print "    " $0}
!In { print $0}
END { if (In) print "````" }
