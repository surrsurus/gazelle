# Local deps
from .atomizer import Atomizer
from .env import Environment
from .gazellestr import gazellestr
from .stdenv import global_env
from .sym import eof, Symbol, Symbols, Quotes
import collections

### Parser
# Atomizer -> Gazelle Expression
def parse(atomizer):
  ''' Parse a program: read and expand/error-check it '''

  # Backwards compatibility: given a str, convert it to an atomizer
  import io
  if isinstance(atomizer, str): 
    atomizer = Atomizer(io.StringIO(atomizer))

  return expand(atomizer.read(), toplevel=True)

# Atomized Gazelle Expression, (Boolean) -> Gazelle Expression
def expand(expr, toplevel=False):
  ''' Expand turns an atomized gazelle expression into an expression
  that is readily readable by `eval()`. You can view this as
  sort of making an AST, though it's more like something
  that optimizes and expands syntactic sugar. This also checks
  syntax for any errors.
  
  We can't just name this parse and expect it to work with the atomizer
  object. It recursively looks at the expression and changes it,
  so it would not work at all with the way the `Atomizer` class works. '''

  # Our input expression should not be an empty list
  # () => Error
  if expr == []:
    raise SyntaxError('Expression is empty')

  # If it isn't a list, we don't need to expand it
  # constant => unchanged
  elif not isinstance(expr, list):
    return expr

  # The leftmost term should always be a procedure.
  # We use this to compare it to our symbol table
  # procedure = (procedure arg1 arg2 arg3 ...)
  procedure = expr[0]

  # Expand quotes
  # (quote expe)
  if procedure is Symbols['quote']:
    # Check to make sure our quote expression is the proper length
    if len(expr) != 2: 
      raise SyntaxError(gazellestr(expr) + ': quote has recieved '
        + str(len(expr) - 1) + ' arguments, not 1')

    return expr

  # Check our if statement and make the proper optimizations,
  # check it's arguments, and expand them
  # (if t c e)
  elif procedure is Symbols['if']:
    # Since there's no else, make sure we add a None so the
    # next error check doesn't trigger
    if len(expr) == 3: 
      # No else statement
      # (if t c) => (if t c None)
      expr = expr + [None] 

    # Not enough arguments or too many
    elif len(expr) != 4:
      raise SyntaxError(gazellestr(expr) + ': if statement has recieved '
        + str(len(expr) - 1) + ' arguments, not 2 or 3')

    return list(list(map(expand, expr)))

  # Make sure we are only applying set! to a symbol
  # (set! var expr)
  elif procedure is Symbols['set!']:
    if len(expr) != 3:
      raise SyntaxError(gazellestr(expr) + ': set! has recieved ' 
        + str(len(expr) - 1) + ' arguments, not 2')

    (_, var, expr) = expr

    # (set! non-var expr) => Error
    if not isinstance(var, Symbol):
      raise SyntaxError(gazellestr(expr) + 
        ': set! expects a symbol')

    return [Symbols['set!'], var, expand(expr)]

  # Validate def and macro
  # (def var expr), (macro var expr)
  elif procedure is Symbols['def'] or procedure is Symbols['macro']: 

    if len(expr) < 3:
      raise SyntaxError(gazellestr(expr) + 
        ': definition expects at least 2 arguments')

    # Var is the label we want to represent the expression
    # Body is the expression we want to bind to var
    var, body = expr[1], expr[2:]

    # Var needs to exist
    # TODO: Test this, I feel like we don't need it since the first
    # error check should capture this possibility
    # if not var:
    #     raise SyntaxError(gazellestr(expr) +
    #         ': definition expects to bind to a variable, none given')

    # Expressions in the form (def (f) (expr)) will break on evaluation
    # as it would need to be called literally as ((f) ...)
    # (def (f) expr)
    if isinstance(var, list) and len(var) == 1:
      var = var[0]

    # Turn (def (f args) body) into the proper lambda expression
    # (def (f args) body) ...
    if isinstance(var, list):
      
      # ... => (def name (lambda (args) body))
      name, args = var[0], var[1:]
      return expand([procedure, name, [Symbols['lambda'], args] + body])

    else:
      
      # (def non-var/list exp) => Error
      if len(expr) != 3:
        raise SyntaxError(gazellestr(expr) + 
          ': definition expects 3 arguments')

      # (def 12345 exp) => Error
      if not isinstance(var, Symbol):
        raise SyntaxError(gazellestr(expr) +
          ': definition expects to bind to a symbol')

      # Expand the expression we want to bind to v
      exp = expand(expr[2])

      # Macro expansion
      if procedure is Symbols['macro']:
        if not toplevel:
          raise SyntaxError(gazellestr(expr) + 
            ': macros can only be defined at the top level') 

        proc = eval(exp)

        if not isinstance(proc, collections.Callable):
          raise SyntaxError(gazellestr(expr) + 
            ': macro must be a procedure, not an atom or list')   
        
        # Add our macro to the macro table
        # (macro v proc)
        macro_table[var] = proc

        # => None; add v:proc to macro_table
        return None

      return [Symbols['def'], var, exp]

  # Expand the content of begin if it exists
  elif procedure is Symbols['begin']:
    # Prevents infinite loop
    if len(expr)==1:
      return None
    else: 
      return [expand(xi, toplevel) for xi in expr]

  # Expand a lambda expression
  # (lambda (expr) e1 e2) 
  elif procedure in [Symbols['lambda'], Symbols['\\']]:
    
    # => (lambda (expr) (begin e1 e2))
    if len(expr) < 3:
      raise SyntaxError(gazellestr(expr) + 
        ': lambda expects at least 2 arguments')

    var, body = expr[1], expr[2:]

    # If the arguments are not a list of symbols, there is a problem
    if not (isinstance(var, list) and all(isinstance(v, Symbol) for v in var) or isinstance(var, Symbol)):
      raise SyntaxError(gazellestr(expr) +
        ': illegal lambda argument list')

    exp = body[0] if len(body) == 1 else [Symbols['begin']] + body

    return [Symbols['lambda'], var, expand(exp)]   

  # Expand quasiquote
  # `expr => expand_quasiquote(expr)
  elif procedure is Symbols['quasiquote']:
    if len(expr) != 2:
      raise SyntaxError(gazellestr(expr) + 
        ': quasiquote (`) expects at least 2 arguments')
    return expand_quasiquote(expr[1])

  # Expand macros that already exist
  # (m arg...) 
  elif isinstance(procedure, Symbol) and procedure in macro_table:
    return expand(macro_table[procedure](*expr[1:]), toplevel)

  # Otherwise we need to keep expanding the expression
  else:
    # (f arg...) => expand each
    return list(list(map(expand, expr)))

