#!/usr/bin/env python3

import parcon
from parcon import (Exact, ZeroOrMore, AnyChar, CharIn, Forward, Optional,
                    InfixExpr, OneOrMore, Literal, Whitespace)
import collections
import operator

def symbol(x):
    if x == 'nil':
        return None
    elif x in ('false', 'f'):
        return False
    elif x in ('true', 't'):
        return True
    return x


class Keyword(collections.namedtuple('Keyword', 'key value')):
    @classmethod
    def fromPair(cls, key, value):
        return Keyword(key, value)

    def __add__(self, other):
        return AddDict(self, other)


class AddDict(dict):
    def __init__(self, *keywords):
        if keywords:
            super().__init__(**{keyword.key: keyword.value
                                for keyword in keywords})
        super().__init__()
    def __add__(self, other):
        if isinstance(other, Keyword):
            self[other.key] = other.value
        elif isinstance(other, dict):
            self.update(other)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: 'dict' and {}".format(
                    type(other)))
        return self


def parseNumber(x):
    if '.' in x:
        return float(x)
    return int(x)

def add_dict(left, right):
    print(left, right)
    return left + right


def infix(constructor, adder=operator.add):
    return Exact(
        InfixExpr(sexp[lambda x: constructor([x])],
                  [(OneOrMore(CharIn(parcon.whitespace)), adder)])
        )

sexp = Forward()
name = parcon.OneOrMore(
    parcon.AnyChar() - parcon.CharIn("()',:[]{} "))["".join]
number = parcon.rational[parseNumber]
symbol = ("'" + name)[symbol]
string = ('"' + Exact(ZeroOrMore(AnyChar() - CharIn('\"'))) + '"')["".join]
keyword = (name + ":" + sexp[lambda x: (x,)])[
    lambda x: Keyword.fromPair(*x)]
sexp_tuple = ("(" + Optional(infix(tuple), tuple()) + ")")
sexp_list = "[" + Optional(infix(list), list()) + "]"
sexp_dict = ("{" +
             Optional(infix(lambda x: AddDict(x[0]), add_dict), dict()) +
             "}")
sexp << (sexp_list | sexp_namedtuple | sexp_tuple | sexp_dict |
         number | string | keyword | symbol | name)


def loads(s):
    return sexp.parse_string(s)


def load(f):
    return loads(f.read())
