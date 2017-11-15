import sys

# Local deps
from .atomizer import Atomizer
from . import repl

### CLI
# The commandline interface helps determine what action
# the user is trying to perform. Based on the arguments, we
# can either load files, start the REPL, or run the tests.

# None -> None
def cli():
  ''' Examine the commandline arguments and determine what to do. '''

  # Start Repl
  #  repl starts under the condition :
  #  `./gazelle.py` or `py gazelle.py` or `python gazelle.py `
  if len(sys.argv) == 1:
    repl.run()

  # Evaluate Files
  #  repl will rep all files after the program name such as:
  #  `py gazelle.py file1.gel file2.gel ... fileN.gel`
  else:
      for file in sys.argv[1:]:
        if file == 'repl':
          repl.run()
          exit()
        repl.capture_parseval(Atomizer(open(file)))