# Gazelle Expression -> Gazelle Expression
def expand_quasiquote(expr):
  ''' Expand `expr => 'expr; `,expr => expr; `(,@expr y) => (append expr y) '''

  if not (expr != [] and isinstance(expr, list)):
    return [Symbols['quote'], expr]

  if expr[0] is Symbols['unquotesplicing']:
    raise SyntaxError(gazellestr(expr) + 
      ': can\'t splice here')

  if expr[0] is Symbols['unquote']:
    if len(expr) != 2:
      raise SyntaxError(gazellestr(expr) + 
        ': unquote (,) expects 1 argument')

    return expr[1]

  elif (expr[0] != [] and isinstance(expr[0], list)) and expr[0][0] is Symbols['unquotesplicing']:
    if len(expr[0]) != 2:
      raise SyntaxError(gazellestr(expr[0]) + 
        ': unquotesplicing (,@) expects 1 argument')

    return [Symbols['append'], expr[0][1], expand_quasiquote(expr[1:])]

  else:
    return [Symbols['cons'], expand_quasiquote(expr[0]), expand_quasiquote(expr[1:])]

### Macros

# Arguments -> Gazelle Expression
def let(*args):
  ''' Let macro '''

  args = list(args)
  expr = [Symbols['let']] + args

  if len(args) <= 1:
    raise SyntaxError(gazellestr(expr) + ': let expects greater than 1 argument')

  bindings, body = args[0], args[1:]

  if not all(isinstance(b, list) and len(b)==2 and isinstance(b[0], Symbol) for b in bindings):
    raise SyntaxError(gazellestr(expr) + ': let was given an illegal binding list')

  var, vals = list(zip(*bindings))

  return [[Symbols['lambda'], list(var)]+list(map(expand, body))] + list(map(expand, vals))

macro_table = {Symbols['let']:let} ## More macros can go here

