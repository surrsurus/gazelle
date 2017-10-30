### Parsing and Evaluation Module

from atomizer import Atomize
from env import Environment
from sym import eof_object, Symbol, Symbols, Quotes

import StringIO, re

### Helpers
# Convert a Python object back into a Scheme-readable string.
# Object -> Gazelle Expression
def schemestr(exp):
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')' 
    else:
        return str(exp)

### Parser

# Atomize or String -> Gazelle Expression
def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an `Atomize`
    if isinstance(inport, str): inport = Atomize(StringIO.StringIO(inport))
    return expand(inport.read(), toplevel=True)

# Expand turns an atomized gazelle expression into an expression
# that is readily readable by `eval()`. You can view this as
# sort of making an AST, though it's more like something
# that optimizes and expands syntactic sugar. This also checks
# syntax for any errors
# Atomized Gazelle Expression, (Boolean) -> Gazelle Expression
def expand(x, toplevel=False):
    # TODO: lists should be joined
    "Walk tree of x, making optimizations/fixes, and signaling SyntaxError."

    # Our input expression should not be an empty list
    if x == []:
        raise SyntaxError('Expression is empty')   # () => Error

    # If it isn't a list, we don't need to expand it
    elif not isinstance(x, list):                  # constant => unchanged
        return x

    # The leftmost term should always be a procedure.
    # We use this to compare it to our symbol table
    procedure = x[0]

    # Check to make sure our quote expression is the proper length
    if procedure is Symbols['quote']:                  # (quote exp)
        if len(x) != 2: 
            raise SyntaxError(schemestr(x) + ': quote has recieved '
                + str(len(x) - 1) + ' arguments, not 1')

        return x

    # Check our if statement and make the proper optimizations,
    # check it's arguments, and expand them
    elif procedure is Symbols['if']:                # (if t c e)
        if len(x) == 3: 
            # No else statement
            x = x + [None]                         # (if t c) => (if t c None)
            

        elif len(x) != 4:
            raise SyntaxError(schemestr(x) + ': if statement has recieved '
                + str(len(x) - 1) + ' arguments, not 2 or 3')

        return map(expand, x)

    # Make sure we are only applying set! to a symbol
    elif procedure is Symbols['set!']:                
        if len(x) != 3:
            raise SyntaxError(schemestr(x) + ': set! has recieved ' 
                + str(len(x) - 1) + ' arguments, not 2')               

        var = x[1]                       

        if not isinstance(var, Symbol):            # (set! non-var exp) => Error
            raise SyntaxError(schemestr(x) + 
                ': set! expects a symbol')

        return [Symbols['set!'], var, expand(x[2])]

    # Validate def and macro
    elif procedure is Symbols['def'] or procedure is Symbols['macro']: 

        if len(x) < 3:
            raise SyntaxError(schemestr(x) + 
                ': definition expects at least 2 arguments')

        # V is ???
        # Body is the expression we want to bind to v
        var, body = x[1], x[2:]

        if isinstance(var, list) and var:          # (define (f args) body)
            name, args = var[0], var[1:]           #  => (define name (lambda (args) body))
            return expand([procedure, name, [Symbols['lamb'], args] + body])

        else:

            if len(x) != 3:                        # (define non-var/list exp) => Error
                raise SyntaxError(schemestr(x) + 
                    ': definition expects 3 arguments')

            if not isinstance(var, Symbol):
                raise SyntaxError(schemestr(x) +
                    ': definition expects to bind to a symbol')

            # Expand the expression we want to bind to v
            exp = expand(x[2])

            # Macro expansion
            if procedure is Symbols['macro']:
                if not toplevel:
                    raise SyntaxError(schemestr(x) + 
                        ': macros can only be defined at the top level') 

                proc = eval(exp)

                if not callable(proc):
                    raise SyntaxError(schemestr(x) + 
                        ': macro must be a procedure, not an atom or list')   
                
                # Add our macro to the macro table
                macro_table[var] = proc             # (define-macro v proc)

                return None                         #  => None; add v:proc to macro_table

            return [Symbols['def'], var, exp]

    # Expand the content of begin if it exists
    elif procedure is Symbols['begin']:
        if len(x)==1:                                
            return None                    
        else: 
            return [expand(xi, toplevel) for xi in x]

    # Expand a lambda expression
    elif procedure is Symbols['lamb']:               # (lambda (x) e1 e2) 
        if len(x) < 3:                             #  => (lambda (x) (begin e1 e2))
            raise SyntaxError(schemestr(x) + 
                ': lamb expects at least 2 arguments')

        var, body = x[1], x[2:]

        # If the arguments are not a list, and everything isn't a symbol, there is a problem
        if not (isinstance(var, list) and all(isinstance(v, Symbol) for v in var) or isinstance(var, Symbol)):
            raise SyntaxError(schemestr(x) +
                ': illegal lamb argument list')

        exp = body[0] if len(body) == 1 else [Symbols['begin']] + body

        return [Symbols['lamb'], var, expand(exp)]   

    # Expand quasiquote
    elif procedure is Symbols['quasiquote']:         # `x => expand_quasiquote(x)
        if len(x) != 2:
            raise SyntaxError(schemestr(x) + 
                ': quasiquote (`) expects at least 2 arguments')
        return expand_quasiquote(x[1])

    # Expand macros that already exist
    elif isinstance(procedure, Symbol) and procedure in macro_table:
        return expand(macro_table[procedure](*x[1:]), toplevel) # (m arg...) 

    # Otherwise we need to keep expanding the expression
    else:                                
        return map(expand, x)                       # (f arg...) => expand each

