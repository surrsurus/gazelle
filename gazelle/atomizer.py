import re

from sym import eof_object, Sym, Quotes

# A regex that we use to tokenize a string
Tokenizer = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""
# A refex that we use to determine if a number 0-9 is present within a string
ContainsNum = re.compile('\d')

# The `Atomize` class takes an input object, typically a string or file
# and contains methods for turning it into an atomized gazelle expression
# that can be expanded and ultimately evaluated.
#
# An atomized gazelle expression consists of expressions that 
# consist of atoms and lists. These lists and atoms then become
# expanded into symbols and procedures through the parser.
#
# In reality, these lists and atoms are to become python objects.
# We essentially perform the action of gazelle syntax -> python object
# and reason about it using lisp terms. We do this to make evaluation
# and parsing easier later on.
class Atomize(object):
    "An input port. Retains a line of chars."
    def __init__(self, file):
        self.file = file; self.line = ''

    # Return the next token from the input based on the tokenizer
    # -> Token
    def next_token(self):
        ''' Return the next token, reading new text into line buffer if needed '''
        while True:
            if self.line == '': self.line = self.file.readline()
            if self.line == '': return eof_object
            token, self.line = re.match(Tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                return token

    ### Atoms
    # McCarthy defined two fundamental types: lists and atoms. Originally an atom was 
    # defined as simply something immutable and unique, though we cannot
    # guarantee that in gazelle due to the fact atoms are created based on tokens
    # which can ultimately be the same, and when atoms are stored they can be 
    # overwritten in the environment, not to mention the method `atom`
    # simply takes some non-list input and turns it into a python object
    #
    # One point of note is that in the original there were **no numbers**.  Instead, numbers
    # had to be represented as lists of atoms, proving to be quite slow. Though here,
    # an atom can be an integer, floating point value, or complex number.
    #
    # It's worth noting that atom's do not have an atom type, or associated object.
    # When we atomize a token, we simply convert it to a native python object
    # for faster parsing and evaluation

    # Based on the input object, read from it an expression that consists
    # of purely lists and atoms. This is an atomized expression
    # that needs to be expanded for proper evaluation
    # -> Atomized Gazelle Expression
    def read(self):
        ''' Read a gazelle expression from the input and return the list or atom '''

        # The `read_ahead` function simply takes a token read
        # from the input object and finds lists, quotes, eofs,
        # and atoms
        # Token -> Atom
        def read_ahead(token):
            # Lparen means that a list has begun
            if '(' == token: 
                L = []
                while True:
                    token = self.next_token()
                    if token == ')': return L
                    else: L.append(read_ahead(token))
            # If we see a rparen here, there must be an error since
            # after each lparen we check for the end of the list
            elif ')' == token: raise SyntaxError('unexpected )')
            # Expand quotes into their proper symbol
            elif token in Quotes: return [Quotes[token], self.read()]
            # We also shouldn't be having eofs
            elif token is eof_object: raise SyntaxError('unexpected EOF in list')
            # Otherwise we just return the proper atom
            else: return self.atom(token)

        # body of read:
        token1 = self.next_token()
        return eof_object if token1 is eof_object else read_ahead(token1)

    # Will take something that is not a list and determine what the equivalent
    # python object is. Since a token is a string, we need to turn them
    # into their python object equivalence though this involves a less than
    # ideal solution of using try/except
    # Token -> Atom
    def atom(self, token):
        ''' Atomize a token into a python object, either a bool, number, or symbol (String) '''

        # Typically, #t and #f are either symbols or empty lists,
        # though in gazelle we can read these tokens and return the proper
        # python objects for faster expansion/evaluation
        if token == '#t': return True
        elif token == '#f': return False

        # if it isn't a boolean value, it could be a string
        # wrapped in double quotes
        elif token[0] == '"': return token[1:-1].decode('string_escape')

        # TODO: The act of determining if a token is something like `123foobar`
        # is potentially costly towards computation time
        # it might be better to remove such symbols from gazelle
        # and return SyntaxErrors

        # Otherwise if the token contains an integer,
        # it *may be* an int, float, or complex number
        elif ContainsNum.search(token):
            # See if it's just something like `'123'`
            try: return int(token)
            except ValueError:
                # See if it's something like `'12.3'`
                try: return float(token)
                except ValueError:
                    # See if it's something like `'123j'`
                    try: return complex(token.replace('i', 'j', 1))
                    # Otherwise it must be something like `123foobar`
                    except ValueError:
                        return Sym(token)
        
        # If the token contains no numbers, isn't wrapped in double quotes,
        # and doesn't contain a number, it must be a string
        else: return Sym(token)