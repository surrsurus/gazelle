from gazellestr import gazellestr
from sym import Symbol

### Environment
# An environment, at it's core is a collection of variables
# and procedures, therefore an `Environment` is just that
# 
# We can create a mutable environment by representing it as a dictionary
# that is, a simple key/value relation where the key is a string
# representation of the value which may be an atom, a list, or a procedure
class Environment(dict):

  def __init__(self, params=(), args=(), outer=None):
    ''' Bind param list to corresponding args, or 
    single param to list of args. '''

    self.outer = outer
    if isinstance(params, Symbol): 
      self.update({params:list(args)})
    else: 
      if len(args) != len(params):
        raise SyntaxError('expected %s, given %s, ' 
          % (gazellestr(params), gazellestr(args)))
      self.update(zip(params,args))

  def find(self, var):
    ''' Find the innermost Environment where var appears. '''

    if var in self: return self
    elif self.outer is None: raise LookupError(var)
    else: return self.outer.find(var)