# Gazelle Expression -> Gazelle Expression
def expand_quasiquote(x):
    """Expand `x => 'x; `,x => x; `(,@x y) => (append x y) """

    if not (x != [] and isinstance(x, list)):
        return [Symbols['quote'], x]

    if x[0] is Symbols['unquotesplicing']:
        raise SyntaxError(schemestr(x) + 
            ': can\'t splice here')

    if x[0] is Symbols['unquote']:
        if len(x) != 2:
            raise SyntaxError(schemestr(x) + 
                ': unquote (,) expects 1 argument')

        return x[1]

    elif (x[0] != [] and isinstance(x[0], list)) and x[0][0] is Symbols['unquotesplicing']:
        if len(x[0]) != 2:
            raise SyntaxError(schemestr(x[0]) + 
                ': unquotesplicing (,@) expects 1 argument')

        return [Symbols['append'], x[0][1], expand_quasiquote(x[1:])]

    else:
        return [Symbols['cons'], expand_quasiquote(x[0]), expand_quasiquote(x[1:])]

### Macros

# Arguments -> Gazelle Expression
def let(*args):
    args = list(args)
    x = [Symbols['let']] + args

    if len(args) <= 1:
        raise SyntaxError(schemestr(x) + ': let expects greater than 1 argument')

    bindings, body = args[0], args[1:]

    if not all(isinstance(b, list) and len(b)==2 and isinstance(b[0], Symbol) for b in bindings):
        raise SyntaxError(schemestr(x) + ': let was given an illegal binding list')

    var, vals = zip(*bindings)

    return [[Symbols['lamb'], list(var)]+map(expand, body)] + map(expand, vals)

macro_table = {Symbols['let']:let} ## More macros can go here

### Procedures
# A procedure as implemented in gazelle is a lambda expression as
# defined by Church wherein the lambda expression takes arguments
# binds them to an expression, then returns the result
#
# McCarthy's paper makes a distinction between forms and functions
# because we need a clear notation of *how* we apply functions
# to parameters. McCarthy subexplains it thusly:
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
# Therefore, a `Procedure` object represents a *function*, that is, a lambda 
# expression. In gazelle, these expressions are written in the form
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
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    # A `Procedure` is a function, therefore we should be able to
    # call it as a function with respect to the proper environment
    # Note that the environment is created each time the procedure is
    # called
    def __call__(self, *args): 
        return eval(self.body, Environment(self.parms, args, self.env))

