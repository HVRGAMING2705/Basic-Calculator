"""Tokenizer: source text -> stream of tokens."""
from dataclasses import dataclass
from enum import Enum, auto

from .errors import CalcSyntaxError


class TokenType(Enum):
    NUMBER = auto()
    IDENT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    CARET = auto()
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    ASSIGN = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    pos: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, pos={self.pos})"


_SINGLE = {
    "+": TokenType.PLUS, "-": TokenType.MINUS, "*": TokenType.STAR,
    "/": TokenType.SLASH, "%": TokenType.PERCENT, "^": TokenType.CARET,
    "(": TokenType.LPAREN, ")": TokenType.RPAREN, ",": TokenType.COMMA,
    "=": TokenType.ASSIGN,
}


def tokenize(text):
    """Split an expression string into tokens. Raises CalcSyntaxError on
    illegal characters."""
    tokens, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < n and text[i + 1].isdigit()):
            start = i
            seen_dot = False
            while i < n and (text[i].isdigit() or (text[i] == "." and not seen_dot)):
                if text[i] == ".":
                    seen_dot = True
                i += 1
            tokens.append(Token(TokenType.NUMBER, float(text[start:i]), start))
            continue
        if ch.isalpha() or ch == "_":
            start = i
            while i < n and (text[i].isalnum() or text[i] == "_"):
                i += 1
            tokens.append(Token(TokenType.IDENT, text[start:i], start))
            continue
        if ch in _SINGLE:
            tokens.append(Token(_SINGLE[ch], ch, i))
            i += 1
            continue
        raise CalcSyntaxError(f"unexpected character {ch!r}", text, i)
    tokens.append(Token(TokenType.EOF, None, n))
    return tokens
