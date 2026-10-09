"""Test suite for the Expression Parser Calculator. Run with:
    python test_calc.py
"""
import math

from calc import Evaluator, calculate, CalcSyntaxError, CalcNameError, CalcMathError

PASS = 0
FAIL = 0


def check(expr, expected, ev=None):
    global PASS, FAIL
    try:
        got = calculate(expr, ev)
        ok = abs(got - expected) < 1e-9
    except Exception as exc:  # noqa: BLE001
        got, ok = f"{type(exc).__name__}: {exc}", False
    if ok:
        PASS += 1
    else:
        FAIL += 1
        print(f"FAIL {expr!r}: expected {expected}, got {got}")


def check_raises(expr, exc_type, ev=None):
    global PASS, FAIL
    try:
        calculate(expr, ev)
    except exc_type:
        PASS += 1
        return
    except Exception as exc:  # noqa: BLE001
        FAIL += 1
        print(f"FAIL {expr!r}: expected {exc_type.__name__}, got {type(exc).__name__}")
        return
    FAIL += 1
    print(f"FAIL {expr!r}: expected {exc_type.__name__}, no error raised")


def main():
    global PASS, FAIL
    ev = Evaluator()
    # precedence & associativity
    check("2 + 3 * 4", 14, ev)
    check("(2 + 3) * 4", 20, ev)
    check("10 - 2 - 3", 5, ev)          # left assoc
    check("2 ^ 3 ^ 2", 512, ev)         # right assoc: 2^(3^2)
    check("-3 ^ 2", -9, ev)             # unary binds looser than ^
    check("(-3) ^ 2", 9, ev)
    check("10 % 3", 1, ev)
    check("7 / 2", 3.5, ev)
    check("--5", 5, ev)
    # functions & constants
    check("sin(pi / 2)", 1, ev)
    check("cos(0)", 1, ev)
    check("sqrt(16)", 4, ev)
    check("log(e)", 1, ev)
    check("log(100, 10)", 2, ev)
    check("max(3, 9, 4)", 9, ev)
    check("abs(-7)", 7, ev)
    check("2 * pi", 2 * math.pi, ev)
    # variables
    check("x = 5", 5, ev)
    check("x * 2", 10, ev)
    check("y = x ^ 2 + 1", 26, ev)
    check("y", 26, ev)
    # errors
    check_raises("2 +", CalcSyntaxError, ev)
    check_raises("(2 + 3", CalcSyntaxError, ev)
    check_raises("2 & 3", CalcSyntaxError, ev)
    check_raises("1 / 0", CalcMathError, ev)
    check_raises("sqrt(-1)", CalcMathError, ev)
    check_raises("nope + 1", CalcNameError, ev)
    check_raises("nosuchfn(2)", CalcNameError, ev)
    check_raises("pi = 3", CalcNameError, ev)

    print(f"\n{PASS} passed, {FAIL} failed")
    raise SystemExit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
