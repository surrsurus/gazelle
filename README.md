# gazelle
Gazelle - A scripting language inspired by LISP and Scheme

# Why Gazelle?
Gazelle is:
- **Easy to setup** 
  - Have Python 2? You can run Gazelle. Gazelle requires no external dependencies (that shouldn't be already downloaded)
- **Inspired by LISP and Scheme**
  - Gazelle code is written entirely with prefix notation in the form `(procedure expression)`
  - Gazelle has no true AST, instead the programmer ends up directly coding the AST for Gazelle to interpret
  - Only 3 fundamental types: Atoms, Lists, and Procedures
- **Extendable**
  - Adding features to Gazelle is simple and easy through editing the python source or via directly programming in Gazelle itself

The interpreter has a REPL and can run gazelle files, and contains everything you need to get started when coding.

# Not convinced?
Gazelle can be used to write answers to Project Euler questions. Here's problem 1:

`(return (sum (filter (\ (n) (or (= (% n 5) 0) (= (% n 3) 0))) (range 1000))))`

# How to use

#### Windows

1. Firstly, you'll need Python 2 which can be downloaded [here](https://www.python.org/downloads/)
2. You'll then need to download the [latest release](https://github.com/surrsurus/gazelle/releases)
3. Then, start the REPL. Run the REPL by running `win-repl.bat` in the directory of `gazelle-master`

#### Linux

1. Install Python 2 with your package manager of choice (though on most distros it should be included by default)
2. Run `linux-repl.sh`

# Basic Usage

The Gazelle REPL should provide the necessary testing environment for your deercode usage.

In addition, files can be ran by using a file path as your argument such as `python gazelle.py ./euler/one.gel` and files can be run in succession such as `python gazelle.py ./euler/one.gel ./euler/two.gel`

## Code examples

Take a look at the [getting started guide](https://github.com/surrsurus/gazelle/wiki/Getting-Started) and our [documentation](https://github.com/surrsurus/gazelle/wiki/Documentation) to learn how to code with deercode. You can view example programs in the [examples folder](https://github.com/surrsurus/gazelle/tree/master/example) packaged with deercode

## Run Tests

Run the integration tests by executing `python gazelle.py test`

# Shortcomings

Gazelle is very much lacking when it comes to efficiency. Gazelle lacks tail-call optimizations and lazy evaluation, two things that would make Gazelle much faster. Python really limits what deercode can do and we're looking to begin porting this to a different language

In addition, Gazelle is pretty tough to read and the REPL lacks parentheses completion which may hinder your REPL experience.

# Contributing
Take a look at [this page](https://github.com/surrsurus/gazelle/blob/master/CONTRIBUTING.md) you can contribute to Gazelle.

## Credits
Inspiration from: [This webste](http://norvig.com/lispy2.html)

And the original LISP Paper by McCarthy: [here](http://www-formal.stanford.edu/jmc/recursive.html)

## License

<img align="center" src="https://licensebuttons.net/l/GPL/2.0/88x62.png" alt="GPL" width=100>

This code is released under the GNU GENERAL PUBLIC LICENSE. All works in this repository are meant to be utilized under this license. You are entitled to remix, remodify, and redistribute this program as you see fit, under the condition that all derivative works must use the GPL Version 3.