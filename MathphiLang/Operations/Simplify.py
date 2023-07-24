#TODO 
# chenge line 107








from .Operation import Operation
from ..Core.TokenType import TokenType
from ..MathLiterals.MathLiteral import MathLiteral
from ..Solver.Solution import Solution
from sympy.core.expr import Expr as Expression
from sympy.core.add import Add
from sympy.core.symbol import Symbol
from sympy.core.mul import Mul
from sympy.core.numbers import NegativeOne,Number
from sympy.core.power import Pow
from sympy.core.numbers import Float
from sympy.core.numbers import Integer
from sympy import preorder_traversal
from sympy import simplify
from sympy import latex


class Simplify(Operation):
    def __init__(self,children: list, solution: Solution):
        super().__init__(op =TokenType.SIMPLIFY, children = children)
        # assume that the expr is correctly written in latex form and successfully parsed
        self.expr = children[0]
        self.solution = solution
    # main method that causes the operation starting to manipulate the given expr
    def execute(self):
        pass
    def expr_from_nodes(self,stack):
        s = stack.copy()
        insertion_index = 0
        while len(s)>1:
             right = s.pop()
             left = s.pop()
             op = s.pop()
             if isinstance(op,Pow):
                 result = Pow(left , right, evaluate=False)
                 s.append(result)
                 continue
             if isinstance(op,Mul):
                 result = Mul(left , right, evaluate= False)
                 s.append(result)
                 continue
             if isinstance(op,Add):
                 result = Add(left , right ,evaluate= False)
                 s.append(result)
                 
                 continue
             if op.is_number:
                insertion_index += 1
                s.insert(insertion_index,right)
                insertion_index +=2
                s.insert(insertion_index,left)
                s.append(op)
                continue
        return s[0]     
        
    # simplify parts of expr like ' 2+3-5*4 + 2**3'
    def simplify_basic_ops(self):
        expr = self.expr.parsed_latex
        steps = list(tuple())
        stack = []
        for arg in preorder_traversal(expr):
            stack.append(arg)
        is_division = False
        insertion_index = 0
        while len(stack) > 1 :
            right = stack.pop()
            left = stack.pop()
            op = stack.pop()
            
            if isinstance(op,Pow):
                base = left
                exponent = right
                # terminate the loop if the power's args doesn't represent numbers
                if not (exponent.is_number and base.is_number):
                    continue
                
                # division case : exponent equals negative one
                if isinstance(exponent,NegativeOne):
                    is_division  =True
                    stack.append(op)
                else:
                    is_division = False
                    result = base ** exponent
                    result = simplify(result)
                    stack.append(result)
                    stepResult = latex(self.expr_from_nodes(stack))
                    steps.append((stepResult,'stepDescription: exponentiation is performed'))
                continue

            if isinstance(op,Mul):
                
                # check if we came from power that represents division
                if is_division:
                    result = left * right
                    result = simplify(result)
                    stack.append(result)
                    stepResult = latex(self.expr_from_nodes(stack))
                    steps.append((stepResult,'stepDescription: division is performed'))
                    is_division = False
                else:

                    if not (right.is_number and left.is_number):
                        continue
                    #check if mul represents the negative sign if yes : don't describe the step
                    if isinstance(left,NegativeOne) or isinstance(right,NegativeOne):
                        is_subtraction = True
                        stack.append(op)
                    else:
                        
                        result = left * right
                        result = simplify(result)
                        stack.append(result)
                        stepResult = latex(self.expr_from_nodes(stack))
                        steps.append((stepResult,'stepDescription: multiplication is performed'))
                        

                continue
            if isinstance(op,Add):
                result = left + right
                result = simplify(result)
                stack.append(result)
                stepResult = latex(self.expr_from_nodes(stack))
                if (left * right).is_negative:
                    steps.append((stepResult,'stepDescription: subtraction is performed'))
                elif (left * right ).is_positive:
                    steps.append((stepResult,'stepDescription: addition is performed'))
                else:
                    steps.append((stepResult,"stepDescription: zero doesn't change anything "))

                continue
            if op.is_number:
                insertion_index +=1
                stack.insert(insertion_index,right)
                insertion_index +=2
                stack.insert(insertion_index,left)
                stack.append(op)
                continue
        return steps

    

    