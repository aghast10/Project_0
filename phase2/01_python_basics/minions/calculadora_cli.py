#
# CALCULADORA CLI CON LAS CUATRO OPERACIONES BÁSICAS.
#

def parse_expression(user_input):
    extraction = []
    tokens =[]
    for i in user_input:
        try:
            extraction.append(str(int(i)))
        except ValueError:
            try:
                tokens.append(int("".join(extraction)))
                extraction.clear()
                tokens.append(i)
            except ValueError:
                return "error"
            
    tokens.append(int("".join(extraction)))
    return tokens

def operation(tokens):
    mult_div = None
    while "*" in tokens and "/" in tokens:
        if tokens.index("*") < tokens.index("/"):
            mult_div = "*"
            operation_multdiv(tokens, mult_div)
        elif tokens.index("/") < tokens.index("*"):
            mult_div = "/"
            operation_multdiv(tokens, mult_div)
    while "*" in tokens:
            mult_div = "*"
            operation_multdiv(tokens, mult_div)
    while "/" in tokens:
            mult_div = "/"
            operation_multdiv(tokens, mult_div)

    if "errordiv0" in tokens:
        return "error, división entre 0"
    if "error" in tokens:
        return "error, formato no válido"
    
    while len(tokens) != 1 and "error" not in tokens:
        if tokens[1] == '+':
            result = tokens[0] + tokens[2]
            tokens.insert(3, result)
            del tokens[0:3]

        elif tokens[1] == '-':
            result = tokens[0] - tokens[2]
            tokens.insert(3, result)
            del tokens[0:3]
        else:
            break
    return tokens[0] if len(tokens) == 1 else "error, operador inválido"
    
def operation_multdiv(tokens, mult_div):
    if mult_div == "*":
        result = tokens[tokens.index(mult_div) - 1] * tokens[tokens.index(mult_div) + 1]
    else:
        try:
            result = tokens[tokens.index(mult_div) - 1] / tokens[tokens.index(mult_div) + 1]
        except ZeroDivisionError:
            result = "errordiv0"

    tokens.insert(tokens.index(mult_div) + 2, result)
    tokens.pop(tokens.index(mult_div) - 1)
    tokens.pop(tokens.index(mult_div) + 1)
    tokens.pop(tokens.index(mult_div))

def main():
    user_input = input()
    while user_input != "":
        print (operation(parse_expression(user_input)))
        user_input = input()

main()