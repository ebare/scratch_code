# H2O 
# Mg(OH)2
# K4[ON(SO3)2]2


def parse_molecule (formula):
    out = {}
    
    stack = []
    cur_element = None
    for char in formula:
        if char in '{([':
            stack.append(char)
        if char.isupper():
            stack.append(char)
        if char.islower():
            stack[-1] = stack[-1] + char
        if char.isdigit():
            if stack[-1] in ')}]':
                pass
            else:
                stack.append(char)

    return out