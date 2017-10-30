from parseval import eval, parse
import colors

# Test builtin procedures
builtins_test = [
    ("(if 1 2)", 2),
    ("(if (= 3 4) 2)", None),
    ("(quote x)", 'x'), 
    ("(quote (1 2 three))", [1, 2, 'three']), 
    ("'x", 'x'),
    ("'(one 2 3)", ['one', 2, 3]),
    ("(def L (list 1 2 3))", None),
    ("`(testing ,@L testing)", ['testing',1,2,3,'testing']),
    ("`(testing ,L testing)", ['testing',[1,2,3],'testing']),
    ("`,@L", SyntaxError),
    ("""'(1 ;test comments '
     ;skip this line
     2 ; more ; comments ; ) )
     3) ; final comment""", [1,2,3])
]

# Test the call/cc functionality
callcc_tests = [
    ("(call/cc (lamb (throw) (+ 5 (* 10 (throw 1))))) ;; throw", 1),
    ("(call/cc (lamb (throw) (+ 5 (* 10 1)))) ;; do not throw", 15),
    ("""(call/cc (lamb (throw) 
         (+ 5 (* 10 (call/cc (lamb (escape) (* 100 (escape 3)))))))) ; 1 level""", 35),
    ("""(call/cc (lamb (throw) 
         (+ 5 (* 10 (call/cc (lamb (escape) (* 100 1))))))) ; 0 levels""", 1005)
]

# Test macros
macro_tests = [
    ("(let ((a 1) (b 2)) (+ a b))", 3),
    ("(let ((a 1) (b 2 3)) (+ a b))", SyntaxError),
    ("(macro unless (lamb args `(if (not ,(car args)) (begin ,@(cdr args))))) ; test `", None),
    ("(unless (= 2 (+ 1 1)) (display 2) 3 4)", None),
    (r'(unless (= 4 (+ 1 1)) (display 2) (display "\n") 3 4)', 4),
]

# Test operators
operator_tests = [
    ("(+ 1 2)", 3),
    ("(- 2 1)", 1),
    ("(% 6 2)", 0),
    ("(* 2 2)", 4),
    ("(/ 10 2)", 5),
    ("(= 5 5)", True),
    ("(= \"hello\" \"hello\")", True),
    ("(= \"hello\" \"world\")", False),
    ("(= '(1 2 3) '(1 2 3 4))", False),
    ("(> 5 2)", True),
    ("(< 5 2)", False),
    ("(<= 5 2)", False),
    ("(<= 5 5)", True),
    ("(>= 5 2)", True),
    ("(>= 2 2)", True),
    ("(>> 16 2)", 4),
    ("(<< 4 2)", 16)
]

# Test procedures by using `def` and `lamb`
proc_tests = [
    ("(def (twice x) (* 2 x))", None), ("(twice 2)", 4),
    ("(twice 2 2)", TypeError),
    ("(def ((account bal) amt) (set! bal (+ bal amt)) bal)", None),
    ("(def a1 (account 100))", None),
    ("(a1 0)", 100), ("(a1 10)", 110), ("(a1 10)", 120),
    ("""(def (newton guess function derivative epsilon)
    (def guess2 (- guess (/ (function guess) (derivative guess))))
    (if (< (abs (- guess guess2)) epsilon) guess2
        (newton guess2 function derivative epsilon)))""", None),
    ("""(def (square-root a)
    (newton 1 (lamb (x) (- (* x x) a)) (lamb (x) (* 2 x)) 1e-8))""", None),
    ("(> (square-root 200.) 14.14213)", True),
    ("(< (square-root 200.) 14.14215)", True),
    ("(= (square-root 200.) (sqrt 200.))", True)
]

