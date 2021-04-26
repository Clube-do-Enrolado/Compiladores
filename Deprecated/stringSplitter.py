"""
    [PORTUGUÊS]
     | Autor: Rafael Zacarias Palierini
     | GitHub: Zakonildo
     |
     | Grupo:                NOMES               |     R.A      
     |      |- Andy Silva Barbosa                | 22.218.025-9 |
     |      |- Rafael Zacarias Palierini         | 22.218.030-9 |
     |      |- Rubens de Araujo Rodrigues Mendes | 22.218.009-3 |
     |      |- Vitor Acosta da Rosa              | 22.218.006-9 |
     |
     | 2ª Atividade Prática de Compiladores
     | Name: Componente Separador de String em Python

     [DESCRIÇÃO]
        Este componente visa separar strings com a sintaxe em Python. Para utiliza-lo si-
        ga os comentários ao longo das funções.

    [TOKENS AND REGEX]

        keyword = {if, else, elif, def, for, while, return, break}
        operator = {==, !=, >=, <=, +=, -=, *=, /=, =, >, <, +, -, *, /}
        boolean = {True, False}
        : = {:}
        interger = {[ 0-9 ]+}
        float = {[ 0-9 ]+.[ 0-9 ]+}
        string = {"([ \s-! ]*[ #-$ ]*[ &-\[ ]*[ \]-~ ]*)*"}
        variable = {([ _-_ ]*[ A-Z ]*[ a-z ]+ | [ _-_ ]*[ A-Z ]+[ a-z ]* | [ _-_ ]+[ A-Z ]*[ a-z ]*)([ 0-9 ]*)}


    [ENGLISH]
     | Author: Rafael Zacarias Palierini
     | GitHub: Zakonildo
     |
     | Group:                NAMES               |     R.A      
     |      |- Andy Silva Barbosa                | 22.218.025-9 |
     |      |- Rafael Zacarias Palierini         | 22.218.030-9 |
     |      |- Rubens de Araujo Rodrigues Mendes | 22.218.009-3 |
     |      |- Vitor Acosta da Rosa              | 22.218.006-9 |
     |
     | Compilers 2nd Pratical Lesson
     | Name: Python String Splitter Component

    [DESCRIPTION]
        This component aims to split a string in Python's syntax. To use it, follow the
        commentaries along with the functions.

    [TOKENS AND REGEX]

        keyword = {if, else, elif, def, for, while, return, break}
        operator = {==, !=, >=, <=, +=, -=, *=, /=, =, >, <, +, -, *, /}
        boolean = {True, False}
        : = {:}
        interger = {[ 0-9 ]+}
        float = {[ 0-9 ]+.[ 0-9 ]+}
        string = {"([ \s-! ]*[ #-$ ]*[ &-\[ ]*[ \]-~ ]*)*"}
        variable = {([ _-_ ]*[ A-Z ]*[ a-z ]+ | [ _-_ ]*[ A-Z ]+[ a-z ]* | [ _-_ ]+[ A-Z ]*[ a-z ]*)([ 0-9 ]*)}
"""


# [PORTUGUÊS]
#   Está função irá filtra uma palavrar com um operador no meio dela, por exemplo "myVar=5".
#   Seu retorno deve ser uma lista e uma string. A lista deverá conter a palavra separada e
#   concatenada no fim da lista (Ex: [..., "myVar", "=", "5"]). A string retornada será o úl-
#   timoitem da separação (Ex: word="5").
#
# [ENGLISH]
#   This function will filter a word with the operator in the middle of it, for example
#   "myVar=5". The return must be a list and a string. The list should contain the word
#   splitted and appended in the end of the list (Ex. [..., "myVar", =, "5"]). The string
#   returned will be the last item of the split (Ex. word="5").
#
#   [PARAM]
#    | opMiddle(string, list[string], list[strings])
#    | return list[string], string

def opMiddle(word, newS, operator, key):
    global op
    word = word.replace(operator, " " + operator + " ").split(" ")
    for i in range(len(word)):
        if word[i] != "":
            if word[i] != operator:
                newS, finalWord = fullVerify(word[i], newS, op, key + 1)
                if finalWord == word[i]:
                    newS.append(word[i])
                    if i == 2:
                        word[2] = finalWord
            else:
                newS.append(word[i])
    word = word[-1]
    return newS, word

# [PORTUGUÊS]
#   Está função irá filtra uma palavrar com um operador no fim dela, por exemplo "else:".
#   Seu retorno deve ser uma lista e uma string. A lista deverá conter a palavra separada e
#   concatenada no fim da lista (Ex: [..., "else", ":"]). A string retornada será a palavra
#   sem o operador (Ex: word="else").
#
# [ENGLISH]
#   This function will filter a word with the operator in the end of it, for example
#   "else:". The return must be a list and a string. The list should contain the word
#   splitted and appended in the end of the list (Ex. [..., "else", ":"]). The string
#   returned will be the string without the operator (Ex. word="else").
#
#   [PARAM]
#    | opAfter(string, list[string], list[strings])
#    | return list[string], string

def opAfter(word, newS, operator):
    word = word.replace(operator, "")
    newS.append(word)
    newS.append(operator)
    return newS, word