### Procedures
# A procedure as implemented in gazelle is a lambda expression as
# defined by Church wherein the lambda expression takes arguments
# binds them to an expression, then returns the result
#
# McCarthy's paper makes a distinction between forms and functions
# because we need a clear notation of *how* we apply functions
# to parameters. McCarthy explains it thusly:
#
# "Let `f` be an expression that stands for a function of two integer 
# variables. It should make sense to write `f(3, 4)` and the value of this 
# expression should be determined. The expression 
#   `y^2 + x`
# does not meet this requirement; `y^2 + x(3, 4)` is not a conventional 
# notation, and if we attempted to define it we would be uncertain whether 
# its value would turn out to be 13 or 19. Church calls an expression like 
# `y^2 + x`, a form. A form can be converted into a function if we can 
# determine the correspondence between the variables occurring in the 
# form and the ordered list of arguments of the desired function. 
# This is accomplished by Church's lambda-notation."
#
# Therefore, a `Procedure` object represents a *function*, that is, 
# a lambda expression. In gazelle, these expressions are written in 
# the form
#   `(lamb (args) (expr))`
# In addition a `Procedure` knows what environment it was created in
# and has the ability to make a new internal environment that is created from
# it's arguments, it's parameters, and the environment it was created in.
# This is what creates a function scope in gazelle
#
# However, the procedure by itself is useful, but if we want to make it
# resusable or recursive, we bind the procedure to a specific label
# that we can envoke with the `def` keyword such that
#  `(def func (lamb (args) (expr)))`
# will assign `func` to the lambda expression
# This notation also allows for recursion
#  `(def func (lamb (args) (func)))`
# as the environment `func` is defined in will be passed to the `Procedure`
# object, allowing it to access itself
class Procedure(object):
  def __init__(self, params, body, env):
    self.params, self.body, self.env = params, body, env

  def __call__(self, *args): 
    ''' A `Procedure` is a function, therefore we should be able to
    call it as a function with respect to the proper environment
    Note that the environment is created each time the procedure is
    called. '''

    return eval(self.body, Environment(self.params, args, self.env))

### Eval
# Gazelle expression -> Evaluated Gazelle expression
def eval(expr, env=global_env):
  ''' Evaluate an expression in an environment. '''
  # TODO: Missing unquote

  while True:
    # variable reference
    if isinstance(expr, Symbol):
      return env.find(expr)[expr]

    # constant literal
    elif not isinstance(expr, list):
      return expr

    # procedure = (func arg1 arg2 arg3 ...)
    procedure = expr[0]

    # (quote subexpr)
    if procedure is Symbols['quote']:     
      (_, subexpr) = expr
      return subexpr

    # (if test conseq else)
    elif procedure is Symbols['if']:        
      (_, test, conseq, alt) = expr
      expr = (conseq if eval(test, env) else alt)

    # (set! var expr)
    elif procedure is Symbols['set!']:      
      (_, var, subexpr) = expr
      env.find(var)[var] = eval(subexpr, env)
      return None

    # (def var expr)
    elif procedure is Symbols['def']:
      (_, var, subexpr) = expr
      env[var] = eval(subexpr, env)

      return None
    # (lambda (var*) expr)
    elif procedure is Symbols['lambda']:
      (_, vars, subexpr) = expr
      return Procedure(vars, subexpr, env)

    # (begin expr+)
    elif procedure is Symbols['begin']:
      for subexpr in expr[1:-1]:
        eval(expand(subexpr), env)
      expr = expr[-1]

    # test exact
    elif procedure == Symbols['check-expect']:
      (_, var, subexpr) = expr
      return (eval(var, env) == eval(subexpr, env))

    # test range
    elif procedure == Symbols['check-within']: 
      (_, var, lower_bound, upper_bound) = expr
      return ((eval(var, env) <= eval(upper_bound, env) and
          (eval(var, env) >= eval(lower_bound, env))))
    
    # (member? var list)
    elif procedure == Symbols['member?']: 
      (_, var, lst) = expr
      return (eval(var, env) in eval(lst, env))
    
    # (display symbol/var)
    elif procedure == Symbols['display']:
      (_, body) = expr
      print(gazellestr(eval(body, env)))
      return None

    # (return exp)
    elif procedure == Symbols['return']:
      (_, body) = expr
      return eval(body, env)

    # (include "filepath")
    elif procedure == Symbols['include']:
      (_, file) = expr
      return eval(parse(Atomizer(open(file))), env)

    # (stdlib)
    elif procedure == Symbols['stdlib']:
      eval(parse(Atomizer(open('./lib/stdlib.gel'))), env)
      return None

    # (while cond body)
    elif procedure == Symbols['while']:

      (_, cond, body) = expr
      while eval(cond, env):
        eval(body, env)

      return None
    
    # (proc expr*)
    else:                    
      subexprs = [eval(subexpr, env) for subexpr in expr]
      proc = subexprs.pop(0)
      if isinstance(proc, Procedure):
        expr = proc.body
        env = Environment(proc.params, subexprs, proc.env)
      else:
        return proc(*subexprs)