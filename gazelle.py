import sys
sys.dont_write_bytecode = True

# Local deps
from gazelle import repl

### CLI
# The commandline interface helps determine what action
# the user is trying to perform. Based on the arguments, we
# can either load files, start the REPL, or run the tests.

if __name__ == '__main__':
  sys.argv.pop(0)

  # Evaluate Files
  #  repl will rep all files after the program name such as:
  #  `py gazelle.py file1.gel file2.gel ... fileN.gel`
  if sys.argv:
    for file in sys.argv:
      repl.run_file(file)

  # Start Repl
  #  repl starts under the condition :
  #  `./gazelle.py` or `py gazelle.py` or `python gazelle.py`
  else:
    repl.run()
  
  
