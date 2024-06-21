import re

def valid_var_user(variables=()):
    contador = 0
    for i in variables:
        if i == None or len(i) == 0:
            contador = contador +1
    if len(variables) == contador:
        return "ALL_NONE"
    elif contador == 0:
        return "NICE"
    else:
        return "NOT_ALL_NONE"
    
def validar_contraseña(contraseña):
    # Verificar que tenga al menos 8 caracteres
    if len(contraseña) < 8:
        return False
    
    # Verificar que tenga al menos una letra mayúscula
    if not re.search(r"[A-Z]", contraseña):
        return False
    
    # Verificar que tenga al menos un caracter especial
    if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", contraseña):
        return False
    
    if not re.search(r'\d', contraseña):
        return False
    
    return True