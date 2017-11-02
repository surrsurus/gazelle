# Local deps
import colors
from gazellestr import convert as gazellestr
from parseval import eval, parse, gazellestr, global_env

# Parse, Eval and capture any errors
def capture_parseval(expression):
  try:

    val = eval(parse(expression), global_env)

    return val

  except Exception as e:
    colors.printf('[!] %s: %s' % (type(e).__name__, e), colors.FAIL)

    # TypeErrors arise if a non-callable object is called 
    # or non-iterable object is iterated over
    if type(e) == TypeError:
      if 'object is not callable' in str(e):
        print "[#] This could be a problem because the lefthand term of an expression isn't a procedure\n[:] Make sure to use `quote` (') on lists of atoms."
      if 'object is not iterable' in str(e):
        print '[#] You cannot iterate over an atom or procedure.\n[:] In addition, some procedures only take lists as inputs.'
    
    # LookupErrors arise if a symbol can't be found in an Environment
    elif type(e) == LookupError:
      print '[#] ' + str(e) + ' cannot be found in the current scope.\n[:] This might be a typo, or this symbol is not defined'

    # ValueErrors occur if the user tries to give a procedure more arguments than it needs
    elif type(e) == ValueError:
      print '[#] You are trying to give a procedure more arguments than it can handle.'

    return '#error'

# Parse, Eval, and don't capture errors so you can see where something
# went wrong exactly
debug_capture_parseval = lambda expr: eval(parse(expr))

# A prompt-read-eval-print loop.
# The repl
#  1. Reads from stdin through `raw_input`
#  2. Parses the input into an expanded gazelle expression
#     (barring no syntax errors)
#  3. Evaluates the gazelle expression
#  4. Returns the output to stdout through `print`
#  5. Goes back to step 1.
# (String) -> None
def run(prompt='gel> ', subprompt='> '):
  try:

    while True:
      
      inpt = raw_input(prompt)

      if inpt == "quit": break

      # If the user has started a list, and
      # the list is incomplete, allow the user to complete
      # it on the next line
      while list(inpt)[0] == '(' and inpt.count('(') != inpt.count(')'):
        inpt += ' ' # Lack of an extra space may cause some programs to fail
        inpt += raw_input((len(prompt)-len(subprompt)) * ' ' + subprompt)

      val = capture_parseval(inpt)

      if val:
        print gazellestr(val)
        
  except KeyboardInterrupt:
    pass
