# Roadmap

- Disjoint stdlib from loading on start. Should always be `include`d at the start of each file/repl. Might want to also add some kind of shorthand instead of the full file path, like `(include stdlib)`
- Fully document wiki. Possibly add set of html docs under /doc though it could just be local markdown files.
- Add some unit tests. Integration tests are good but do they really touch all the code? Testing will never 100% touch and rigorously prove every line of code work but some things could use a little more reassurance.
  - Maybe there is a better way to do tests as well, there could be something we're missing.
