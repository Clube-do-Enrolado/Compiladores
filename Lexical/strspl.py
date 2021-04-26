"""
    GRUPO:
                 NOMES                           R.A      
    | - Andy Silva Barbosa                | 22.218.025-9 |
    | - Rafael Zacarias Palierini         | 22.218.030-9 |
    | - Rubens de Araujo Rodrigues Mendes | 22.218.009-3 |
    | - Vitor Acosta da Rosa              | 22.218.006-9 |


    Última modificação: 14/04/2021

    Função que separa toda a string dada de forma que
    o analisador léxico consiga interpretá-lo.
"""

# Lista de caracteres especiais que devem ser reconhecidos como lexemas e servem assim como o espaço
# em branco como delimitadores.
special = [",","+","-","*","/","=","==","!=","+=","-=","*=","/=","<",">","<=",">=",":","(",")","\n","\t"]
WHITE_SPACE = " "


def strspl(s):
   lexeme = ""  # Lexema reconhecido até o momento
   strings = [] # Lista de lexemas (ainda para implementar)
   hist = False # Controle de histórico (caso o char imediatamente anterior
                # já tenha sido considerado no lexema)


   for i, char in enumerate(s): # Para cada caractere da string (contando também seu index)
        if char != WHITE_SPACE: # O caractere atual não é um espaço em branco
            lexeme += char # Adiciona o char atual ao lexema reconhecido até o momento

        if char in special: # Caso o char atual seja um operador

            if hist: # Caso esse char atual já tenha sido utilizado em um lexema imediatamente anterior
                lexeme = ""
                hist = False # O histórico não será mais usado na próxima iteração
                continue
            
            # Se o próximo caractere, concatenado ao caractere atual seja
            # também um operador (e.g. ==, <=, += etc.)
            if (i+1) < len(s) and (char+(s[i+1])) in special:

                strings.append(char+s[i+1]) # Salva o lexema encontrado na lista
                lexeme="" 
                hist = True # Indica que o caractere atual está utilizando um vizinho
                            # prevenindo considerar <= e depois = separadamente, por exemplo
                continue
            
            
            strings.append(lexeme) # Salva o lexema encontrado
            lexeme=""
            continue

        if (i+1) < len(s):
            # Caso o próximo caractere seja um espaço, ou o próximo caractere
            # seja um caractere de operação
            if s[i+1] == WHITE_SPACE or s[i+1] in special:
                if char != WHITE_SPACE: # O caractere atual não pode ser um espaço vazio
                    strings.append(lexeme)
                    lexeme=""

   return strings
