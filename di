#!/usr/bin/env python3.5
# Python 3.6 users should update the above line accordingly

import math, operator as op
import os
import sys
import random
from functools import reduce
from itertools import compress

################################################################################

# Commands for the stdlib that need to be defined here
################################################################################

### Input and Feedback

# Variable print or Verbose print (vprinting must be enabled)
vprinting = False
def vprint(arg):
    if vprinting:
        print(arg)

################################################################################

# File parsing
################################################################################

# Evaluate a list of deercode expressions
def eval_lib(lib):
    for l in lib:
        # Ignore length 0 lines if any are there from the file loading
        if len(l) > 0:
            eval(parse(l))

# Parse a file and run it
def eval_file(path):
    with open(path) as f:
        eval_lib(f.read().splitlines())

################################################################################

# Parsing
################################################################################

# Read an expression from a line
def parse(program):
    return read_from_tokens(tokenize(program))

# Convert a string into a list of tokens
def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').split()

# Read an expression from a sequence of tokens
def read_from_tokens(tokens):

    # EOFError if file is too short
    if len(tokens) == 0:
        raise EOFError('unexpected EOF while reading')

    # Pop a token off
    token = tokens.pop(0)

    # Evaluate statements in parens
    if '(' == token:
        L = []
        while tokens[0] != ')':
            # Recursively read from tokens
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected ")" in + ' + tokens)

    else:
        # Everything is ultimately atomized
        return atom(token)

# Atomize tokens into numbers or symbols
# Might not be elegant, but it works
def atom(token):
    try: return int(token)       # Number
    except ValueError:
        try: return float(token) # Number
        except ValueError:
            return str(token)    # Symbol

################################################################################

# Environments
################################################################################

def standard_env():
    ''' An environment with some standard procedures '''
    env = Env()
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update() # sum function
    env.update({
        '>':  op.gt,     '<':  op.lt,    '>=':op.ge, '<=':op.le, '=':op.eq,
        '>>': op.rshift, '<<': op.lshift,
        '+':          lambda *x: reduce(op.add, (x), 0),
        '-':          lambda *x: x[0] - sum(x[1:]),
        '*':          lambda *x: reduce(op.mul, (x), 1),
        '/':          lambda *x: reduce(op.truediv, (x[1:]), x[0]),
        '//':         lambda *x: reduce(op.floordiv, (x[1:]), x[0]),
        '%':          op.mod,
        'abs':        abs,
        'and':        op.and_,
        'append':     op.add,
        'begin':      lambda *x: x[-1],
        'car':        lambda x: x[0],
        'cdr':        lambda x: x[1:],
        'compress':   lambda x, y: list(compress(x, y)),
        'cons':       lambda x,y: [x] + y,
        'even?':      lambda x: x % 2 == 0,
        'false':      lambda *x: False,
        'grange':     lambda *x: list(range(x[0], x[1])) if len(x) > 1 else list(range(x[0])),
        'int':        int,
        'include':    eval_file,
        'len':        len,
        'list':       lambda *x: list(x),
        'list?':      lambda x: isinstance(x,list),
        'map':        lambda *x: list(map(x[0], x[1])),
        'max':        max,
        'min':        min,
        'not':        op.not_,
        'nil':        lambda *x: None,
        'null?':      lambda x: x == [],
        'number?':    lambda x: isinstance(x, (int, float)),
        'or':         op.or_,
        'odd?':       lambda x: x % 2 == 0,
        'prin':       lambda *x: print(' '.join(x)),
        'proc?':      callable,
        'quit':       lambda *x: exit(0),
        'randint':    random.randint,
        'readchar':   lambda *x: input('>'),
        'readfloat':  lambda *x: float(input('>')),
        'readint':    lambda *x: int(input('>')),
        'round':      round,
        'symbol?':    lambda x: isinstance(x, str),
        'sum':        lambda x: sum(x),
        'true':       lambda *x: True,
        'xor':        op.xor
    })
    return env

class Env(dict):
    ''' An environment: a dict of {'var':val} pairs, with an outer Env. '''
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    # Find the innermost Env where var appears
    def find(self, var):
        try:
            return self if (var in self) else self.outer.find(var)
        except AttributeError:
            # Fix for windows IDLEs
            if os.name == 'nt':
                print('[!] ' + 'Deercode Error: Atom "' + var + '" is undefined. You are either missing arguments or have referenced a function that does not exist.')
            else:
                print('\033[91m' + '[!] ' + 'Deercode Error: Atom "' + var + '" is undefined. You are either missing arguments or have referenced a function that does not exist.' + '\033[0m')

            return self if ('nil' in self) else self.outer.find('nil')

# Set a standard env
stdlib = standard_env()

################################################################################

# Interaction: A REPL
################################################################################

