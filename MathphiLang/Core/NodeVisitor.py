from .Node import Node

class NodeVisitor(object):
   
    def visit(self, node: Node):
        # this method is responsible for calling the appropriate visit for the above node in the args of that method

        #get the method name that manipulate the given node in the args
        method_name = 'visit_' + type(node).__name__
        # assign that method that manipulate the above node to the visitor 
        # so that the visitor var represents an interface for all visit_ methods
        # visitor has the arg : method name that will call
        # visitor has the arg : self.generic_visit so that it can call that method if there is no method is matched the method name
        visitor = getattr(self, method_name ,self.generic_visit())
        return visitor(node)
    def generic_visit(self, node: Node):
        raise Exception(f'No visit_{type(node).__name__} method')