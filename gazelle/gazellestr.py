import collections

# Object -> Gazelle Expression
def gazellestr(exp):
  ''' Convert a Python object back into a Gazelle-readable string. '''

  # Bools
  if isinstance(exp, bool):
    if exp: return '#t'
    else: return '#f'

  # Procedures
  elif isinstance(exp, collections.Callable):
    try:
      return '(lambda (' + ' '.join([str(x) for x in exp.params]) + \
        ') (' + ' '.join([gazellestr(x) for x in exp.body]) + '))'
    except AttributeError:
      return exp
  
  # Lists
  elif isinstance(exp, list):
    return '(' + ' '.join(map(gazellestr, exp)) + ')' 
  
  # Everything else
  return str(exp)