# Read, Eval, Print loop
def repl(prompt='\033[92m' + 'λ ' + '\033[0m', vp=False):
    global vprinting

    vprinting = vp

    # Fix for Windows IDLEs
    if prompt == '\033[92m' + 'λ ' + '\033[0m':
        if os.name == 'nt':
            prompt = 'λ '

    while True:

        try:
            # Prompt
            i = input(prompt)
            # If prompt exists...
            if len(i) > 1:
                # Evaluate it
                val = eval(parse(i))
                # Print value
                if val is not None and vp:
                    print(lispstr(val))

        # Catch errors

        # EOFErrors crash the program
        except EOFError:
            print()
            exit()

        # Elegantly exit without python freaking out
        except KeyboardInterrupt:
            print()
            exit()

        # Function or variable doesn't exist

        # Other exceptions raise an error, but the program
        # continues normally (ish)
        except Exception as e:
            # Fix for windows IDLEs
            if os.name == 'nt':
                print('[!] ' + str(e))
            else:
                print('\033[91m' + '[!] ' + str(e) + '\033[0m')

# Turn python list into readable atoms
def lispstr(exp):
    if  isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

# Load a library into the current environment by parsing
# it's contents, as they are all functions
def loadlib(lib, msg=None):
    if msg != None:
        print(msg)

    for l in lib:
        if len(l) > 0:
            eval(parse(l))

################################################################################

# Lambdas
################################################################################

class Lambda(object):
    ''' A user-defined lambda '''
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))

################################################################################

# Evaluation of atoms
################################################################################

def eval(atom, env=stdlib):
    ''' Evaluate an expression (atoms) for a given environment '''

    # If atom is a string, see if we can find the variable or function
    # Or if atom is a deercode string, return the string object
    if isinstance(atom, str):
        # Strings surrounded by quotes are returned
        if list(atom)[0] == '"' and list(atom)[len(atom)-1] == '"':
            return atom[1:-1]
        # Otherwise do a lookup
        else:
            return env.find(atom)[atom]

    # If atom is a boolean , return it
    elif isinstance(atom, bool):
        return atom

    # If atom isn't a list, it must be a constant of sorts
    elif not isinstance(atom, list):
        return atom

    # If atom is deer, show the raw data elsewhere in the line
    elif atom[0] == 'deer':
        (_, exp) = atom
        return exp

    # If atom is a comment, comment it out (useful for programs)
    elif atom[0] == '#':
        (_, *comment) = atom

    # If atom is prinv, this must be a reference to the special
    # Print variable method
    # This must be defined here as it references the environment in use
    elif atom[0] == 'prinv':
        (_, exp) = atom
        try:
            print(env.find(exp)[exp])
        except TypeError:
            print(eval(exp, env))

    # If atom is if, this must start an if statement
    elif atom[0] == 'if':
        (_, test, conseq, alt) = atom
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)

    # If atom is set, this must set a varaible in the environment
    # This must be defined here as it manipulates the environment in use
    elif atom[0] == 'set':
        (_, var, exp) = atom
        env[var] = eval(exp, env)
        vprint(var + ' : ' + str(env[var]))

    # If atom is override, this must override a global function
    # This must be defined here as it manipulates the environment in use
    elif atom[0] == 'override':
        # override a global function
        (_, var, exp) = atom
        env.find(var)[var] = eval(exp, env)
        vprint(env.find(var)[var])

    elif atom[0] == 'eval':
        # Evaluate a list of commands in left-to-right order
        (_, *exp) = atom
        for e in list(exp):
            var = eval(e, env)
            if var is not None:
                vprint(eval(e, env))

    # If atom is repl, this must start a repl in the current environment
    # (Useful for programs)
    elif atom[0] == 'repl':
        repl(prompt='extlib> ', vp=True)

    # If atom is global, this must set a global varaible
    # This must be defined here as it manipulates the environment in use
    elif atom[0] == 'global':
        (_, var, exp) = atom
        stdlib.find(var)[var] = eval(exp, env)
        vprint(var + ' : ' + str(stdlib[var]))

    # If atom is lamb, this must define a lambda function
    # This must be defined here as it passes the environment in use as an arg
    elif atom[0] == 'lamb':
        (_, parms, body) = atom
        return Lambda(parms, body, env)

    # If atom is env, show all methods and variables in the global scope
    # This must be defined here as it references the environment in use
    elif atom[0] == 'env':
        for method in sorted(env.keys()):
            print(method)
        return '-- global env --'

    # ASCII art easter egg!
    elif atom[0] == 'asciiart':
        deercodeLoader.prettify()

    # Otherwise we assume atom is a function in the environment
    else:
        proc = eval(atom[0], env)
        args = [eval(exp, env) for exp in atom[1:]]
        return proc(*args)

################################################################################

# Deercode overhead
################################################################################

