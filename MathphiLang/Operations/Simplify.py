from .Operation import Operation
from ..Core.TokenType import TokenType
from ..Core.DataSet import Explainer
from ..Solver.MathSequence import MathSequence
from ..MathLiterals.MathLiteral import MathLiteral
from ..Solver.Solution import Solution
from ..MathLiterals.Expr import Expr
from ..Core.NodeVisitor import NodeVisitor
from sympy.core.expr import Expr as Expression
from sympy.core.add import Add
from sympy.core.symbol import Symbol
from sympy.core.mul import Mul
from sympy.core.numbers import NegativeOne,Number,One
from sympy.core.power import Pow
from sympy.core.numbers import Float
from sympy.core.numbers import Integer
from sympy import preorder_traversal
from sympy import simplify
from sympy import latex
from sympy.core.numbers import Rational

class Simplify(Operation):
    def __init__(self,children: list[Expr], solution: Solution, explainer: Explainer):
        super().__init__(op =TokenType.SIMPLIFY, children = children)
        # assume that the expr is correctly written in latex form and successfully parsed
        # assume that the explainer loaded the data outside
        self.expr = children[0]
        self.solution = solution
        self.explainer = explainer
        self._simplify_arithmetic = None
    
    # main method that causes the operation starting to manipulate the given expr
    def execute(self):
        pass
        
    @property
    def simplify_arithmetic(self)-> MathSequence:
        if self._simplify_arithmetic is None:
            self._simplify_arithmetic = SimplifyArithmetic(self.expr,self.explainer)
            return  self._simplify_arithmetic.getSolution
        else:
            return  self._simplify_arithmetic.getSolution
    
    
    

