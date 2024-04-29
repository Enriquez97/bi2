import random

def code_dashboard(ruc : str, user : str):
    code = ''
    for i in range(10):
        code += str(random.randint(0, 9))
    return ruc+code+user