class Initializer():
    def __init__(self):
        self.ascii_art = [
        "        ,/  \.                                        ",
        "       |(    )|                                       ",
        "   `.\_`\\')(`/'_/,'                                  ",
        "   \`-._:,\  /.;_,-'/                                 ",
        "       )/`.,'\(                                       ",
        "       |.    ,|                                       ",
        "       :6)  (6;                                       ",
        "        \`\ _(\\                                      ",
        "         \._'; `.___...---..________...------._       ",
        "          \   |   ,'   .  .     .       .     .`:.    ",
        "           \`.' .  .         .   .   .     .   . \\\\ ",
        "            `.       .   .  \  .   .   ..::: .    ::  ",
        "              \ .    .  .   ..::::::::''  ':    . ||  ",
        "               \   `. :. .:'            \  '. .   ;;  ",
        "                `._  \ ::: ;           _,\  :.  |/(   ",
        "                   `.`::: /--....---''' \ `. :. :`\`  ",
        "                    | |:':               \  `. :.\\   ",
        "                    | |' ;                \  (\  .\\  ",
        "                    | |.:                  \  \`.  :  ",
        "                    |.| |                   ) /  :.|  ",
        "                    | |.|                  /./   | |  ",
        "                    |.| |                 / /    | |  ",
        "                    | | |                /./     |.|  ",
        "                    ;_;_;              ,'_/      ;_|  ",
        "                   '-/_(              '--'      /,'   ",
        "          ____                  ____          _       ",
        "         |  _ \  ___  ___ _ __ / ___|___   __| | ___  ",
        "         | | | |/ _ \/ _ \ '__| |   / _ \ / _` |/ _ \ ",
        "         | |_| |  __/  __/ |  | |__| (_) | (_| |  __/ ",
        "         |____/ \___|\___|_|   \____\___/ \__,_|\___| "
        ]
        self.version = '1.1.0'

    # Get season
    def seasoner(self):
        from datetime import date, datetime
        Y = 2000 # Dummy leap year to allow input X-02-29 (leap day)
        seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
                   ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
                   ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
                   ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
                   ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]
        now = date.today()

        if isinstance(now, datetime):
            now = now.date()
        now = now.replace(year=Y)

        return next(season for season, (start, end) in seasons \
            if start <= now <= end)

    # Print ascii art
    def prettify(self):
        for line in self.ascii_art:
            # Fix for windows IDLEs
            if os.name == 'nt':
                print(line)
            else:
                print('\033[92m' + line + '\033[0m')

        # print('DEERCODE V' + self.version)

    # Load deercode!
    def start(self):
        import time

        modules = [
            'Initializing deer...',
            'Re-routing deer grazing patterns...',
            'Installing deerVM...',
            'Creating a bitcoin miner on deerVM...',
            'Deleting deerVM because programs that run in VMs are dumb...',
            'Cross-Compiling deercode to ruby...',
            'Cross-Compiling ruby to rust...',
            'Fatal error: Rust is worse than c#, retrying last module with param.0',
            'Cross-Compiling ruby to lua...',
            'Installing LUAos...',
            'Fatal error: LUAos written in TI-BASIC',
            'Installing DEERos...',
            'Loading all 47091542.5 deercode imports...',
            'Fatal error: deer',
            'Retrying last with object flags --deer'
        ]

        # Absolutely vital to the interpreter
        # DO NOT CHANGE IN ANY WAY
        print('Loading Interpreter Loader...')
        module_occurance = math.ceil(100/len(modules))
        module_counter = 0
        for i in range(100):
            time.sleep(random.randint(1,4)*.1)
            if i % module_occurance == 0:
                # Write as many space as the largest length of the modules list
                sys.stdout.write(''.join([' ' for _ in range(max(map(len, modules)))]))
                sys.stdout.write('\r    %s' % modules[module_counter])
                module_counter += 1
            sys.stdout.write('\r%d%%' % i)
            sys.stdout.flush()

        # Push putput down a line
        sys.stdout.write('\n')

        # Load additional modules
        print('Checking if DeerCode is active in this season..')

        # Check season
        season = self.seasoner()
        if season == 'autumn':
            print('Season: fall')
            print('DeerCode will run at 2x speed to prepare for winter')
        elif season == 'winter':
            print('Season: winter')
            raise Exception('Deercode is hibernating. Code cannot be run')
        elif season == 'summer':
            print('Season: summer')
        elif season == 'spring':
            print('Season: spring')

################################################################################

# Main method
################################################################################

deercodeLoader = Initializer()

if __name__ == '__main__':

    # Evaluate a file if given
    if len(sys.argv) > 1:
        # Started deers require no loading time
        if (sys.argv[1] == 'startle'):
            repl(vp=True)

        # Legacy mode
        if (sys.argv[1] == 'legacy'):
            # deercodeLoader.prettify()
            deercodeLoader.start()
            repl(vp=True)

        # Load some files
        else:
            print('-- running ' + sys.argv[1] + ' --')
            # Open file
            with open(sys.argv[1]) as f:
                lines = f.read().splitlines()

                # Parse lines
                for line in lines:
                    # Ignore empty lines
                    if len(line) > 0:
                        val = eval(parse(line))
                        # Return output
                        if val is not None:
                            print(lispstr(val))


    # If no path given, start a basic repl
    else:
        # deercodeLoader.prettify()
        print('DEERCODE V' + deercodeLoader.version)
        repl(vp=True)

################################################################################