# Test the standard environemnt
stdenv_tests = [
    ("(abs -1)", 1),
    ("(abs 1)", 1),
    ("(append \"h\" \"w\")", 'hw'),
    ("(def f +)", None),
    ("(apply f '(1 2))", 3),
    ("(begin)", None),
    ("(bool? #t)", True),
    ("(car '(1 2 3))", 1),
    ("(cdr '(1 2 3))", [2, 3]),
    ("(cons '(1) '(2))", [[1], 2]),
    ("(eq? 1 1)", True),
    ("(equal? 5 5)", True),
    ("(length '(1 2 3))", 3),
    ("(land #t #f)", False),
    ("(list 1 2 3 4 5)", [1, 2, 3, 4, 5]),
    ("(list? '(1 2 3))", True),
    ("(max '(1 2 3 4 5))", 5),
    ("(min '(1 2 3 4 5))", 1),
    ("(not #t)", False),
    ("(null? '())", True),
    ("(number? 1)", True),
    ("(number? \"1\")", False),
    ("(proc? bool?)", True),
    ("(proc? 12345)", False),
    ("(round 1.2)", 1.0),
    ("(round 1.7)", 2.0),
    ("(str? \"hello world\")", True)
]

# Test methods in the standard library
stdlib_tests = [
    ("(and 1 2 3)", 3), 
    ("(and (> 2 1) 2 3)", 3), 
    ("(and)", True),
    ("(and (> 2 1) (> 2 3))", False),
    ('(nil? nil)', True),
    ("(nil? '())", True),
    ("(= nil '())", True),
    ("(reverse '(1 2 3))", [3, 2, 1]),
    ("(map (lamb (x) (* 2 x)) '(1 2 3))", [2, 4, 6]),
]

# Test syntax by throwing errors
syntax_tests = [
    ("()", SyntaxError), 
    ("(set! x)", SyntaxError), 
    ("(def 3 4)", SyntaxError),
    ("(quote 1 2)", SyntaxError), 
    ("(if 1 2 3 4)", SyntaxError), 
    ("(lamb 3 3)", SyntaxError), 
    ("(lamb (x))", SyntaxError),
    ("""(if (= 1 2) (macro a 'a) 
     (macro a 'b))""", SyntaxError)
]

# Test tail recursion
tail_recursion_tests = [
    ("""(def (sum-squares-range start end)
         (def (sumsq-acc start end acc)
            (if (> start end) acc (sumsq-acc (+ start 1) end (+ (* start start) acc))))
         (sumsq-acc start end 0))""", None),
    ("(sum-squares-range 1 3000)", 9004500500)
]

# A list of all testing suites and their names
suites = [
    (builtins_test, 'Built-in'),
    (callcc_tests, 'Call/CC'),
    (macro_tests, 'Macro'),
    (operator_tests, 'Operator'),
    (proc_tests, 'Procedure'),
    (stdenv_tests, 'Standard Environment'),
    (stdlib_tests, 'Standard Library'),
    (syntax_tests, 'Syntax'),
    (tail_recursion_tests, 'Tail Recursion')
]

# Run a test and capture output, comapre it to an expected
# value
def capture(expr, expected):
    ''' Run a test and compare it to an expected value '''

    # Attempt to run test normally
    try:
        result = eval(parse(expr))
        print '[:] ', expr, '=>', (result)
        return (result == expected)
    # Tests can raise exceptions, so capture them slightly differently
    except Exception as e:
        print '[#] ', expr, '=raises=>', type(e).__name__, e
    # `issubclass` might not work on some tests, so we just capture any
    # TypeErrors and return false because that that point the test definitely
    # failed
    try:
        # Since we look for exceptions let's properly capture them and not
        # return False prematurely
        return issubclass(expected, Exception) and isinstance(e, expected)
    except TypeError:
        return False

def run():
    ''' Test each test case in all suites to 
    see if gazelle is being properly interpreted '''

    fails = 0
    tests = 0

    # Iterate over each test in all suites
    for suite in suites:

        # Print section header
        colors.printf(suite[1] + ' Tests', colors.HEADER)

        # Iterate over tests in a suite
        for (expr, expected) in suite[0]:

            tests += 1 # Count our tests

            # Capture test output
            if not capture(expr, expected):
                
                # Failed a test if we reached here
                fails += 1
                colors.printf(('[!] FAIL: Expected: %s' % str(expected)), colors.FAIL)

    # Print test results
    colors.printf(('%s %d out of %d tests fail.' % ('*'*45, fails, tests)), colors.OKBLUE)

    # Print conclusion
    if fails == 0:
        colors.printf('[%] Testing concluded successfully', colors.OKGREEN)
    else:
        colors.printf('[!] Testing concluded with errors', colors.FAIL)

