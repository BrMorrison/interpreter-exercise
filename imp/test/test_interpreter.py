from imp.interpreter import Interpreter
import pytest

class TestBasicInterpreter:
    def test_run_empty_program(self):
        test_str = ''
        expected_env = {}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_assign_literals(self):
        test_str = 'i = 20; _qwert_ = 2;'
        expected_env = {'i': 20, '_qwert_': 2}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env
        
    def test_run_assign_id(self):
        test_str = 'i = 20; y = i;'
        expected_env = {'i': 20, 'y': 20}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_assign_math(self):
        test_str = 'i = 5 + 21 / 4;'
        expected_env = {'i': 10}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env
    
    def test_run_condition_true(self):
        test_str = 'if(true){ i = 11; } else { y = 13; }'
        expected_env = {'i': 11}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_condition_false(self):
        test_str = 'if(false){ i = 11; } else { y = 13; }'
        expected_env = {'y': 13}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_loop_false(self):
        test_str = 'while(false){ i = 17; }'
        expected_env = {}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_loop_negation(self):
        test_str = 'if(!false){ i = 17; }else{}'
        expected_env = {'i': 17}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_condition_and(self):
        test_str = '''
        if(true && true){i = 1;}else{}
        if(true && false){j = 2;}else{}
        if(false && true){k = 4;}else{}
        if(false && false){a = 8;}else{}
        '''
        expected_env = {'i': 1}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_condition_leq(self):
        test_str = '''
        if(1 <= 2){i = 1;}else{}
        if(2 <= 2){j = 2;}else{}
        if(3 <= 2){k = 4;}else{}
        '''
        expected_env = {'i': 1, 'j': 2}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env
    
    def test_run_loop(self):
        test_str = '''
        x = 4; y = 10; product = 0; i = 0;
        while( i+1 <= x ) {
            product = product + y;
            i = i + 1;
        }
        '''
        expected_env = {'x': 4, 'y': 10, 'product': 40, 'i': 4}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_nested_loop(self):
        test_str = '''
        base = 2; exponent = 10; result = 1; i = 1;
        while( i <= exponent ) {
            j = 1;
            temp_product = 0;
            while( j <= base ) {
                temp_product = result + temp_product;
                j = j+1;
            }
            result = temp_product;
            i = i+1;
        }
        '''
        expected_env = {'base': 2, 'exponent': 10, 'result': 1024, 'i': 11, 'j': 3, 'temp_product': 1024}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

@pytest.mark.skip
class TestExpandedArithmeticInterpreter:
    def test_run_assignment_subtraction(self):
        test_str = 'i = 5 - 3 - 1; j = 0 - 31;'
        expected_env = {'i': 1, 'j': -31}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

    def test_run_assignment_multiplication(self):
        test_str = 'i = 5 * 0; j = 2 * 4 * 8;'
        expected_env = {'i': 0, 'j': 64}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env

@pytest.mark.skip
class TestPemdasInterpreter:
    def test_run_assignment_pemdas(self):
        test_str = 'i = 11/2 + 21/4;'
        expected_env = {'i': 10}
        interpreter = Interpreter(test_str)
        interpreter.run()
        assert expected_env == interpreter.env


@pytest.mark.skip
class TestExpandedLogicInterpreter:
    pass