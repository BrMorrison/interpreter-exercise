from imp.grammar import *
from imp.parser import Parser

class TestBasicParser:
    def test_parse_assign_literal(self):
        test_str = 'i = 20;'
        expected = Program(StatementsSequence(
            StatementAssignment(
                Id('i'),
                ArithExpInt(Int(20), None)),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_assign_math(self):
        test_str = 'i = 8 + x/7;'
        expected = Program(StatementsSequence(
            StatementAssignment(
                Id('i'),
                ArithExpInt(
                    Int(8),
                    ArithExp_Sum(
                        ArithExpId(
                            Id('x'),
                            ArithExp_Div(
                                ArithExpInt(Int(7), None),
                                None)),
                        None))),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_if_literal_condition(self):
        test_str = 'if(false){}else{}'
        expected = Program(StatementsSequence(
            StatementIf(
                BoolExpBool(Bool(False), None),
                Block(None),
                Block(None)),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_while_bool_logic(self):
        test_str = 'while(!false && true){}'
        expected = Program(StatementsSequence(
            StatementWhile(
                BoolExpNegation(
                    BoolExpBool(
                        Bool(False),
                        BoolExp_And(
                            BoolExpBool(Bool(True), None),
                            None)),
                        None),
                Block(None)),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_while_leq(self):
        test_str = 'while(7 <= 13){}'
        expected = Program(StatementsSequence(
            StatementWhile(
                BoolExpLEQ(
                    ArithExpInt(Int(7), None),
                    ArithExpInt(Int(13), None),
                    None),
                Block(None)),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_non_empty_block(self):
        test_str = 'while(true){ var = 17; }'
        expected = Program(StatementsSequence(
            StatementWhile(
                BoolExpBool(Bool(True), None),
                Block(StatementsSequence(
                    StatementAssignment(
                        Id('var'),
                        ArithExpInt(Int(17), None)),
                    None))),
            None))
        parsed = Parser(test_str).parse()
        assert parsed == expected

    def test_parse_multiple_statements(self):
        test_str = 'x=1;y=2;z=3;if(true){}else{}while(false){}'
        expected = Program(StatementsSequence(
            StatementAssignment(Id('x'), ArithExpInt(Int(1), None)),
            StatementsSequence(
                StatementAssignment(Id('y'), ArithExpInt(Int(2), None)),
                StatementsSequence(
                    StatementAssignment(Id('z'), ArithExpInt(Int(3), None)),
                    StatementsSequence(
                        StatementIf(
                            BoolExpBool(Bool(True), None),
                            Block(None),
                            Block(None)),
                        StatementsSequence(
                            StatementWhile(
                                BoolExpBool(Bool(False), None),
                                Block(None)),
                            None))))))
        parsed = Parser(test_str).parse()
        assert parsed == expected
