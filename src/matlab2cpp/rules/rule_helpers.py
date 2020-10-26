

def deduceTemplateType(node):
    # try to figure out the type for the template by examining the other args
    for carg_node in node.parent.children:
        if carg_node is node: # skip ourselves
            continue
        
        return carg_node.type
    return 'TYPE' # unknown
