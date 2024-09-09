from imp.lexer import TokenType, Lexer
from imp.grammar import *
from typing import Dict, Any

# This is the table that is used to determine which production should be used
# for non terminals with multiple productions.
parse_table: Dict[NonTerminal, Dict[TokenType, Production]] = {
    NonTerminal.ArithExp: {
        TokenType.INT: Production.ArithExpInt,
        TokenType.ID: Production.ArithExpId,
    },
    NonTerminal.ArithExp_: {
        TokenType.PLUS:   Production.ArithExp_Sum,
        TokenType.DIVIDE: Production.ArithExp_Div,
    },
    NonTerminal.BoolExp: {
        TokenType.BOOL: Production.BoolExpBool,
        # Tokens that start an ArithExp imply BoolExpLEQ
        TokenType.INT:      Production.BoolExpLEQ,
        TokenType.ID:       Production.BoolExpLEQ,
        TokenType.NEGATION: Production.BoolExpNegation,
    },
    NonTerminal.BoolExp_: {
        TokenType.AND: Production.BoolExp_And,
    },
    NonTerminal.Statements: {
        # Tokens that start a Statement imply StatementsSequence
        TokenType.ID:    Production.StatementsSequence,
        TokenType.IF:    Production.StatementsSequence,
        TokenType.WHILE: Production.StatementsSequence,
    },
    NonTerminal.Statement: {
        TokenType.ID:    Production.StatementAssignment,
        TokenType.IF:    Production.StatementIf,
        TokenType.WHILE: Production.StatementWhile,
    }
}

###########################################
# Parser Definition