class SimplifyArithmetic(object):
    def __init__(self,expr,explainer: Explainer):
        self.expr = expr
        self.current_expr = self.expr
        self._op_done = False
        self._steps = []
        self._descriptions = []
        self._execute_calls_number = 0
        self.explainer = explainer
        self.explainer.extractArithmeticDes()
        self.mathSequence = MathSequence()
    def compute(self,node = None):
        if node is None:
            node = self.current_expr
        method_name = 'compute_' + type(node).__name__
        computer = getattr(self, method_name ,self.generic_compute)
        return computer(node)
    
    def generic_compute(self, node):
        raise Exception(f'No compute_{type(node).__name__} method')
    
    def compute_Add(self,node):
        # addition and subtraction manipulation go here 
        # involving numbers , roots , fraction , ..., and so on.
        # also, define a pattern starting with add node to be discovered here
        args_stack = []
        first_arg, second_arg = None, None
        for arg in node.args:
            args_stack.append(arg)
        while len(args_stack) >0:
            first_arg, second_arg = args_stack.pop(),args_stack.pop()
            if type(first_arg) is type(second_arg):
                break
            else:
                args_stack.append(first_arg)
                args_stack.insert(0,second_arg)

        if isinstance(first_arg,Number) and isinstance(second_arg,Number) and not self._op_done:
            self._op_done = True
            self._num_num_add(node)
            # with multiple args
            if(len(node.args) > 2):
                result = Add(self.compute(first_arg)+self.compute(second_arg),*args_stack,evaluate=False)
                return result
            # with two args
            return self.compute(first_arg)+self.compute(second_arg) 
        
        else:
            if(len(node.args) > 2):
                return Add(self.compute(node.args[0]),self.compute(node.args[1]),*[self.compute(arg) for arg in node.args[2:]],evaluate=False)
            return Add(self.compute(node.args[0]), self.compute(node.args[1]), evaluate=False)
        
    
    def compute_Mul(self,node):
        # multiplication and division manipulation go here 
        # involving numbers , roots , fraction , ..., and so on.
        # also, define a pattern starting with mul node to be discovered here
        if isinstance(node.args[0],Number) and isinstance(node.args[1],Number) and not self._op_done:
            self._op_done = True
            if(len(node.args) > 2):
                return Mul(self.compute(node.args[0])*self.compute(node.args[1]),*[self.compute(arg) for arg in node.args[2:]],evaluate=False)
            return self.compute(node.args[0])*self.compute(node.args[1]) 
        
        else:
            if(len(node.args) > 2):
                return Mul(self.compute(node.args[0]),self.compute(node.args[1]),*[self.compute(arg) for arg in node.args[2:]],evaluate=False)
            return Mul(self.compute(node.args[0]), self.compute(node.args[1]), evaluate=False)
    
    def compute_Pow(self,node):
        if isinstance(node.args[0],Number) and isinstance(node.args[1],Number)and not self._op_done:
            self._op_done = True
            return self.compute(node.args[0])**self.compute(node.args[1])
        else:
            return Pow(self.compute(node.args[0]), self.compute(node.args[1]), evaluate=False)   
    
    def compute_Integer(self,node):
        return node
    
    def compute_One(self,node):
        return node
    
    def compute_NegativeOne(self,node):
        return node
    
    def compute_Half(self,node):
        return node
    
    def compute_Float(self,node):
        return node
    
    def compute_Zero(self,node):
        return node
    
    def compute_Rational(self,node):
        return node
    
    def step(self):
        if not isinstance(self.current_expr,Number):
            self._steps.append(self.current_expr)
            self.current_expr = self.compute()
            self._op_done = False
            self._execute_calls_number += 1
            return self.current_expr
        else:
            if self._execute_calls_number == len(self._steps):
                self._steps.append(self.current_expr)
    
    @property
    def getSolution(self):

        while self.step() is not None:
            self.step()
        self.mathSequence.descriptions = self._descriptions
        self.mathSequence.steps = self._steps
        self.mathSequence.construct_sequence()
        return self.mathSequence
    @property
    def restart(self):
        self._execute_calls_number = 0
        self.current_expr = self.expr
        self._steps = []
    
    def setExpr(self,expr):
        self.expr = expr
    
    def _num_num_add(self,node):
        num1,num2 = node.args[0],node.args[1]
        if num1.is_positive and num2.is_positive:
            self._descriptions.append(self.explainer.explainArithmetic('addition','pos_pos','numbers','brief',num1,num2))
        elif num1.is_positive and num2.is_negative:
            if num1 == -1*num2:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','opposite','numbers','brief'))
            else:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','pos_neg','numbers','brief',-1*num2,num1))
        elif num1.is_negative and num2.is_positive:
            if num1 == -1* num2:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','opposite','numbers','brief'))
            else:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','pos_neg','numbers','brief',-1*num1,num2))
        elif num1.is_negative and num2.is_negative:
                self._descriptions.append(self.explainer.explainArithmetic('addition','neg_neg','numbers','brief'))
        elif num1.is_zero and num2.is_positive:
                self._descriptions.append(self.explainer.explainArithmetic('addition','zero_pos','numbers','brief'))
        elif num1.is_zero and num2.is_negative:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','zero_neg','numbers','brief'))
        elif num1.is_positive and num2.is_zero:
                self._descriptions.append(self.explainer.explainArithmetic('addition','zero_pos','numbers','brief'))
        elif num1.is_negative and num2.is_zero:
                self._descriptions.append(self.explainer.explainArithmetic('subtraction','zero_neg','numbers','brief'))
        elif num1.is_zero and num2.is_zero:
                self._descriptions.append(self.explainer.explainArithmetic('addition','zero_zero','numbers','brief'))


    # write functions that recognize certain patterns here 
    def _is_root(self,node):
        if self._is_power(node):
            if self._is_fraction(node.args[1]) :
                if isinstance(node.args[1],Rational):
                    if node.args[1].p == 1:
                         return True
                if (isinstance(node.args[1].args[0],One) or isinstance(node.args[1].args[1],One)):
                    return True
        return False
    
    def _is_fraction(self,node):
        if isinstance(node,Mul):
            if (isinstance(node.args[0],Number) and isinstance(node.args[1],Pow)):
                if isinstance(node.args[1].args[0],Number) and isinstance(node.args[1].args[1],NegativeOne):
                    return True
            elif (isinstance(node.args[1],Number) and isinstance(node.args[0],Pow)):
                if isinstance(node.args[0].args[0],Number) and isinstance(node.args[0].args[1],NegativeOne):
                    return True
        elif isinstance(node,Rational):
            if isinstance(node.p,int) and isinstance(node.q,int):
                return True
        return False
    def _is_number(self,node):
        return isinstance(node,Number)
    
    def _is_power(self,node):
        if isinstance(node,Pow) :
            if isinstance(node.args[0],Number):
                if isinstance(node.args[1],Number):
                    return True
                elif self._is_fraction(node.args[1]) :
                    return True
                elif isinstance(node.args[1],Rational):
                    if isinstance(node.args[1].p,int) and isinstance(node.args[1].q,int):
                        return True
        return False
    
    def _generate_fraction(self,num,denom):
        pass

    def _generate_root(self, rank):
        pass

    def _generate_power(self, base, exponent):
        pass
