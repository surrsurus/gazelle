# Object -> Gazelle Expression
def gazellestr(exp):
  ''' Convert a Python object back into a Gazelle-readable string. '''

  # Bools
  if exp is True: return '#t'
  elif exp is False: return '#f'

  # Procedures
  elif callable(exp):
    try:
      return '(lambda (' + ' '.join([str(x) for x in exp.params]) + \
        ') (' + ' '.join([gazellestr(x) for x in exp.body]) + '))'
    except AttributeError:
      return exp
  
  # Lists
  elif isinstance(exp, list):
    return '(' + ' '.join(map(gazellestr, exp)) + ')' 
  
  # Everything else
  else:
    return str(exp)