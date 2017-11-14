from gazelle import colors
from gazelle.parseval import eval, parse
from gazelle.atomizer import Atomizer
import gazelle.repl as repl

# Test builtin procedures
builtins_test = [
  # check-expect
  ('(check-expect (= 1 1) #t)', True),
  ('(check-expect (= "string" "string") #t)', True),
  ('(check-expect (= "string" "gazelle") #f)', True),
  ('(check-expect (+ 1 2 3) 6)', True),
  ('(check-expect (filter (\ (n) (= (% n 3) 0)) (range 20)) \'(0 3 6 9 12 15 18)))', True),
  ('(check-expect (append "gaz" "elle") "gazelle")', True),
  # check-within
  ('(check-within 1 0 2)', True),
  ('(check-within 1 3 10000)', False),
  ('(check-within "b" "a" "c")', True),
  # def
  ('(def gazelle "gazelle")', None),
  ('(def (gazelle x) (return x))', None),
  ('(def gazelle (\ (x) (return x)))', None),
  # if
  ('(if 1 2)', 2),
  ('(if (= 3 4) 2)', None),
  # include
  ('(include "./euler/one.gel")', 233168),
  # lambda
  ('(def a (lambda (x) (return x)))', None),
  ('(def a (\ (x) (return x)))', None),
  # member?
  ('(member? 1 \'(1 2 3))', True),
  ('(member? "a" "gazelle")', True),
  # quasiquotes and unquotesplicing
  ('(def L (list 1 2 3))', None),
  ('`(testing ,@L testing)', ['testing',1,2,3,'testing']),
  ('`(testing ,L testing)', ['testing',[1,2,3],'testing']),
  ('`,@L', SyntaxError),
  # quote
  ('(quote x)', 'x'), 
  ('(quote (1 2 three))', [1, 2, 'three']), 
  # return
  ('(return 5)', 5),
  # set!
  ('''(begin
    (def a 10)
    (set! a 15)
    (return a))''', 15),

  # Other
  
  # constant literals
  ('\'x', 'x'),
  ('\'(one 2 3)', ['one', 2, 3]),
  # comments
  (''''(1 ;test comments '
   ;skip this line
   2 ; more ; comments ; ) )
   3) ; final comment''', [1,2,3])
]

# Test the call/cc functionality
callcc_tests = [
  ('(call/cc (\ (throw) (+ 5 (* 10 (throw 1))))) ;; throw', 1),
  ('(call/cc (\ (throw) (+ 5 (* 10 1)))) ;; do not throw', 15),
  ('''(call/cc (\ (throw) 
     (+ 5 (* 10 (call/cc (\ (escape) 
      (* 100 (escape 3)))))))) ; 1 level''', 35),
  ('''(call/cc (\ (throw) 
     (+ 5 (* 10 (call/cc (\ (escape) 
      (* 100 1))))))) ; 0 levels''', 1005)
]

# Test macros
macro_tests = [
  ('(let ((a 1) (b 2)) (+ a b))', 3),
  ('(let ((a 1) (b 2 3)) (+ a b))', SyntaxError),
  ('''(macro unless (\ args 
    `(if (not ,(car args)) (begin ,@(cdr args))))) ; test `''', None),
  ('(unless (= 2 (+ 1 1)) (display 2) 3 4)', None),
  (r'(unless (= 4 (+ 1 1)) (display 2) (display "\n") 3 4)', 4),
]

# Test operators
operator_tests = [
  # +
  ('(+ 1 2)', 3),
  ('(+ 1)', 1),
  ('(+ 1 2 3 4 5)', 15),
  ('(+ "string" "string")', TypeError),
  ('(+ \'(1 2 3 4) 5)', TypeError),
  # "Weird" behavior
  ('(+ #t)', 1),
  ('(+ #f)', 0),
  ('(+ #f #f)', 0),
  ('(+ #f #t)', 1),
  # -
  ('(- 2 1)', 1),
  ('(- 1)', 1),
  ('(- 1 2 3 4 5)', -13),
  ('(- "string" "string")', TypeError),
  ('(- \'(1 2 3 4) 5)', TypeError),
  # "Weird" behavior
  ('(- #t)', 1),
  ('(- #f)', 0),
  ('(- #f #f)', 0),
  ('(- #f #t)', -1),
  # %
  ('(% 6 2)', 0),
  # *
  ('(* 2 2)', 4),
  # /
  ('(/ 10 2)', 5),
  ('(/ 20 2)', 10),
  ('(/ 1 0)', ZeroDivisionError),
  ('(/ "string" "gazelle")', TypeError),
  ('(/ \'(1 2 3) \'(1 2 3))', TypeError),
  # "Weird" behavior
  ('(/ #t)', True),
  ('(/ #f)', False),
  ('(/ #f #f)', ZeroDivisionError),
  ('(/ #f #t)', 0.0),
  # //
  ('(// 5 2)', 2),
  ('(// 20 3)', 6),
  ('(// 1 0)', ZeroDivisionError),
  ('(// "string" "gazelle")', TypeError),
  ('(// \'(1 2 3) \'(1 2 3))', TypeError),
  # "Weird" behavior
  ('(// #t)', True),
  ('(// #f)', False),
  ('(// #f #f)', ZeroDivisionError),
  ('(// #f #t)', 0),
  # =
  ('(= 5 5)', True),
  ('(= "string" "string")', True),
  ('(= "string" "gazelle")', False),
  ('(= \'(1 2 3) \'(1 2 3 4))', False),
  ('(= \'(1 2 3) \'(1 2 3))', True),
  ('(= #t #f)', False),
  ('(= #t #t)', True),
  ('(= #f #f)', True),
  ('(= #t)', TypeError),
  ('(= 1)', TypeError),
  ('(= 1 2 3)', TypeError),
  ('(= "string")', TypeError),
  # >
  ('(> 5 2)', True),
  ('(> 2 2)', False),
  # "Weird" behavior
  ('(> #f #t)', False),
  ('(> #t #f)', True),
  # <
  ('(< 5 2)', False),
  ('(< 2 2)', False),
  ('(< 2 5)', True),
   # "Weird" behavior
  ('(< #f #t)', True),
  ('(< #t #f)', False),
  # <=
  ('(<= 5 2)', False),
  ('(<= 5 5)', True),
  # >=
  ('(>= 5 2)', True),
  ('(>= 2 2)', True),
  # >>
  ('(>> 16 2)', 4),
  # <<
  ('(<< 4 2)', 16)
]

