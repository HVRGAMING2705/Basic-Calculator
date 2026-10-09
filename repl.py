"""Interactive REPL for the Expression Parser Calculator."""
from calc import Evaluator, calculate, CalcError, FUNCTIONS

HELP = """Commands:
  <expression>   evaluate, e.g. 2 + 3 * (4 - 1) ^ 2
  x = <expr>     assign a variable
  vars           list variables
  funcs          list available functions
  help           this message
  exit / quit    leave

Operators: + - * / % ^ (power), parentheses, unary minus.
Functions: sin cos tan asin acos atan sqrt exp log ln abs floor ceil round max min
Constants: pi e tau
"""


def main():
    ev = Evaluator()
    print("Expression Parser Calculator — type 'help', 'exit' to quit.")
    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("exit", "quit"):
            break
        if line == "help":
            print(HELP)
            continue
        if line == "vars":
            for k in sorted(ev.env):
                print(f"  {k} = {ev.env[k]}")
            continue
        if line == "funcs":
            print("  " + ", ".join(sorted(FUNCTIONS)))
            continue
        try:
            result = calculate(line, ev)
            # print ints without trailing .0
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            print(result)
        except CalcError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
