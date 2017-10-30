import sys

# Local deps
from atomizer import Atomize
import repl
import integration_tests

def start():
  ''' Examine the commandline and determine what to do '''

  # Load stdlib
  repl.capture_parseval(Atomize(open('./lib/stdlib.gel')))

  # Start Repl
  #  repl starts under the condition :
  #  `./gazelle.py` or `py gazelle.py` or `python gazelle.py `
  if len(sys.argv) == 1:
    repl.run()

  # Run tests
  elif len(sys.argv) > 1 and (sys.argv[1] == 'test'):
    integration_tests.run()

  # Evaluate Files
  #  repl will rep all files after the program name such as:
  #  `py gazelle.py file1.gel file2.gel ... fileN.gel`
  else:
    [repl.capture_parseval(Atomize(open(file))) for file in sys.argv[1:]]