# Local deps
from . import colors
from .atomizer import Atomizer
from .gazellestr import gazellestr
from .parseval import gazeval, parse, gazellestr, global_env

def run_file(path):
  try:
    gazeval(parse(path, file=True), global_env)
  except Exception as e:
    colors.printf('[!] %s: %s' % (type(e).__name__, e), colors.FAIL)

    # TypeErrors arise if a non-callable object is called 
    # or non-iterable object is iterated over
    if type(e) == TypeError:
      if 'object is not callable' in str(e):
        colors.printf('[#] This could be a problem because the lefthand term of an expression isn\'t a procedure\n[:] Make sure to use `quote` (\') on lists of atoms.', colors.FAIL)
      if 'object is not iterable' in str(e):
        colors.printf('[#] You cannot iterate over an atom or procedure.\n[:] In addition, some procedures only take lists as inputs.', colors.FAIL)
          
    # LookupErrors arise if a symbol can't be found in an Environment
    elif type(e) == LookupError:
      colors.printf('[#] ' + str(e) + ' cannot be found in the current scope.\n[:] This might be a typo, or this symbol is not defined', colors.FAIL)

    # ValueErrors occur if the user tries to give a procedure more arguments than it needs
    elif type(e) == ValueError:
      colors.printf('[#] You are trying to give a procedure more arguments than it can handle.', colors.FAIL)
    else:
      raise e

# (String) -> None
def run(prompt='gel> ', subprompt='> '):
  ''' A prompt-read-gazeval-print loop.
  The repl
   1. Reads from stdin through `raw_input`
   2. Parses the input into an expanded gazelle expression
      (barring no syntax errors)
   3. Evaluates the gazelle expression
   4. Returns the output to stdout through `print`
   5. Goes back to step 1 '''
  
  try:
    
    while True:
      
      inpt = input(prompt)

      if inpt == "quit": break

      # If the user has started a list, and
      # the list is incomplete, allow the user to complete
      # it on the next line
      while list(inpt)[0] == '(' and inpt.count('(') != inpt.count(')'):
        inpt += ' ' # Lack of an extra space may cause some programs to fail
        inpt += input((len(prompt)-len(subprompt)) * ' ' + subprompt)

      val = gazeval(parse(inpt), global_env)

      if val is not None:
        print(gazellestr(val))

  except Exception as e:
    if isinstance(e, KeyboardInterrupt) or isinstance(e, EOFError):
      pass
    else:
      colors.printf('[!] %s: %s' % (type(e).__name__, e), colors.FAIL)

      # TypeErrors arise if a non-callable object is called 
      # or non-iterable object is iterated over
      if type(e) == TypeError:
        if 'object is not callable' in str(e):
          colors.printf('[#] This could be a problem because the lefthand term of an expression isn\'t a procedure\n[:] Make sure to use `quote` (\') on lists of atoms.', colors.FAIL)
        if 'object is not iterable' in str(e):
          colors.printf('[#] You cannot iterate over an atom or procedure.\n[:] In addition, some procedures only take lists as inputs.', colors.FAIL)
          
      # LookupErrors arise if a symbol can't be found in an Environment
      elif type(e) == LookupError:
        colors.printf('[#] ' + str(e) + ' cannot be found in the current scope.\n[:] This might be a typo, or this symbol is not defined', colors.FAIL)

      # ValueErrors occur if the user tries to give a procedure more arguments than it needs
      elif type(e) == ValueError:
        colors.printf('[#] You are trying to give a procedure more arguments than it can handle.', colors.FAIL)
      else:
        raise e
