import assign  #from assign import Assign
from .variables import *
import matlab2cpp

Declare = "struct %(name)s"

def Counter(node):
    return "%(name)s = %(value)s"

#def Fvar(node): #defined in variables.py
#    return "%(name)s.%(value)s"
    
# NOTE: The default implementation of Fget in variables.py doesn't produce
# correct code e.g:
# m:   prmStr.Pilots(:,1:numSym,1:numTx);
# cpp: prmStr.Pilots(m2cpp::span<uvec>(0, prmStr.n_rows-1)) ;
#                                               | -> prmStr.Pilots
# TO BE FIXED?

# NF_DEBUG: Take the default (in variables.py) for now
#def Fget(node):
#    # NF_DEBUG: original code was returning None -> BANG!
#    return "%(name)s.%(value)s(", ", ", ")"
#    pass

def Fset(node):
    return "%(name)s.%(value)s[", ", ", "-1]"

def Matrix(node):
    if node.backend == "structs":
        if node[0].cls == "Vector":
            if len(node[0]) == 1:
                return "%(0)s"
    return "[", ", ", "]"

def Assign(node):
    return assign.Assign(node) # Default

    lhs, rhs = node
    print('here')
    # assign a my_var = [a.val], a is a structs, my_var should be a vec
    if node[1].cls == "Matrix" and node[1].backend == "structs":
        element = rhs[0][0]
        if element.backend == "structs":
            size = rhs.str
            var = lhs.name
            name = element.name
            value = element.value

            declares = node.func[0]
            if "_i" not in declares:
                declare = matlab2cpp.collection.Var(declares, "_i")
                declare.type = "sword"
                declare.backend = "sword"
                declares.translate()
            
            string = var + ".resize(" + size + ") ;\n" +\
                "for (_i=0; _i<" + size + "; ++_i)\n  "+\
                var + "[_i] = " + name + "[_i]." + value + " ;"

            return string

    return "%(0)s = %(1)s"