# Test procedures by using `def` and `\`
proc_tests = [
  ('(def (twice x) (* 2 x))', None), ('(twice 2)', 4),
  ('(twice 2 2)', SyntaxError),
  ('(def ((account bal) amt) (set! bal (+ bal amt)) bal)', None),
  ('(def a1 (account 100))', None),
  ('(a1 0)', 100), ('(a1 10)', 110), ('(a1 10)', 120),
  ('''(def (newton guess function derivative epsilon)
  (def guess2 (- guess (/ (function guess) (derivative guess))))
  (if (< (abs (- guess guess2)) epsilon) guess2
    (newton guess2 function derivative epsilon)))''', None),
  ('''(def (square-root a)
  (newton 1 (\ (x) (- (* x x) a)) (\ (x) (* 2 x)) 1e-8))''', None),
  ('(> (square-root 200.) 14.14213)', True),
  ('(< (square-root 200.) 14.14215)', True),
  ('(= (square-root 200.) (sqrt 200.))', True)
]

# Test the standard environemnt
stdenv_tests = [
  # abs
  ('(abs -1)', 1),
  ('(abs 1)', 1),
  ('(abs "1")', TypeError),
  # append
  ('(append "str" "ing")', 'string'),
  ('(append "gaz" "elle")', 'gazelle'),
  ('(append "h")', TypeError),
  # Strange behavior since `append` is the python + operator
  # (but expects 2 arguments instead of +)
  ('(append 1 2)', 3),
  # begin
  ('''(begin 
    (def f +)
    (return (apply f \'(1 2)))))
  ''', 3),
  ('(begin (return 5))', 5),
  # bool?
  ('(bool? #t)', True),
  ('(bool? #f)', True),
  ('(bool? 5)', False),
  ('(bool? "5")', False),
  ('(bool? \'(5))', False),
  # call/cc handled in a seperate testing suite
  # car
  ('(car \'(1 2 3))', 1),
  ('(car \'(4 5))', 4),
  ('(car "string")', 's'),
  ('(car "gazelle")', 'g'),
  ('(car 12345)', TypeError),
  # cdr
  ('(cdr \'(1 2 3))', [2, 3]),
  ('(cdr \'(4 5))', [5]),
  ('(cdr "string")', 'tring'),
  ('(cdr "gazelle")', 'azelle'),
  ('(cdr 12345)', TypeError),
  # cons
  ('(cons \'(1) \'(2))', [[1], 2]),
  ('(cons \'(1) 2)', TypeError),
  # filter
  ('''(begin
    (def fib \'(0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578))
    (return (sum (filter (\ (n) (= (% n 2) 0)) fib))))''', 4613732),
  # length
  ('(length \'(1 2 3))', 3),
  ('(length \'(1 2 3 4))', 4),
  ('(length \'())', 0),
  ('(length "string")', 6),
  ('(length "gazelle")', 7),
  ('(length 0)', TypeError),
  # list
  ('(list 1 2 3 4 5)', [1, 2, 3, 4, 5]),
  ('(list 1)', [1]),
  ('(list \'())', [[]]),
  ('(list)', []),
  ('(list? \'(1 2 3))', True),
  # map
  ('(map (\ (x) (* 2 x)) (range 5))', [0, 2, 4, 6, 8]),
  # max
  ('(max \'(1 2 3 4 5))', 5),
  ('(max "string")', 't'),
  ('(max "gazelle")', 'z'),
  ('(max 1)', TypeError),
  ('(max #t)', TypeError),
  # min
  ('(min \'(1 2 3 4 5))', 1),
  ('(min "string")', 'g'),
  ('(min "gazelle")', 'a'),
  ('(min 1)', TypeError),
  ('(min #t)', TypeError),
  # not
  ('(not #t)', False),
  ('(not 1)', False),
  ('(not "string")', False),
  ('(not "gazelle")', False),
  ('(not \'(1 2 3))', False),
  ('(not \'(#f #f #f))', False),
  # number?
  ('(number? 1)', True),
  ('(number? "1")', False),
  ('(number? #t)', False),
  ('(number? #f)', False),
  ('(number? \'(1 2 3))', False),
  ('(number? "string")', False),
  ('(number? "gazelle")', False),
  # proc?
  ('(proc? bool?)', True),
  ('(proc? #t)', False),
  ('(proc? 12345)', False),
  ('(proc? \'(1 2 3 4 5))', False),
  ('(proc? "string")', False),
  ('(proc? "gazelle")', False),
  # range
  ('(range 5)', [0, 1, 2, 3, 4]),
  ('(range 5 10)', [5, 6, 7, 8, 9]),
  ('(range "string")', TypeError),
  ('(range "gazelle")', TypeError),
  # "Weird" behavior
  ('(range #t)', [0]),
  ('(range #f)', []),
  # round
  ('(round 1.2)', 1.0),
  ('(round 1.7)', 2.0),
  ('(round "string")', TypeError),
  ('(round "gazelle")', TypeError),
  ('(round \'(1 2 3 4))', TypeError),
  # "Weird" behavior
  ('(round #t)', 1.0),
  ('(round #f)', 0.0),
  # str?
  ('(str? "string")', True),
  ('(str? "gazelle")', True),
  ('(str? 1)', False),
  ('(str? \'(1 2 3 4))', False),
  ('(str? #t)', False),
  ('(str? #f)', False),
  # sum
  ('(sum (range 5))', 10),
  ('(sum \'(0 1 2 3 4))', 10),
  ('(sum "string")', TypeError),
  ('(sum "gazelle")', TypeError),
  ('(sum #t)', TypeError),
  ('(sum #f)', TypeError),
  # "Weird" behavior
  ('(sum \'(#t #f))', 1),
]

