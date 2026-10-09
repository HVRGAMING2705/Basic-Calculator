"""Recursive-descent parser: tokens -> AST.

Grammar:
    statement := IDENT "=" expr | expr
    expr      := term (("+" | "-") term)*
    term      := factor (("*" | "/" | "%") factor)*
    factor    := ("-" | "+") factor | power
    power     := primary ("^" factor)?        # right associative
    primary   := NUMBER | IDENT | call | "(" expr ")"
    call      := IDENT "(" [expr ("," expr)*] ")"
"""
from dataclasses import dataclass

from .errors import CalcSyntaxError
from .tokenizer import TokenType


@dataclass
class Number:
    value: float


@dataclass
class Var:
    name: str


@dataclass
class BinOp:
    op: str
    left: object
    right: object


@dataclass
class UnaryOp:
    op: str
    operand: object


@dataclass
class Call:
    name: str
    args: list


@dataclass
class Assign:
    name: str
    value: object


class Parser:
    def __init__(self, tokens, text):
        self.tokens = tokens
        self.text = text
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype, what):
        tok = self.peek()
        if tok.type is not ttype:
            raise CalcSyntaxError(f"expected {what}, found {tok.value!r}",
                                  self.text, tok.pos)
        return self.advance()

    def parse(self):
        node = self.parse_statement()
        tok = self.peek()
        if tok.type is not TokenType.EOF:
            raise CalcSyntaxError(f"unexpected trailing {tok.value!r}",
                                  self.text, tok.pos)
        return node

    def parse_statement(self):
        # assignment lookahead: IDENT followed by ASSIGN
        tok = self.peek()
        nxt = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
        if (tok.type is TokenType.IDENT and nxt is not None
                and nxt.type is TokenType.ASSIGN):
            self.advance()
            self.advance()
            return Assign(tok.value, self.parse_expr())
        return self.parse_expr()

    def parse_expr(self):
        node = self.parse_term()
        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            node = BinOp(op, node, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek().type in (TokenType.STAR, TokenType.SLASH,
                                   TokenType.PERCENT):
            op = self.advance().value
            node = BinOp(op, node, self.parse_factor())
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            return UnaryOp(tok.value, self.parse_factor())
        return self.parse_power()

    def parse_power(self):
        base = self.parse_primary()
        if self.peek().type is TokenType.CARET:
            self.advance()
            return BinOp("^", base, self.parse_factor())  # right-assoc
        return base

    def parse_primary(self):
        tok = self.peek()
        if tok.type is TokenType.NUMBER:
            self.advance()
            return Number(tok.value)
        if tok.type is TokenType.IDENT:
            self.advance()
            if self.peek().type is TokenType.LPAREN:
                self.advance()
                args = []
                if self.peek().type is not TokenType.RPAREN:
                    args.append(self.parse_expr())
                    while self.peek().type is TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expr())
                self.expect(TokenType.RPAREN, "')'")
                return Call(tok.value, args)
            return Var(tok.value)
        if tok.type is TokenType.LPAREN:
            self.advance()
            node = self.parse_expr()
            self.expect(TokenType.RPAREN, "')'")
            return node
        raise CalcSyntaxError(f"unexpected {tok.value!r}", self.text, tok.pos)


def parse(tokens, text):
    return Parser(tokens, text).parse()
