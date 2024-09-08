from grammar import *
from parser import Parser
from typing import Dict

class Interpreter:
    def __init__(self, program: str):
        self.env: Dict[str, int] = {}
        self.program: str = program
        self.parsed_program: Program | None = None
    
    def run(self, print_results=True):
        """
        Run a complete program, including all necessary setup and teardown
        """
        # Reset environment
        self.env = {}
        if self.parsed_program is None:
            self.parsed_program = Parser(self.program).parse()
        
        # Run the code and print the results
        self._run_program(self.parsed_program)

        if print_results:
            print("Program complete. Printing environment...")
            for var, val in self.env.items():
                print("  {} = {}".format(var, val))

    def _eval_arith_exp(self, exp: ArithExp) -> int:
        """
        Evaluate an arithmetic expression
        """
        match exp:
            case ArithExpInt(val, remain):
                return self._eval_arith_exp_(val.value, remain)

            case ArithExpId(var, remain):
                # Make sure the variable has already been defined and look up its value
                if var.value not in self.env:
                    raise ValueError('Encountered unknown variable: {}'.format(var.value))
                val = self.env[var.value]
                return self._eval_arith_exp_(val, remain)

            case _:
                assert False

    def _eval_arith_exp_(self, val: int, remain: ArithExp_) -> int:
        """
        Evaluate the remainder of an arithmetic expression
        """
        match remain:
            case None:
                return val

            case ArithExp_Sum(exp, remain):
                val2 = self._eval_arith_exp(exp)
                result = val + val2
                return self._eval_arith_exp_(result, remain)

            case ArithExp_Div(exp, remain):
                val2 = self._eval_arith_exp(exp)
                result = int(val / val2)
                return self._eval_arith_exp_(result, remain)

            case _:
                assert False

    def _eval_bool_exp(self, exp: BoolExp) -> bool:
        """
        Evaluate a boolean expression
        """
        match exp:
            case BoolExpBool(val, remain):
                return self._eval_bool_exp_(val.value, remain)

            case BoolExpLEQ(lhs, rhs, remain):
                lhs = self._eval_arith_exp(lhs)
                rhs = self._eval_arith_exp(rhs)
                val = lhs <= rhs
                return self._eval_bool_exp_(val, remain)

            case BoolExpNegation(exp, remain):
                val = not self._eval_bool_exp(exp)
                return self._eval_bool_exp_(val, remain)

            case _:
                assert False

    def _eval_bool_exp_(self, val: bool, remain: BoolExp_) -> bool:
        """
        Evaluate the remainder of a boolean expression
        """
        match remain:
            case None:
                return val

            case BoolExp_And(exp, remain):
                result = val and self._eval_bool_exp(exp)
                return self._eval_bool_exp_(result, remain)

            case _:
                assert False

    def _run_statement(self, stmt: Statement):
        """
        Execute a single statement
        """
        match stmt:
            case StatementAssignment(ident, exp):
                self.env[ident.value] = self._eval_arith_exp(exp)

            case StatementIf(cond, if_body, else_body):
                if (self._eval_bool_exp(cond)):
                    self._run_block(if_body)
                else:
                    self._run_block(else_body)

            case StatementWhile(cond, body):
                while(self._eval_bool_exp(cond)):
                    self._run_block(body)

            case _:
                assert False

    def _run_statements(self, stmts: Statements):
        """
        Execute a (potentially empty) series of statements
        """
        match stmts:
            case None:
                pass

            case StatementsSequence(stmt, remain):
                self._run_statement(stmt)
                self._run_statements(remain)

            case _:
                assert False

    def _run_block(self, block: Block):
        """
        Execute a block of statements
        """
        self._run_statements(block.stmts)

    def _run_program(self, prog: Program):
        """
        Execute a full program
        """
        self._run_statements(prog.stmts)

if __name__ == '__main__':
    test_data = '''
    i = 7;
    _foo87_ = 9;
    while (i <= 10) {
        i = i + 1;
    }
    if (i <= _foo87_) {
        i = 0;
    } else {
    }
    '''

    interpreter = Interpreter(test_data)
    interpreter.run()