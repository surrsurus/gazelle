from sym import Symbol

### Environment
# An environment, at it's core is a collection of variables
# and procedures, therefore an `Environment` is just that
# 
# We can create a mutable environment by representing it as a dictionary
# that is, a simple key/value relation where the key is a string
# representation of the value which may be an atom, a list, or a procedure
class Environment(dict):
    def __init__(self, parms=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isinstance(parms, Symbol): 
            self.update({parms:list(args)})
        else: 
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, ' 
                                % ((parms), (args)))
            self.update(zip(parms,args))

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self: return self
        elif self.outer is None: raise LookupError(var)
        else: return self.outer.find(var)