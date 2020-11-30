import datatype


def parseNumDimsAndExplicitMem(node):
    # Look for a class(var) or string type literal (e.g 'uint32'). Extract if
    # present. Return the number of leading nodes that comprise the dimensions
    mem = None
    numDimArgs = 0
    for cn in node:
        if (cn.backend == 'reserved') and (cn.name == 'class'): # class(var)
            mem = cn[0].mem
        elif cn.cls == "String": # 'uint32'
            mem = datatype.matlabTypes_mem.get(cn.value, None)
        else:
            numDimArgs += 1

    return numDimArgs, mem

def getDimFromNumDimArgs(node, numArgs, dimIdxStart = 0):
    if numArgs == 1:
        return 3
    elif numArgs == 2:
        if node[dimIdxStart].cls == "Int" and node[0].value == "1":
            return 2 # rowvec
        elif node[1].cls == "Int" and node[dimIdxStart+1].value == "1":
            return 1 # colvec
        else:
            return 3
    elif numArgs == 3:
        return 4 # cube
    
def getConstInt(node):
    constInt = None
    if node.cls == "Int":
        constInt = int(node.value)
    elif (node.cls == "Neg") and (node[0].cls == "Int"):
        constInt = -int(node[0].value)
    return constInt
    
def renderDimNodeArgs(numDimArgs, dimIdxStart = 0):
    if numDimArgs == 1:
        idxList = [ dimIdxStart, dimIdxStart ]
    else:
        idxList = range(dimIdxStart, dimIdxStart+numDimArgs)
        
    args = ["%("+str(i)+")s" for i in idxList]
    args = ", ".join(args)
    return args


def isBeingCastedToMemType(node):
    # Get mem type from parent if it is a cast
    if node.parent.backend == 'reserved':
        return datatype.matlabTypes_mem.get(node.parent.name, None)
    
def deduceTemplateType(node):
    # try to figure out the type for the template by examining the other args
    for carg_node in node.parent.children:
        if carg_node is node: # skip ourselves
            continue
        
        return carg_node.type
    return 'TYPE' # unknown

