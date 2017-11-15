from . import colors

# Error -> String
def gazelleerr(e):
  ''' Analyze the python error and return the
  proper gazelle error and give some potentially helpful hints. '''

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

  return '#error'