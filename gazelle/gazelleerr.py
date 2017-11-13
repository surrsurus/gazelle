import colors

def gazelleerr(e):

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