
def prettyd(i,name=None):
  "show public keys, in sorted order"
  def public(key): 
      return not key[0] == "_"
  me    = i.__dict__
  name = name or i.__class__.__name__
  order = sorted(k for k in me.keys() 
                 if public(k))
  pairs = [':%s %s' % (k,me[k]) for k in order]
  return name+'{'+ ', '.join(pairs) +'}'
