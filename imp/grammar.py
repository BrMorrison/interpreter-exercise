from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

###########################################
# Grammar Enums

# Top-level grammar objects
class NonTerminal(Enum):
    Int = auto()
    Bool = auto()
    Id = auto()
    ArithExp = auto()
    ArithExp_ = auto()
    BoolExp = auto()
    BoolExp_ = auto()
    Block = auto()
    Statements = auto()
    Statement = auto()
    Program = auto()

# The way the non-terminals can be constructed
class Production(Enum):
    Int = auto()
    Bool = auto()
    Id = auto()
    ArithExpInt = auto()
    ArithExpId = auto()
    ArithExp_Sum = auto()
    ArithExp_Div = auto()
    BoolExpBool = auto()
    BoolExpLEQ = auto()
    BoolExpNegation = auto()
    BoolExp_And = auto()
    Block = auto()
    StatementsSequence = auto()
    StatementAssignment = auto()
    StatementIf = auto()
    StatementWhile = auto()
    Program = auto()

###########################################
# Literals and Identifiers

@dataclass
class Int:
    value: int

@dataclass
class Bool:
    value: bool

@dataclass
class Id:
    value: str

###########################################
# Arithmetic Expressions

@dataclass
class ArithExpInt:
    value: Int
    remain: ArithExp_

@dataclass
class ArithExpId:
    value: Id
    remain: ArithExp_

ArithExp = ArithExpInt | ArithExpId

@dataclass
class ArithExp_Sum:
    exp: ArithExp
    remain: ArithExp_

@dataclass
class ArithExp_Div:
    exp: ArithExp
    remain: ArithExp_

ArithExp_ = ArithExp_Sum | ArithExp_Div | None

###########################################
# Boolean Expressions

@dataclass
class BoolExpBool:
    value: Bool
    remain: BoolExp_

@dataclass
class BoolExpLEQ:
    lhs: ArithExp
    rhs: ArithExp
    remain: BoolExp_

@dataclass
class BoolExpNegation:
    exp: BoolExp
    remain: BoolExp_

BoolExp = BoolExpBool | BoolExpLEQ | BoolExpNegation

@dataclass
class BoolExp_And:
    exp: BoolExp
    remain: BoolExp_

BoolExp_ = BoolExp_And | None

###########################################
# Statements, Programs, and Blocks

@dataclass
class StatementAssignment:
    id: Id
    exp: ArithExp

@dataclass
class StatementIf:
    cond: BoolExp
    if_body: Block
    else_body: Block

@dataclass
class StatementWhile:
    cond: BoolExp
    body: Block

Statement = StatementAssignment | StatementIf | StatementWhile

@dataclass
class StatementsSequence:
    stmt: Statement
    remain: Statements

Statements = StatementsSequence | None

@dataclass
class Block:
    stmts: Statements

@dataclass
class Program:
    stmts: Statements

###########################################
# Helper Functions

def pretty_print(obj, indentation: str =""):
    """
    Prints a somewhat readable representation of a syntax object
    """
    # If it's something simple, just print it and return
    match obj:
        case Int(val):
            print("(Int: {})".format(val))
            return
        case Bool(val):
            print("(Bool: {})".format(val))
            return
        case Id(name):
            print("(Id: {})".format(name))
            return
        case None:
            print("None")
            return

    # If it's more complex, then print its members recursively
    print("(" + type(obj).__name__ + ":")
    for field in obj.__dataclass_fields__.keys():
        new_indentation = indentation + '| '
        print(new_indentation + field + ': ', end='')
        value = obj.__getattribute__(field)
        pretty_print(value, new_indentation)
    print(indentation + ")")
