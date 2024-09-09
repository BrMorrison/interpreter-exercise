from imp.lexer import Lexer, TokenType, Token
import pytest

class TestBasicLexer:
    """
    Tests that cover the tokens found in the basic language
    """

    def test_lex_positive_int(self):
        """
        Tests that we can lex positive numbers
        """
        lex = Lexer("123 456")
        expected = [123, 456]
        for num in expected:
            assert num == lex.next().value
        assert TokenType.EOF == lex.next().type
    
    @pytest.mark.skip
    def test_lex_negative_int(self):
        """
        Tests that we can lex negative numbers
        Note: this isn't supported because it would make parsing things like '10-5' hard.
        """
        lex = Lexer("-123 -456")
        expected = [-123, -456]
        for num in expected:
            assert num == lex.next().value
        assert TokenType.EOF == lex.next().type

    def test_lex_id(self):
        """
        Test that we can lex different identifiers
        """
        lex = Lexer("foo __hi__ bar_foo20")
        expected = ['foo', '__hi__', 'bar_foo20']
        for num in expected:
            assert num == lex.next().value
        assert TokenType.EOF == lex.next().type

    def test_lex_bool(self):
        """
        Test that we can lex bool literals (and don't lex things that aren't bools as bools)
        """
        lex = Lexer("true false False True truet falsef istrue ifalse")
        expected = [
            Token(TokenType.BOOL, True),
            Token(TokenType.BOOL, False),
            Token(TokenType.ID, "False"),
            Token(TokenType.ID, "True"),
            Token(TokenType.ID, "truet"),
            Token(TokenType.ID, "falsef"),
            Token(TokenType.ID, "istrue"),
            Token(TokenType.ID, "ifalse"),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    
    def test_lex_arithmetic(self):
        """
        Lex the basic arithmetic operators (+ and /)
        """
        lex = Lexer("++=/ /+=")
        expected = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.DIVIDE, '/'),
            Token(TokenType.DIVIDE, '/'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.ASSIGN, '='),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_logic(self):
        """
        Lex the basic logic operators (! and &&)
        """
        lex = Lexer("&& !&&&&!!")
        expected = [
            Token(TokenType.AND, '&&'),
            Token(TokenType.NEGATION, '!'),
            Token(TokenType.AND, '&&'),
            Token(TokenType.AND, '&&'),
            Token(TokenType.NEGATION, '!'),
            Token(TokenType.NEGATION, '!'),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_comparison(self):
        """
        Lex the <= comparison operator
        """
        lex = Lexer("<=<= <=")
        expected = [
            Token(TokenType.LEQ, '<='),
            Token(TokenType.LEQ, '<='),
            Token(TokenType.LEQ, '<='),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_punctuation(self):
        """
        Lex the punctuation tokens (){};
        """
        lex = Lexer("})}{;;(()")
        expected = [
            Token(TokenType.RCURLY, '}'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.RCURLY, '}'),
            Token(TokenType.LCURLY, '{'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_keywords(self):
        """
        Test that we can lex keywords (and don't lex things that aren't keywords as keywords)
        """
        lex = Lexer("if else while ifelsewhile elsewhileif whileifelse")
        expected = [
            Token(TokenType.IF, 'if'),
            Token(TokenType.ELSE, 'else'),
            Token(TokenType.WHILE, 'while'),
            Token(TokenType.ID, 'ifelsewhile'),
            Token(TokenType.ID, 'elsewhileif'),
            Token(TokenType.ID, 'whileifelse'),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

class TestExtendedLexer:
    """
    Tests that cover the tokens found in the language extensions.
    """

    def test_lex_arithmetic_extended(self):
        """
        Lex the extended arithmetic operators (- and *)
        """
        lex = Lexer("---***--*-")
        expected = [
            Token(TokenType.MINUS, '-'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.TIMES, '*'),
            Token(TokenType.TIMES, '*'),
            Token(TokenType.TIMES, '*'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.TIMES, '*'),
            Token(TokenType.MINUS, '-'),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_logic_extended(self):
        """
        Lex the extended logic operator (||)
        """
        lex = Lexer("||||||")
        expected = [
            Token(TokenType.OR, '||'),
            Token(TokenType.OR, '||'),
            Token(TokenType.OR, '||'),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type

    def test_lex_comparison_extended(self):
        """
        Lex the extended comparison operators (==, !=, >=, <, and >)
        """
        lex = Lexer("==!===<>=>>===")
        expected = [
            Token(TokenType.EQ, '=='),
            Token(TokenType.NEQ, '!='),
            Token(TokenType.EQ, '=='),
            Token(TokenType.LT, '<'),
            Token(TokenType.GEQ, '>='),
            Token(TokenType.GT, '>'),
            Token(TokenType.GEQ, '>='),
            Token(TokenType.EQ, '=='),
            ]
        for val in expected:
            assert val == lex.next()
        assert TokenType.EOF == lex.next().type
