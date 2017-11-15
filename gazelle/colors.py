import os

### Colors
# Colors for making console output prettier.
# Should be accessed as an enum, `colors.HEADER`
# for example.

HEADER = ''
OKBLUE = ''
OKGREEN = ''
WARNING = ''
FAIL = ''
ENDC = ''

# Enable colors if not on windows
if os.name != 'nt':
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

def printf(string, color):
  ''' Print a string and format it with a color. '''
  print(color + string + ENDC)