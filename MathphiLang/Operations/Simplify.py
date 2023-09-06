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
from sympy import sympify

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
    
    def _sort_args_mul(self,args):
        pass

    def _sort_args(self,args):
        first_arg,second_arg  = None, None
        args_stack = []
        for arg in args:
            args_stack.append(arg)  
        args_stack.reverse()
        for i in args_stack:
            first_arg = args_stack.pop()
            # return similar types if exits 
            for (arg2, index) in zip(args_stack,range(len(args_stack))):
                if self.classify_expr(first_arg) == self.classify_expr(arg2):
                    second_arg = arg2
                    del args_stack[index]
                    return first_arg, second_arg, args_stack
            # code for different types exiting in the stack
            if self.classify_expr(first_arg) in ('number','fraction'):
                for (arg2,index) in zip(args_stack,range(len(args_stack))):
                    if self.classify_expr(arg2) in ('number','fraction'):
                        second_arg = arg2
                        del args_stack[index]
                        return first_arg, second_arg, args_stack
            first_arg = args_stack.insert(0,first_arg)
        
        # otherwise return the first two args
        first_arg = args_stack.pop()
        second_arg = args_stack.pop()
        return first_arg, second_arg , args_stack

    def compute_Add(self,node):
        # addition and subtraction manipulation go here 
        # involving numbers , roots , fraction , ..., and so on.
        # also, define a pattern starting with add node to be discovered here
       
        if self._has_ready_args(node):

            first_arg, second_arg, args_stack = self._sort_args(node.args)
            
            if self._is_number(first_arg) and self._is_number(second_arg) and not self._op_done:
                return self._num_num_add(first_arg, second_arg, args_stack)
            
            elif  self._is_fraction(first_arg) and self._is_fraction(second_arg) and not self._op_done:
                return self._frac_frac_add(first_arg,second_arg,args_stack)
            
            elif  self._is_fraction(first_arg) and self._is_number(second_arg) and not self._op_done:
                return self._num_frac_add(second_arg,first_arg,args_stack)
            
            elif  self._is_fraction(second_arg) and self._is_number(first_arg) and not self._op_done:
                return self._num_frac_add(first_arg,second_arg,args_stack)
            
            else:
                if(len(args_stack) > 0):
                    return Add(self.compute(first_arg),self.compute(second_arg),*args_stack,evaluate=False)
                return Add(self.compute(first_arg), self.compute(second_arg), evaluate=False)
        else:
            if(len(node.args) > 2):
                return Add(self.compute(node.args[0]),self.compute(node.args[1]),*[self.compute(arg) for arg in node.args[2:]],evaluate=False)
            return Add(self.compute(node.args[0]), self.compute(node.args[1]), evaluate=False)
        
    
    def compute_Mul(self,node):
        # multiplication manipulation go here 
        # involving numbers , roots , fraction , ..., and so on.
        # also, define a pattern starting with mul node to be discovered here
        if self._has_ready_args(node):

            first_arg, second_arg, args_stack = self._sort_args(node.args)
            
            if self._is_number(first_arg) and self._is_number(second_arg) and not self._op_done:
                return self._num_num_mul(first_arg, second_arg, args_stack)
            
            elif  self._is_fraction(first_arg) and self._is_fraction(second_arg) and not self._op_done:
                return self._frac_frac_mul(first_arg,second_arg,args_stack)
            
            elif  self._is_fraction(first_arg) and self._is_number(second_arg) and not self._op_done:
                return self._num_frac_mul(second_arg,first_arg,args_stack)
                
            elif  self._is_fraction(second_arg) and self._is_number(first_arg) and not self._op_done:
                return self._num_frac_mul(first_arg,second_arg,args_stack)
            
            else:
                if(len(args_stack) > 0):
                    return Mul(self.compute(first_arg),self.compute(second_arg),*args_stack,evaluate=False)
                return Mul(self.compute(first_arg), self.compute(second_arg), evaluate=False)
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

    def _num_num_mul(self, first_arg, second_arg,args_stack):
        self._op_done = True
        num1,num2 = first_arg,second_arg
        if num1.is_positive and num2.is_positive:
            self._descriptions.append('')
        elif num1.is_positive and num2.is_negative:
            if num1 == -1*num2:
                self._descriptions.append('')
            else:
                self._descriptions.append('')
        elif num1.is_negative and num2.is_positive:
            if num1 == -1* num2:
                self._descriptions.append('')
            else:
                self._descriptions.append('')
        elif num1.is_negative and num2.is_negative:
                self._descriptions.append('')
        elif num1.is_zero and num2.is_positive:
                self._descriptions.append('')
        elif num1.is_zero and num2.is_negative:
                self._descriptions.append('')
        elif num1.is_positive and num2.is_zero:
                self._descriptions.append('')
        elif num1.is_negative and num2.is_zero:
                self._descriptions.append('')
        elif num1.is_zero and num2.is_zero:
                self._descriptions.append('')
        # with multiple args
        if(len(args_stack) > 0):
            result = Mul(self.compute(first_arg)*self.compute(second_arg),*args_stack,evaluate=False)
            return result
        # with two args
        return self.compute(first_arg)*self.compute(second_arg)


    def _num_frac_mul(self,num, frac, args_stack):
        self._op_done = True
        frac_tuple = frac.as_numer_denom()
        # with multiple args
        numer = Mul(num,frac_tuple[0],evaluate=False)
        denom = frac_tuple[1]
        frac_new = None
        if frac_tuple[0]==1:
            numer = simplify(numer)
            frac_new = Rational(numer,denom,gcd=1)
        else:
            frac_new = self._generate_fraction(numer,denom,evaluate=False)

        if(len(args_stack) > 0):
            result = Mul(frac_new,*args_stack,evaluate=False)
            return result
        # with two args
        return frac_new

    def _frac_frac_mul(self,first_arg, second_arg, args_stack):
        self._op_done = True
        frac1 = first_arg.as_numer_denom()
        frac2 = second_arg.as_numer_denom()
        # with multiple args
        self._descriptions.append('')
        numer = Mul(frac1[0],frac2[0],evaluate=False)
        denom = Mul(frac1[1],frac2[1],evaluate=False)
        frac = self._generate_fraction(numer,denom,evaluate=False)
        if(len(args_stack) > 0):
            result = Mul(frac,*args_stack,evaluate=False)
            return result
        # with two args
        return frac

    def _root_root_mul(self):
        pass

    def _root_root_add(self):
        pass

    def _power_power_add(self):
        pass

    def _power_number_add(self):
        pass

    def _power_numer_mul(self):
        pass

    def _num_frac_add(self,num, frac, args_stack):
        self._op_done = True
        frac1 = frac
        frac2 = self._generate_fraction(num,1,evaluate=False)
        # with multiple args
        self._descriptions.append('frac')
        if(len(args_stack) > 0):
            result = Add(frac1,frac2,*args_stack,evaluate=False)
            return result
        # with two args
        return Add(frac1,frac2,evaluate=False)

    def _frac_frac_add(self,first_arg, second_arg, args_stack):
        frac1 = first_arg.as_numer_denom()
        frac2 = second_arg.as_numer_denom()
        if frac1[1] == frac2[1]:
            self._op_done = True
            # with multiple args
            self._descriptions.append('frac')
            numer = Add(frac1[0],frac2[0],evaluate=False)
            denom = frac1[1]
            frac = self._generate_fraction(numer,denom,evaluate=False)
            if(len(args_stack) > 0):
                result = Add(frac,*args_stack,evaluate=False)
                return result
            # with two args
            return frac
        else:
            self._op_done  = True
            common_denom = Mul(frac1[1],frac2[1],evaluate=False)
            numer_1 = Mul(frac1[0],frac2[1],evaluate=False)
            numer_2 =  Mul(frac2[0],frac1[1],evaluate=False)
            frac1_new = self._generate_fraction(numer_1,common_denom,evaluate=False)
            frac2_new = self._generate_fraction(numer_2,common_denom,evaluate=False)
            self._descriptions.append('')
            if(len(args_stack) > 0):
                result = Add(frac1_new,frac2_new,*args_stack,evaluate=False)
                return result
            # with two args
            return Add(frac1_new,frac2_new,evaluate=False)


    def _num_num_add(self,first_arg, second_arg, args_stack):
        self._op_done = True
        num1,num2 = first_arg,second_arg
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
        # with multiple args
        if(len(args_stack) > 0):
            result = Add(self.compute(first_arg)+self.compute(second_arg),*args_stack,evaluate=False)
            return result
        # with two args
        return self.compute(first_arg)+self.compute(second_arg)


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
                if node.q != 1:
                    return True
        return False
    def _is_number(self,node):
        if isinstance(node,Number):
            if isinstance(node,Rational):
                if node.q ==1:
                    return True   
        return False
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
    def classify_expr(self,node):
        if self._is_number(node):
            return 'number'
        elif self._is_fraction(node):
            return 'fraction'
        elif self._is_power(node):
            return 'power'
        elif self._is_root(node):
            return 'root'
        else:
            return type(node)
        
    # functions for generating a certain expr
    def _generate_fraction(self,num,denom, evaluate =False ):  
        if self._is_number(num) and self._is_number(denom):
            return Rational(num,denom,gcd=1)
        else:   
            return Mul(num,Pow(denom,-1,evaluate=evaluate),evaluate=evaluate)

    def _generate_root(self,number, rank ,evaluate = False):
        if isinstance(number,Number):
            return sympify(f'{number}^(1/{rank})',evaluate=evaluate)
        return Pow(number,Rational(1,rank),evaluate=evaluate)

    def _generate_power(self, base, exponent, evaluate = False):
        if isinstance(base,Number) and isinstance(exponent,Number):
            return sympify(f'{base}^{exponent}',evaluate=evaluate)
        return Pow(base,exponent,evaluate=evaluate)
    
    def _generate_subtraction(self,num1,num2,evaluate= False):
        return sympify(f'{num1}-{num2}',evaluate=evaluate)
    
    def _has_ready_args(self,node):
        if node.args is not None:
            for arg in node.args:
                if self._is_number(arg):
                    continue
                elif self._is_fraction(arg):
                    continue
                elif self._is_power(arg):
                    continue
                elif self._is_root(arg):
                    continue
                else:
                    return False
            return True
        return False