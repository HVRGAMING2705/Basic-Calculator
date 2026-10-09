"""Exception hierarchy with source-position information."""


class CalcError(Exception):
    """Base class for all calculator errors."""


class CalcSyntaxError(CalcError):
    def __init__(self, message, text="", pos=0):
        self.text = text
        self.pos = pos
        pointer = " " * pos + "^" if text else ""
        super().__init__(f"syntax error at position {pos}: {message}\n{text}\n{pointer}")


class CalcNameError(CalcError):
    pass


class CalcMathError(CalcError):
    pass
