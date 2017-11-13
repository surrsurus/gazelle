### Symbols
# The symbol was the basic atom in Lisp 1 and served as 
# the basic unit of data. In his early papers,
#  McCarthy freely mixes the terms atom and symbol.
#
# In gazelle, a symbol is an atom that isn't a bool,
# integer, float, or complex number, therefore it must be a string
class Symbol(str): pass

# String, (Dict) -> Atom
def Sym(s, symbol_table={}):
  ''' Find or create unique Symbol entry for str s in symbol table. '''
  
  if s not in symbol_table: symbol_table[s] = Symbol(s)
  return symbol_table[s]

# Dictionary of common symbols we check for when expanding
# and evaluating
Symbols = {
  'append':          Sym('append'),       
  'begin':           Sym('begin'),        
  'check-expect':    Sym('check-expect'),
  'check-within':    Sym('check-within'),
  'cons':            Sym('cons'),
  'def':             Sym('def'),
  'display':         Sym('display'),
  'if':              Sym('if'),
  'include':         Sym('include'),
  'lambda':          Sym('lambda'),
  '\\':              Sym('\\'),
  'let':             Sym('let'),
  'macro':           Sym('macro'),
  'member?':         Sym('member?'),
  'quasiquote':      Sym('quasiquote'),
  'quote':           Sym('quote'),
  'return':          Sym('return'),
  'set!':            Sym('set!'),
  'unquote':         Sym('unquote'),
  'unquotesplicing': Sym('unquotesplicing'),
  'while':           Sym('while'),
}

# Quotes such as these must be expanded into
# `Symbol`s before evaluation time
Quotes = { 
  '\'': Symbols['quote'],
  '`':  Symbols['quasiquote'],
  ',':  Symbols['unquote'],
  ',@': Symbols['unquotesplicing']
}

# The eof represents the end of a file or input
eof = Symbol('#<eof>') # Note: uninterned; can't be read