def callcc(proc):
    ''' Call proc with current continuation; escape only '''
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")
    def throw(retval): ball.retval = retval; raise ball
    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball: return ball.retval
    else: raise w

### StdEnv
# An environment with basic procedures
# -> Environment
def standard_env():
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
        '+':          lambda *x: reduce(op.add, (x), 0),
        '-':          lambda *x: x[0] - sum(x[1:]),
        '*':          lambda *x: reduce(op.mul, (x), 1),
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
        'eq?':        op.is_, 
        'equal?':     op.eq, 
        'eval':       lambda x: eval(x), 
        'include':    lambda x: eval(parse(Atomize(open(x)))),
        'length':     len, 
        'land':       lambda *x: reduce(op.and_, (x)),
        'list':       lambda *x: list(x),
        'list?':      lambda x: isinstance(x,list), 
        'map':        map,
        'max':        max,
        'filter':     filter,
        'min':        min,
        'not':        op.not_,
        'null?':      lambda x: x == [], 
        'number?':    lambda x: isinstance(x, int) or isinstance(x, float) or isinstance(x, complex),   
        'or':         op.or_,   
        'proc?':      callable,
        'range':      lambda *x: list(range(x[0], x[1])) if len(x) > 1 else list(range(x[0])),
        'readchar':   lambda *x: input('>'),
        'readfloat':  lambda *x: float(input('>')),
        'readint':    lambda *x: int(input('>')),
        'round':      round,
        'str?':       lambda x: isinstance(x, str),
        'sum':        lambda x: sum(x),
        })
    return env

global_env = standard_env()

### Eval
# Evaluate an expression in an environment.
# Gazelle expression -> Evaluated Gazelle expression
def eval(expr, env=global_env):
    "Evaluate an expression in an environment."
    while True:
        if isinstance(expr, Symbol):       # variable reference
            return env.find(expr)[expr]
        elif not isinstance(expr, list):   # constant literal
            return expr

        procedure = expr[0]

        if procedure is Symbols['quote']:     # (quote subexp)
            (_, subexp) = expr
            return subexp
        elif procedure is Symbols['if']:        # (if test conseq alt)
            (_, test, conseq, alt) = expr
            expr = (conseq if eval(test, env) else alt)
        elif procedure is Symbols['set!']:       # (set! var subexp)
            (_, var, subexp) = expr
            env.find(var)[var] = eval(subexp, env)
            return None
        elif procedure is Symbols['def']:    # (define var subexp)
            (_, var, subexp) = expr
            env[var] = eval(subexp, env)
            return None
        elif procedure is Symbols['lamb']:    # (lambda (var*) subexp)
            (_, vars, subexp) = expr
            return Procedure(vars, subexp, env)
        elif procedure is Symbols['begin']:     # (begin subexp+)
            for subexp in expr[1:-1]:
                eval(subexp, env)
            expr = expr[-1]
        elif procedure== Symbols['check-expect']: # test exact
            (_, var, subexp) = expr
            return (eval(var, env) == eval(subexp, env))
        elif procedure == Symbols['check-within']: # test range
            (_, var, lower_bound, upper_bound) = expr
            return ((eval(var, env) <= eval(upper_bound, env) and
                    (eval(var, env) >= eval(lower_bound, env))))
        elif procedure == Symbols['member?']: # member?
            (_, var, lst) = expr
            return (eval(var, env) in eval(lst, env))
        elif procedure == Symbols['display']: # display
            (_, body) = expr
            print body
            return None
        else:                    # (proc subexp*)
            subexps = [eval(subexp, env) for subexp in expr]
            proc = subexps.pop(0)
            if isinstance(proc, Procedure):
                expr = proc.body
                env = Environment(proc.parms, subexps, proc.env)
            else:
                return proc(*subexps)