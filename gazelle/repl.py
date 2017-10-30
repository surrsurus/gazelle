import colors
from parseval import eval, parse, schemestr

# Parse, Eval and capture any errors
def capture_parseval(expression):
    try:

        val = eval(parse(expression))

        if val is not None: 
            return val

    except Exception as e:
        colors.printf('%s: %s' % (type(e).__name__, e), colors.FAIL)

        # TypeErrors arise if a non-callable object is called
        if type(e) == TypeError:
            print "This could be a problem because the lefthand term of an expression isn't a procedure. \n \
                Make sure to use `quote` (') on lists of atoms."

        return e

# A prompt-read-eval-print loop.
# The repl
#  1. Reads from stdin through `raw_input`
#  2. Parses the input into an expanded gazelle expression
#     (barring no syntax errors)
#  3. Evaluates the gazelle expression
#  4. Returns the output to stdout through `print`
#  5. Goes back to step 1.
# (String) -> None
def run(prompt='gel> '):
    try:
        while True:
            inpt = raw_input(prompt)
            if inpt == "quit": break

            val = capture_parseval(inpt)

            if val:
                print schemestr(val)
                
    except KeyboardInterrupt:
        pass