# Test methods in the standard library
stdlib_tests = [
  ('(stdlib)', None),
  ('(and 1 2 3)', 3), 
  ('(and (> 2 1) 2 3)', 3), 
  ('(and)', True),
  ('(and (> 2 1) (> 2 3))', False),
  ('(nil? nil)', True),
  ('(nil? \'())', True),
  ('(= nil \'())', True),
  ('(reverse \'(1 2 3))', [3, 2, 1]),
]

# Test syntax by throwing errors
syntax_tests = [
  ('()', SyntaxError), 
  ('(set! x)', SyntaxError), 
  ('(def 3 4)', SyntaxError),
  ('(quote 1 2)', SyntaxError), 
  ('(if 1 2 3 4)', SyntaxError), 
  ('(\ 3 3)', SyntaxError), 
  ('(\ (x))', SyntaxError),
  ('''(if (= 1 2) (macro a 'a) 
   (macro a 'b))''', SyntaxError)
]

# Test tail recursion
tail_recursion_tests = [
  ('''(def (sum-squares-range start end)
     (def (sumsq-acc start end acc)
      (if (> start end) acc 
        (sumsq-acc 
          (+ start 1) end (+ (* start start) acc))))
     (sumsq-acc start end 0))''', None),
  ('(sum-squares-range 1 3000)', 9004500500)
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

def capture(expr, expected):
  ''' Run a test and capture output, comapre it to an expected
  value. '''

  # Attempt to run test normally
  try:
    result = eval(parse(expr))
    print('[:] ', expr, '=>', (result))
    return (result == expected)
  # Tests can raise exceptions, so capture them slightly differently
  except Exception as e:
    print('[#] ', expr, '=raises=>', type(e).__name__, e)
    # `issubclass` might not work on some tests, so we just capture any
    # TypeErrors and return false because that that point the test definitely
    # failed
    try:
      # Since we look for exceptions let's properly capture them and not
      # return False prematurely
      return issubclass(expected, Exception) and isinstance(e, expected)
    except TypeError:
      return False

def integration_tests():
  ''' Test each test case in all suites to 
  see if Gazelle code is being properly interpreted. '''

  fails = 0
  tests = 0

  # Iterate over each test in all suites
  for suite in suites:

    # Print section header
    colors.printf('\n' + suite[1] + ' Tests', colors.HEADER)

    # Iterate over tests in a suite
    for (expr, expected) in suite[0]:

      tests += 1 # Count our tests

      # Capture test output
      if not capture(expr, expected):
        
        # Failed a test if we reached here
        fails += 1
        colors.printf(('[!] FAIL: Expected: %s' 
          % str(expected)), colors.FAIL)

  # Print test results
  colors.printf(('%s %d out of %d tests fail.' 
    % ('*'*45, fails, tests)), colors.OKBLUE)

  # Print conclusion
  if fails == 0:
    colors.printf('[%] Testing concluded successfully', colors.OKGREEN)
  else:
    colors.printf('[!] Testing concluded with errors', colors.FAIL)

