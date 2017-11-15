from .env import Environment
from functools import reduce

def callcc(proc):
  ''' Call proc with current continuation; escape only '''
  ball = RuntimeWarning('Sorry, can\'t continue this continuation any longer.')
  def throw(retval): ball.retval = retval; raise ball
  try:
    return proc(throw)
  except RuntimeWarning as w:
    if w is ball: return ball.retval
  else: raise w

### StdEnv
# None -> Environment
def make_env():
  ''' An environment with basic procedures. '''

  import math
  import cmath
  import itertools
  import operator as op

  env = Environment()
  
  env.update(vars(math))
  env.update(vars(cmath))
  env.update(vars(itertools))

  env.update({
    '>':          op.gt,     '<':       op.lt,    
    '>=':         op.ge,     '<=':      op.le,
    '=':          op.eq,
    '>>':         op.rshift, '<<':      op.lshift,
    '+':          lambda *x: reduce(op.add, x, 0),
    '-':          lambda *x: x[0] - sum(x[1:]),
    '*':          lambda *x: reduce(op.mul, x, 1),
    '/':          lambda *x: reduce(op.truediv, (x[1:]), x[0]),
    '//':         lambda *x: reduce(op.floordiv, (x[1:]), x[0]),
    '%':          op.mod,
    'abs':        abs,
    'append':     op.add,
    'apply':      lambda proc,l: proc(*l),
    'begin':      lambda *x: x[-1],
    'bool?':      lambda x: isinstance(x, bool),
    'call/cc':    callcc,
    'car':        lambda x: x[0],
    'cdr':        lambda x: x[1:],
    'cons':       lambda x,y: [x] + y,
    'filter':     lambda f,l: list(filter(f, l)),
    'length':     len, 
    'list':       lambda *x: list(x),
    'list?':      lambda x: isinstance(x,list), 
    # Map can be defined in the stdlib, though it will max out python's recursion depth
    'map':        lambda f,l: list(map(f, l)),
    'max':        max,
    'min':        min,
    'not':        op.not_,
    'number?':    lambda x: not isinstance(x, bool) and isinstance(x, int) or isinstance(x, float) or isinstance(x, complex),   
    'or':         op.or_,
    'proc?':      callable,
    'range':      lambda *x: list(range(x[0], x[1])) if len(x) > 1 else list(range(x[0])),
    'round':      round,
    'str?':       lambda x: isinstance(x, str),
    'sum':        lambda x: sum(x),
    })
  return env

# Create a global env for `gazeval()` to access
global_env = make_env()