class Parser:
    def __init__(self, program: str):
        self.program = program
        self.lexer = Lexer(program)

    def parse(self) -> Program:
        """
        The top level parsing method.
        This is the only thing clients should use.
        """
        try:
            return self._parse_program()
        except Exception as e:
            lineno = self.lexer.get_line_number()
            error_line = self._get_current_line()
            e.add_note("Parsing failure on line {}:\n{}".format(lineno, error_line))
            raise e
    
    def _get_current_line(self) -> str:
        lineno = self.lexer.get_line_number()
        line = self.program.splitlines()[lineno-1]
        return line

    def _expect(self, sym: TokenType) -> Any:
        """
        Helper function for consuming one token of input.
        :param sym: The TokenType that the parser expects the next token to be.
        """
        tok = self.lexer.next()
        assert tok.type == sym, "Expected {}, but found {}".format(sym, tok)
        return tok.value

    def _parse_int(self) -> Int:
        value = self._expect(TokenType.INT)
        return Int(value)

    def _parse_bool(self) -> Bool:
        value = self._expect(TokenType.BOOL)
        return Bool(value)

    def _parse_id(self) -> Id:
        ident = self._expect(TokenType.ID)
        return Id(ident)

    def _parse_arith_exp(self) -> ArithExp:
        next_tok = self.lexer.peek()
        match parse_table[NonTerminal.ArithExp][next_tok.type]:

            # <ArithExp> ::= <Int> <ArithExp_>
            case Production.ArithExpInt:
                val = self._parse_int()
                remain = self._parse_arith_exp_()
                return ArithExpInt(val, remain)

            # <ArithExp> ::= <Id> <ArithExp_>
            case Production.ArithExpId:
                val = self._parse_id()
                remain = self._parse_arith_exp_()
                return ArithExpId(val, remain)

            case _:
                assert False

    def _parse_arith_exp_(self) -> ArithExp_:
        next_tok = self.lexer.peek()
        # Since an ArithExp_ can be empty, it's possible the parse table won't find the upcoming token
        match parse_table[NonTerminal.ArithExp_].get(next_tok.type, None):
            # <ArithExp_> ::= <>
            case None:
                return None

            # <ArithExp_> ::= + <ArithExp> <ArithExp_>
            case Production.ArithExp_Sum:
                self._expect(TokenType.PLUS)
                exp = self._parse_arith_exp()
                remain = self._parse_arith_exp_()
                return ArithExp_Sum(exp, remain)

            # <ArithExp_> ::= / <ArithExp> <ArithExp_>
            case Production.ArithExp_Div:
                self._expect(TokenType.DIVIDE)
                exp = self._parse_arith_exp()
                remain = self._parse_arith_exp_()
                return ArithExp_Div(exp, remain)

            case _:
                assert False

    def _parse_bool_exp(self) -> BoolExp:
        next_tok = self.lexer.peek()
        match parse_table[NonTerminal.BoolExp][next_tok.type]:
            # <BoolExp> ::= <Bool> <BoolExp_>
            case Production.BoolExpBool:
                val = self._parse_bool()
                remain = self._parse_bool_exp_()
                return BoolExpBool(val, remain)

            # <BoolExp> ::= <ArithExp> <= <ArithExp> <BoolExp_>
            case Production.BoolExpLEQ:
                lhs = self._parse_arith_exp()
                self._expect(TokenType.LEQ)
                rhs = self._parse_arith_exp()
                remain = self._parse_bool_exp_()
                return BoolExpLEQ(lhs, rhs, remain)

            # <BoolExp> ::= ! <BoolExp> <BoolExp_>
            case Production.BoolExpNegation:
                self._expect(TokenType.NEGATION)
                exp = self._parse_bool_exp()
                remain = self._parse_bool_exp_()
                return BoolExpNegation(exp, remain)

            case _:
                assert False

    def _parse_bool_exp_(self) -> BoolExp_:
        next_tok = self.lexer.peek()
        # Since a BoolExp_ can be empty, it's possible the parse table won't find the upcoming token
        match parse_table[NonTerminal.BoolExp_].get(next_tok.type, None):
            # <BoolExp_> ::= <>
            case None:
                return None

            # <BoolExp_> ::= && <BoolExp> <BoolExp_>
            case Production.BoolExp_And:
                self._expect(TokenType.AND)
                exp = self._parse_bool_exp()
                remain = self._parse_bool_exp_()
                return BoolExp_And(exp, remain)

            case _:
                assert False

    def _parse_statement(self) -> Statement:
        next_tok = self.lexer.peek()
        match parse_table[NonTerminal.Statement][next_tok.type]:
            # <Statement> ::= <Id> = <ArithExp> ;
            case Production.StatementAssignment:
                ident = self._parse_id()
                self._expect(TokenType.ASSIGN)
                exp = self._parse_arith_exp()
                self._expect(TokenType.SEMICOLON)
                return StatementAssignment(ident, exp)

            # <Statement> ::= if ( <BoolExp> ) <Block> else <Block>
            case Production.StatementIf:
                self._expect(TokenType.IF)
                self._expect(TokenType.LPAREN)
                cond = self._parse_bool_exp()
                self._expect(TokenType.RPAREN)
                if_body = self._parse_block()
                self._expect(TokenType.ELSE)
                else_body = self._parse_block()
                return StatementIf(cond, if_body, else_body)

            # <Statement> ::= while ( <BoolExp> ) <Block>
            case Production.StatementWhile:
                self._expect(TokenType.WHILE)
                self._expect(TokenType.LPAREN)
                cond = self._parse_bool_exp()
                self._expect(TokenType.RPAREN)
                body = self._parse_block()
                return StatementWhile(cond, body)

            case _:
                assert False

    def _parse_statements(self) -> Statements:
        next_tok = self.lexer.peek()
        # Since Statements can be empty, it's possible the parse table won't find the upcoming token
        match parse_table[NonTerminal.Statements].get(next_tok.type, None):
            # <Statements> ::= <>
            case None:
                return None

            # <Statements> ::= <Statement> <Statements>
            case Production.StatementsSequence:
                stmt = self._parse_statement()
                remain = self._parse_statements()
                return StatementsSequence(stmt, remain)

            case _:
                assert False

    def _parse_block(self) -> Block:
        # <Block> ::= { <Statements>}
        self._expect(TokenType.LCURLY)
        stmts = self._parse_statements()
        self._expect(TokenType.RCURLY)
        return Block(stmts)


    def _parse_program(self) -> Program:
        # <Program> ::= <Statements> *EOF*
        stmts = self._parse_statements()
        self._expect(TokenType.EOF)
        return Program(stmts)

if __name__ == '__main__':
    test_data = '''
    i = 7;
    _foo87_ = 29;
    while (i <= 10) {
        i = i + 1;
    }
    if (i <= _foo87_) {
        i = 0;
    } else {
    }
    '''

    parser = Parser(test_data)
    pretty_print(parser.parse())