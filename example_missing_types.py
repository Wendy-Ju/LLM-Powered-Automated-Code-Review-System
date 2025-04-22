def connect(server, port):
    return server + ":" + str(port)

def calculate(a, b, op):
    if op == "add":
        return a + b
    elif op == "mul":
        return a * b
    else:
        return None
