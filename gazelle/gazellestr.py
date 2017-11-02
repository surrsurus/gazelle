### GazelleStr
# Convert a Python object back into a Gazelle-readable string.
# Object -> Gazelle Expression
def convert(exp):

  # Bools
  if exp is True: return '#t'
  elif exp is False: return '#f'

  # Procedures
  elif callable(exp):
    try:
      return '(lambda (' + ' '.join([str(x) for x in exp.params]) + \
        ') (' + ' '.join([convert(x) for x in exp.body]) + '))'
    except AttributeError:
      return exp
  
  # Lists
  elif isinstance(exp, list):
    return '(' + ' '.join(map(convert, exp)) + ')' 
  
  # Everything else
  else:
    return str(exp)