# deercode
Deercode - a high level lisp-like scripting language built on top of python

<img align="center" src="https://github.com/surrsurus/deercode/blob/master/media/deercode.PNG" alt="deercode" width=350>


# Why deercode?
Deercode is:
- **Easy to install** 
  - Deercode is built on python, meaning you can probably already run the deercode REPL
- **Inspired by functional languages**
  - Expressions take the form of `(func args)` and encourage the use of `map`, `compress`, and `lambdas` as deercode has no support for any function definition other than lambda expressions
- **Lisp-like**
  - Deercode has `car`, `cons`, and `cdr` and aims to be useful for manipulating lists and applying functions to them similarly to lisp

The interpreter has a REPL and can run deercode files, everything you need to get started when coding in deercode!

# Not convinced?
Deercode can be used to write answers to project euler questions. Here's problem 1:

`(sum (compress (grange 1000) (map (lamb (n) (or (= (% n 5) 0) (= (% n 3) 0))) (grange 1000))))`

Deercode's functional style lends itself towards creating long one-liners like this, and if you want to try it for yourself, Euler problem solutions are included in the `euler` directory.

# How to use

#### Windows

1. Firstly, you'll need Python 3.5 which can be downloaded [here](https://www.python.org/downloads/)
    - Python 3.6 also works but you'll need to edit line 1 of `di`
2. You'll then need to download the current master branch from this GitHub
3. Then, start the REPL. Run the REPL by running `py di` in the directory of `di`

#### Linux

1. Install Python 3.5 with your package manager of choice
2. Run `chmod +x` on `di`
3. Run `./di` with no arguments to open the REPL

# Basic Usage

The Deercode REPL should provide the necessary testing environment for your deercode usage.

In addition, files can be ran by using a file path as your argument such as `di hello.deer` or `di ./euler/eulerOne.deer`

You can always `(include)` a file in deercode and it will be evaluated.

## Code examples

Take a look at the [getting started guide](https://github.com/surrsurus/deercode/wiki/Getting-Started) and our [documentation](https://github.com/surrsurus/deercode/wiki/Documentation) to learn how to code with deercode. You can view example programs in the [examples folder](https://github.com/surrsurus/deercode/tree/master/example) packaged with deercode

# Shortcomings

Deercode really lacks a lot of the cool functional stuff haskell has like tail-call optimizations. Python really limits what deercode can do and we're looking to begin porting this to a different language

In addition, deercode is pretty tough to read and the REPL lacks parentheses completion which may hinder your REPL experience.

# Contributing
Take a look at [this page](https://github.com/surrsurus/deercode/wiki/Contributing) you can contribute to deercode.

## Special thanks and some credits
Special thanks to [this website](http://norvig.com/lispy.html) for providing a nice base for the interpreter to be expanded on. Thanks!

ASCII Art deer found [here](http://www.chris.com/ascii/index.php?art=animals/deer).

## License

<img align="left" src="https://licensebuttons.net/l/GPL/2.0/88x62.png" alt="GPL" width=100>


This code is released under the GNU GENERAL PUBLIC LICENSE. All works in this repository are meant to be utilized under this license. You are entitled to remix, remodify, and redistribute this program as you see fit, under the condition that all derivative works must use the GPL Version 3.
