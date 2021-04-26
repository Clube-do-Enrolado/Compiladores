def afd_numeric(lexem):
    """Função que avalia se um lexema é numérico.
    
    Dado um lexema, testa através de um DFA (ou AFD),
    se esse lexema é do tipo numérico (INT ou FLOAT),
    seguindo a regex:
    INT:   {[ 0-9 ]+} 
    FLOAT: {[ 0-9 ]+.[ 0-9 ]+}

    Parameters:
    -----------
    lexem (string): O lexema a ser analisado pelo AFD.

    Return:
    (boolean, string): Retorna uma tupla informando se
    o lexema foi reconhecido e qual o tipo do lexema.
    """

    transition_table = {
           0: {'0':1, '1':1, '2':1, '3':1, '4':1, '5':1, '6':1, '7':1, '8':1, '9':1},
           1: {'0':1, '1':1, '2':1, '3':1, '4':1, '5':1, '6':1, '7':1, '8':1, '9':1, '.':2},
           2: {'0':3, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3},
           3: {'0':3, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3}}

    ESTADOS_FINAIS = [1,3] # Estados finais possíveis.
    current_state = 0
    
    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é numérico.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]

    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        # Tratamento dos retornos
        if current_state == 1:
            return (True,"INTEGER")
        else:
            return (True,"FLOAT")

def afd_string(lexem):
    """Função que verifica se o lexema é uma string

    Função que utiliza um AFD (ou DFA) para avaliar a corretude
    da sintaxe de um lexema concorrente à string, seguindo a
    regex: {"([ \s-! ]*[ #-$ ]*[ &-\[ ]*[ \]-~ ]*)*"}.

    Parameter:
    ----------
    lexem (string): O lexema a ser analisado pelo AFD.

    Return:
    (boolean, string): Retorna uma tupla informando se
    o lexema foi reconhecido e qual o tipo do lexema.

    """

    transition_table = {
            0: {'"': 1},
            1: {'"': 2},
            2: {}
            }

    # Adições de caracteres ASCII na tabela
    # de transição.
    transition_table[1][chr(32)] = 1 # \s
    transition_table[1][chr(33)] = 1 # !
    transition_table[1][chr(35)] = 1 # #
    transition_table[1][chr(36)] = 1 # $
    
    for i in range(38, 92):          # & até [
        transition_table[1][chr(i)] = 1

    for i in range(93, 127):         # ] até ~
        transition_table[1][chr(i)] = 1
    
    current_state = 0
    ESTADOS_FINAIS = [2] # Estados finais possíveis

    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,"STRING")
    else:
        return (False,None)

def afd_identifier(lexem):
    """Função que verifica se o lexema é uma variável

    Função que utiliza um AFD (ou DFA) para avaliar a corretude
    da sintaxe de um lexema concorrente à variavel, seguindo
    a regex: {([ _-_ ]*[ A-Z ]*[ a-z ]+ | [ _-_ ]*[ A-Z ]+[ a-z ]* | [ _-_ ]+[ A-Z ]*[ a-z ]*)([ 0-9 ]*)}.

    Parameter:
    ----------
    lexem (string): O lexema a ser analisado pelo AFD.

    Return:
    (boolean, string): Retorna uma tupla informando se
    o lexema foi reconhecido e qual o tipo do lexema.

    """
    
    transition_table = {
            0: {chr(y):1 for y in range(97,123)},
            1: {chr(y):1 for y in range(97,123)}}

    transition_table[0]['_'] = 1
    transition_table[1]['_'] = 1    

    for i in range(10):
        transition_table[1][str(i)] = 1

    current_state = 0
    ESTADOS_FINAIS = [1,2]
    
    for char in lexem.lower():
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,"IDENTIFIER")
    else:
        return (False,None)

def afd_keywords(lexem):
    """Função que verifica se o lexema é uma palavra reservada

    Função que utiliza um AFD (ou DFA) para avaliar a corretude
    da sintaxe de um lexema concorrente à palavra reservada
    (keyword).

    Parameter:
    ----------
    lexem (string): O lexema a ser analisado pelo AFD.

    Return:
    (boolean, string): Retorna uma tupla informando se
    o lexema foi reconhecido e qual o tipo do lexema.

    """
    # Palavras reservadas (keywords) definidas pelo grupo:
    # ["if","else","elif","def","for","while","return","break","print","input","in","and","or","not","range"]
    transition_table = {
            1:  {'a':15, 'b':16, 'd':17, 'e':18, 'f':19, 'i':20, 'n':21, 'o':22, 'p':23, 'r':24, 'w': 25},
            
            19: {'o':22},
            20: {'f':3 , 'n':29},
            23: {'r':30},
            24: {'a':31 , 'e':32},
            25: {'h':33},
 
            16: {'r':27},
            18: {'l':28},
            22: {'r':3},
            29: {'p':6},
            30: {'i':7},
            31: {'n':8},
            32: {'t':9},
            33: {'i':10},

            27: {'e':2 },
            17: {'e':4},
            28: {'i':4 , 's':5 },
            6:  {'u':12},
            21: {'o':12},
            7:  {'n':12},
            8:  {'g':5},
            9:  {'u':13},
            10: {'l':5},


            15: {'n':26},
            2:  {'a':11},
            4:  {'f':3 },
            12: {'t':3},
            5:  {'e':3},
            13: {'r':14},

            26: {'d':3},
            11: {'k':3},
            14: {'n':3},           
            }

    current_state = 1
    ESTADOS_FINAIS = [3,29] # Estados finais possíveis

    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,lexem.upper())
    else:
        return (False,None)

def afd_operator(lexem):
    
    # special = ["+","-","*","/","=","==","!=","+=","-=","*=","/=","<",">","<=",">="]

    transition_table = {
            0: {'!':2, '+':1, '-':1, '*':1, '/':1, '=':1, '<':1, '>':1 },
            1: {'=': 3},
            2: {'=': 3},
            3: {}
            }

    current_state = 0
    ESTADOS_FINAIS = [1,3] # Estados finais possíveis


    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,lexem)
    else:
        return (False,None)

def afd_delimiters(lexem):
    # delimiters = [",",":","(",")","\n","\t"]

    transition_table = {
            0: {',': 1,':': 1, '(':1, ')':1, '\n':1, '\t':1},
            1: {}
            }

    current_state = 0
    ESTADOS_FINAIS = [1]

    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,lexem)
    else:
        return (False,None)

def afd_boolean(lexem):
    transition_table = {
            0: {'T': 1, 'F': 5},
            1: {'r': 2},
            2: {'u': 3},
            3: {'e': 4},
            4: {},
            5: {'a': 6},
            6: {'l': 7},
            7: {'s': 8},
            8: {'e': 4}
            }

    current_state = 0
    ESTADOS_FINAIS = [4]

    for char in lexem:
        # Se o caractere lido não for válido entre as opções dadas
        if char not in transition_table[current_state].keys():
            # O lexema não é válido.
            return (False,None)

        else: # Muda de estado.
            current_state = transition_table[current_state][char]
    
    # Está no estado final e não existem mais caracteres para leitura.
    if current_state in ESTADOS_FINAIS:
        return (True,lexem.upper())
    else:
        return (False,None)
