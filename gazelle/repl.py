# Local deps
import colors
from gazellestr import convert as gazellestr
from gazelleerr import gazelleerr
from parseval import eval, parse, gazellestr, global_env

# Parse, Eval and capture any errors
def capture_parseval(expression):
  try:

    val = eval(parse(expression), global_env)

    return val

  except Exception as e:
    gazelleerr(e)

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

      if val is not None:
        print gazellestr(val)
        
  except KeyboardInterrupt:
    pass
