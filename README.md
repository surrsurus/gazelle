# gazelle [![Build Status](https://travis-ci.org/surrsurus/gazelle.svg?branch=master)](https://travis-ci.org/surrsurus/gazelle) ![Python Version](https://img.shields.io/badge/python-3.6-green.svg)  [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) 

Gazelle is a tiny lisp-like scripting language built with Python.  

Gazelle is:
- **Easy to setup** 
  - Have Python? You can run Gazelle. Gazelle requires no external dependencies (that shouldn't be already downloaded)
- **Inspired by LISP and Scheme**
  - Gazelle code is written entirely with prefix notation in the form `(procedure expression)`
  - Gazelle has no true AST, instead the programmer ends up directly coding the AST for Gazelle to interpret
  - Only 3 fundamental types: Atoms, Lists, and Procedures
- **Extendable**
  - Adding features to Gazelle is simple and easy through editing the python source or via directly programming in Gazelle itself

Not convinced? Gazelle can be used to write answers to Project Euler questions. Here's problem 1:

```
(return (sum (filter (\ (n) (or (= (% n 5) 0) (= (% n 3) 0))) (range 1000))))
```

## Getting Started

Here's how you can get started programming in Gazelle.

### Prerequisites

Before you can run Gazelle, you'll need to have [Python 3.7](https://www.python.org/downloads/) installed for your respective OS. Then, make sure to download either the [latest release](https://github.com/surrsurus/gazelle/releases) of Gazelle or the latest master.

### Running Gazelle

For more detail, check out the [getting started guide](https://github.com/surrsurus/gazelle/wiki/Getting-Started)

#### Windows

To run the repl, you can run `win-repl.bat` in the root directory of Gazelle. You could also run `python gazelle.py`.

#### Linux/OSX

To run the repl on linux/OSX, you can run `linux-repl.bat` in the root directory of Gazelle. You could also run `python2 gazelle.py`.

### Basic Usage

The Gazelle REPL provides all the basic utility you need to begin toying with it.

In addition, files can be ran by using a file path as your argument such as `python gazelle.py ./example/one.gel` and files can be run in succession such as `python gazelle.py ./euler/one.gel ./euler/two.gel`

### Running the Tests

To run the tests, run the `run_tests.py` file from the root directory.

### Code Examples

Take a look at the [getting started guide](https://github.com/surrsurus/gazelle/wiki/Getting-Started) and our [documentation](https://github.com/surrsurus/gazelle/wiki/Documentation) to learn how to code with Gazelle. You can view example programs in the [examples folder](https://github.com/surrsurus/gazelle/tree/master/example) packaged with Gazelle.

## Contributing

Take a look at [this page](https://github.com/surrsurus/gazelle/blob/master/CONTRIBUTING.md) you can contribute to Gazelle.

## License

<img align="center" src="https://licensebuttons.net/l/GPL/2.0/88x62.png" alt="GPL" width=100>

This code is released under the GNU GENERAL PUBLIC LICENSE. All works in this repository are meant to be utilized under this license. You are entitled to remix, remodify, and redistribute this program as you see fit, under the condition that all derivative works must use the GPL Version 3.

## Acknowledgements

Inspiration from [here](http://norvig.com/lispy2.html)

And the original [LISP paper by McCarthy](http://www-formal.stanford.edu/jmc/recursive.html)


