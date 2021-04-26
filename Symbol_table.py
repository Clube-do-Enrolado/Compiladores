"""
Integrantes:

    Andy Silva Barbosa
    Rafael Palierini
    Rubens Mendes
    Vitor Acosta da Rosa

Para executar utilize o ipython3, o
comando display na função printHash
pode apresentar problemas ao compilar
com somente o python3 (no linux).
Sintaxe:
    ipython3 Symbol_table.py
"""


import numpy as np
import pandas as pd

class Symbol():
    """
    Classe responsável pela criação dos símbolos para a tabela.
    
    Parameters:
    -----------
    name (string): O nome do token.
    scope(string): O escopo identificado para aquele token.
    typo (string): O tipo do símbolo (e.g. int, float, function etc).
    value(string): O valor do símbolo.

    """
    def __init__(self, name, scope, typo, value):
        self.name = name
        self.scope = scope
        self.typo = typo
        self.value = value
        
    def getValues(self):
        """
        Método que retorna os valores em um vetor unidimensional.
        
        Returns:
        --------
        (List): Lista contendo todos os dados do símbolo.
        """
        return [self.name, self.scope, self.typo, self.value]
    
hashTable = {}

def lookup(symbol, hashTable):
    """
    Função utilizada para pesquisar através do nome, o símbolo dado
    na tabela Hash. A fim de tratar possíveis erros no código.

    Parameters:
    -----------
    symbol (Symbol): Uma instância da classe Symbol, contendo
    as informações.
    hashTable(dict): Dicionário que contém os símbolos já
    computados, suas chaves são os nomes dos símbolos e
    os valores são os objetos Symbol.

    Returns:
    --------
    (List): Lista contendo os erros encontrados [0] representa
    sem erro e [1] representa erro (inexistência do símbolo,
    símbolo com tipo ou escopo diferentes e incoerência de valor
    e tipo do símbolo).

    """
    name = symbol.name
    err = np.zeros((4,), dtype=int)
    values = []

    try:
        values = hashTable[name]
        print("OK")
    except:
        print("Símbolo Inexistente")
        err[0] = 1
        return err
    
    if values[2] == symbol.typo:
        print("OK")
    else:
        print("O símbolo possui um tipo diferente.")
        err[1] = 1
    
    if values[1] == symbol.scope:
        print("OK")
    else:
        print("O símbolo possui um escopo diferente.")
        err[2] = 1
    
    if values[0] == symbol.name and values[1] == symbol.scope and values[2] != symbol.typo:
        print("OK")
    else:
        print("Os tipos de variável e valor não coincidem.")
        err[3] = 1
    
    return err


def insertSymbol(symbol, hashTable):
    """
    Função que insere um dado símbolo na tabela hash.

    Parameters:
    -----------
    symbol (Symbol): Instância da classe Symbol com
    todos os dados de um determinado símbolo.
    hashTable(dict): Dicionário que contém os símbolos já
    computados, suas chaves são os nomes dos símbolos e
    os valores são os objetos Symbol.
    
    Returns:
    --------
    (dict): Tabela hash atualizada com a última inserção.

    """
    name = symbol.name
        
    hashTable[name] = symbol.getValues()

    return hashTable

def printHash(hashTable):
    """
    Função que imprime os dados presentes na tabela Hash.

    Parameters:
    -----------
    hashTable(dict): Dicionário que contém os símbolos já
    computados, suas chaves são os nomes dos símbolos e
    os valores são os objetos Symbol.
    
    Returns:
    --------
    None

    """

    symbols = pd.DataFrame.from_dict(hashTable, orient='index').reset_index()
    symbols.columns = ["Chave", "Nome", "Escopo", "Tipo", "Valor"]
    symbols = symbols.drop("Chave", axis = 1)
    display(symbols.head(999))
    
# -------- Area de teste -------- #
s1 = Symbol("Nome","global","string","paranaue")
s2 = Symbol("Nome2","global","float",12.55)
s3 = Symbol("my_var","local","int",21423)
s4 = Symbol("Shazum","global","float",503.4)
s5 = Symbol("meu_var","global","string","oxala")
s6 = Symbol("seilaa","global","int",1232)
s7 = Symbol("_var_my","local","float",2142.55)
s8 = Symbol("Batema","global","int",501)
s9 = Symbol("NooN","global","string","alguma coisa")
s10 = Symbol("variavel","global","int",423)
s11 = Symbol("my_var_2","local","int",6546)
s12 = Symbol("vish","global","float",8676.56)
s13 = Symbol("vish","local","string","boa noite")

insertSymbol(s1, hashTable)
insertSymbol(s2, hashTable)
insertSymbol(s3, hashTable)
insertSymbol(s4, hashTable)
insertSymbol(s5, hashTable)
insertSymbol(s6, hashTable)
insertSymbol(s7, hashTable)
insertSymbol(s8, hashTable)
insertSymbol(s9, hashTable)
insertSymbol(s10, hashTable)
insertSymbol(s11, hashTable)
insertSymbol(s12, hashTable)
print(lookup(s13, hashTable))

printHash(hashTable)
