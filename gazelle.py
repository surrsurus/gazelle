import sys
sys.dont_write_bytecode = True

# Local deps
from gazelle.cli import cli

if __name__ == '__main__':
  cli()