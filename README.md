# Expression Parser Calculator

The original notebook did arithmetic with plain functions. This is a real
expression evaluator: a **tokenizer** plus a **recursive-descent parser**
that builds an AST, plus an evaluator with variables and math functions.

## Features

- Operator precedence: `^` (right-associative) > unary minus > `*` `/` `%`
  > `+` `-`; parentheses
- Math functions: sin cos tan asin acos atan sqrt exp log ln abs floor
  ceil round max min
- Constants: `pi`, `e`, `tau`
- Variables and assignment: `x = 5`, then `x * 2`
- Clean errors with source position pointers:
  `CalcSyntaxError`, `CalcNameError`, `CalcMathError`
- Interactive REPL (`repl.py`) with `vars`, `funcs`, `help`
- 29-case test suite (`test_calc.py`)

## How to run

```bash
python repl.py          # interactive calculator
python test_calc.py     # run the test suite (29 tests)
```

```python
from calc import calculate
calculate("2 + 3 * (4 - 1) ^ 2")   # 29.0
calculate("sin(pi / 2) + log(100, 10)")  # 3.0
```

## Grammar

```
statement := IDENT "=" expr | expr
expr      := term (("+" | "-") term)*
term      := factor (("*" | "/" | "%") factor)*
factor    := ("-" | "+") factor | power
power     := primary ("^" factor)?
primary   := NUMBER | IDENT | call | "(" expr ")"
```

## Project layout

```
calc/
  tokenizer.py   source text -> tokens
  parser.py      tokens -> AST (recursive descent)
  evaluator.py   AST -> value (variables, functions, constants)
  errors.py      exception hierarchy with position info
repl.py          interactive shell
test_calc.py     29 test cases
```