# [PORTUGUÊS]
#   Está função irá filtra uma palavrar com um operador no começo dela, por exemplo "=myVar".
#   Seu retorno deve ser uma lista e uma string. A lista deverá conter apenas o operador sepa-
#   rado e concatenado no fim da lista (Ex: [..., "="]). A string retornada será a palavra sem
#   o operador (Ex: word="myVar").
#
# [ENGLISH]
#   This function will filter a word with the operator in the beginning of it, for example
#   "=myVar". The return must be a list and a string. The list should contain only the
#   operator splitted and appended in the end of the list (Ex. [..., "="]). The string
#   returned will be the string without the operator (Ex. word="myVar").
#
#   [PARAM]
#    | opBefore(string, list[string], list[strings])
#    | return list[string], string

def opBefore(word, newS, operator):
    newS.append(operator)
    word = word.replace(operator, "")
    return newS, word

# [PORTUGUÊS]
#   Está função irá fazer a verificação de "operadores" em uma dada palavra. Realiza
#   os callbacks das funções opBefore, opMiddle e opAfter respectivamente. Assim ga-
#   rantimos que não exista "operadores" reconhecidos na lista grudados com uma pala-
#   vra.
#
# [ENGLISH]
#   This function will do a verification at the "operators" in a given word. It callbacks
#   the fuctions opBefore, opMiddle and opAfter respectivily. By that is guaranted that
#   there's no recognized "operators" of the list joined in a word.
#
#   [PARAM]
#    | opAfter(string, list[string], list[strings])
#    | return list[string], string

def fullVerify(word, newS, op, key):
    find = [False, False, False]
    for i in op:
        if word.find(i) > -1 and word.find(i) < len(i) and word != "":
            newS, word = opBefore(word, newS, i)
            find[0] = True
            
    for i in range(len(op)):
        wIndex = word.find(op[i])
        if wIndex >= len(op[i]) and wIndex < len(word) - len(op[i]) and word != "" and i < 9:
            newS, word = opMiddle(word, newS, op[i], key)
            find[1] = True
        elif wIndex >= len(op[i]) and wIndex < len(word) - len(op[i]) and word != "" and word[wIndex] + word[wIndex+1] not in op[0:9]:
            newS, word = opMiddle(word, newS, op[i], key)
            find[1] = True
    for i in op:
        if  word.find(i) != -1 and word.find(i) >= len(word) - len(i) and word != "":
            newS, word = opAfter(word, newS, i)
            find[2] = True

    return newS, word


# [PORTUGUÊS]
#   Aqui é onde a mágica acontece, essa função recebe uma string, por exemplo s="if my_Var== 5:".
#   Ela é responsável por tratar por completo essa string, a separando e retornando uma lista com
#   cada lexema separado. O tratamento é feito primeiramente separando a palavra por espaços. Em
#   seguida é feito uma segunda passagem por cada palavra para verificar se não existem operadores
#   juntos de alguma palavra, por exemplo "my_Var==". Se houver serão utilizados as funções ante-
#   riores para fazer o tratamento e retornar a lista correta com os lexemas. O retorno é a pró-
#   pria lista com os lexemas separados
#
# [ENGLISH]
#   Here is where the magic happens, this function receive a string, for example s="if my_Var== 5:".
#   It is responsable for fully processing the string, separating it by spaces. Next is made a second
#   filter by each word to verify if don't exist operators along any word, for example "my_Var==". If
#   there are operators, the functions shown before will be utilized to do the treatment and return the
#   correct list with the lexemes. The return will be the list with the lexemes splitted.
#
#   [PARAM]
#    | splitString(string)
#    | return list[strings]

def splitString(s):
    global op
    global string
    s = s.split(" ")
    newS  = []
    for word in s:
        wordTemp = word
        if word.isalnum():
            newS.append(word)

        else:
            # [PORTUGUÊS]
            #   Tratamento de String.
            # [ENGLISH]
            #   String Treatment.
            if word[0] == '"':
                newS.append(word)
                if word[-1] == '"':
                    string = False
                continue

            if string == True:
                # [PORTUGUÊS]
                #   Se encontrar alguma ", ele deve juntar a última parte da string.
                # [ENGLISH]
                #   If it finds any ", it should join the last part of the string.
                if word.find('"') > -1:
                    string = not string
                    word = word.split('"')
                    newS[-1] += ' ' + word[0] + '"'
                    word = word[1]
                    if word == '':
                        continue
                else:
                    newS[-1] += ' ' + word
                    continue

            # [PORTUGUÊS]
            #   Daqui para baixo é feito o tratamento da palavra caso ela contenha
            #   algum operador.
            # [ENGLISH]
            #   Below is made a treatment for the word just in case it contains any
            #   "operator".
            if word in op:
                newS.append(op[op.index(word)])
                continue
            
            newS, word = fullVerify(word, newS, op, 0)

            if wordTemp == word or word != newS[-1] and word != newS[-2]:
                newS.append(word)
                continue

    finalS = []
    for i in newS:
        finalS.append(i)
        if i[0] == '"' and i[-1] != '"':
            string = True
            continue
        if string == True:
            finalS.pop()
            finalS[-1] += " " +  i
            if i.find('"') != -1:
                string = False

    return finalS

# [PORTUGUÊS]
#   Esta é a lista de operadores. Os "operadores" que devem ser filtrados devem estar aqui.
#
# [ENGLISH]
#   This is the operator's list. The "operators" that should be filtered must be here.

op = [":", "==", "!=", ">=", "<=", "+=", "-=", "*=", "/=", "=", ">", "<", "+", "-", "*", "/"]


# [PORTUGUÊS]
#   Este boolean controla se temos string ou não.
#
# [ENGLISH]
#   This boolean controls if we have string or not.

string = False
