tokens_dict = {
        "keyword":  ["if","else","elif","def","for","while","return","break","print","input"],
        "operator": ["+","-","*","/","=","==","!=","+=","-=","*=","/="],
        "boolean":  ["True","False"],
        ":" :       [":"],
        "(" :       ["("],
        ")" :       [")"],
        "\\n":      ["\\n"],
        "\\t":      ["\\t"]
        }


def is_integer(s):
    """
    is_integer
    -----------
    Função que verifica se uma dada string é uma variável
    que obedece a regex: [0-9]^+

    Parameters:
    s (string): String a ser analisada.

    Return:
    True: Caso a string obedeça a regex.
    False: Caso a string não obedeça a regex.

    """
    if s.isdigit(): 
        return True  
    return False

def is_float(s):
    """

    is_float
    -----------
    Função que verifica se uma dada string é uma variável
    que obedece a regex: [0-9]^+.[0-9]^+

    Parameters:
    s (string): String a ser analisada.

    Return:
    True: Caso a string obedeça a regex.
    False: Caso a string não obedeça a regex.

    """
    try:
        flt = s.split(".")
        if flt[0].isdigit() and flt[1].isdigit() and len(flt) == 2:
            return True
     
        return False
    except:
        return False

def is_string(s):
    """

    is_string
    -----------
    Função que verifica se uma dada string é uma variável
    que obedece a regex: "[\s-!]*[#-$]*[&-[]*[]-~]*"

    Parameters:
    s (string): String a ser analisada.

    Return:
    True: Caso a string obedeça a regex.
    False: Caso a string não obedeça a regex.

    """
    if s[0] == '"' and s[-1] == '"':
        return True
    return False

def is_variable(s):
    """

    is_variable
    -----------
    Função que verifica se uma dada string é uma variável
    que obedece a regex: [_-_]*[A-Z]*[a-z]+|[_-_]*[A-Z]+[a-z]*|[_-_]+[A-Z]*[a-z]*[0-9]*

    Parameters:
    s (string): String a ser analisada.

    Return:
    True: Caso a string obedeça a regex.
    False: Caso a string não obedeça a regex.

    """
    if s[0] == "_" or (s[0] >= 'A' and s[0] <= 'Z') or (s[0] >= 'a' and s[0] <= 'z'):
        special = []
        for c in s:
            if c.isalnum() == False:
                special.append(c)
        if len(special) > 1 or (len(special) > 0 and special[0] != "_"):
            return False
        return True
    return False
