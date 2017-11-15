# Local deps
from . import colors
from .gazellestr import gazellestr
from .gazelleerr import gazelleerr
from .parseval import eval, parse, gazellestr, global_env

def capture_parseval(expression):
  ''' Parse, Eval and capture any errors. '''

  try:
    val = eval(parse(expression), global_env)
    return val
  except Exception as e:
    gazelleerr(e)

# Parse, Eval, and don't capture errors so you can see where something
# went wrong exactly
debug_capture_parseval = lambda expr: eval(parse(expr))

# (String) -> None
def run(prompt='gel> ', subprompt='> '):
  ''' A prompt-read-eval-print loop.
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

      val = capture_parseval(inpt)

      if val is not None:
        print(gazellestr(val))
  except Exception as e:
    if isinstance(e, KeyboardInterrupt) or isinstance(e, EOFError):
      pass
    else:
      raise e
