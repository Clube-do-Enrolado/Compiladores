from strspl import *
from afds import *


class Token:
    '''
    Classe que representa um Token.
    '''
    def __init__(self, token_type, token_value):
        '''
        Método de inicialização da classe que representa um Token

        Parameters
        ----------
        token_type(string): Tipo do token reconhecido.
        token_value(string): Valor do token reconhecido.

        Return
        ------
        None

        '''

        self.type = token_type
        self.value = token_value

class Lexer:
    def getTokens(self, string):
        '''
        Método que avalia um dado código e retorna seu token.

        Método que lê lexema por lexema, categoriza-o como um
        token que obedece a algum AFD dos 7 AFDs definidos 
        a partir das regras da linguagem, salva-os em uma lista
        e retorna-os para utilização.

        Parameters
        ----------
        string(string): Código para ser avaliado através dos
        afds previamente definidos e que obedecem a linguagem
        proposta.

        Return
        ------
        strings(list): Lista contendo TODOS tokens identificados
        na string inicial dada.
        '''

        tokens_list = []
        # Lista com todas os lexemas separados.
        lexeme = strspl(string)
        # Loop para verificar os lexemas e criar os tokens.
        for word in lexeme:
            if afd_keywords(word)[0]:
               tokens_list.append(Token(afd_keywords(word)[1], word))
    
            elif afd_operator(word)[0]:
                tokens_list.append(Token(afd_operator(word)[1],word))
            
            elif afd_boolean(word)[0]:
                tokens_list.append(Token("BOOLEAN",word))
            
            elif afd_delimiters(word)[0]:
                tokens_list.append(Token(afd_delimiters(word)[1],word))

            elif afd_numeric(word)[0]:
                tokens_list.append(Token(afd_numeric(word)[1],word))
            
            elif afd_string(word)[0]:
                tokens_list.append(Token(afd_string(word)[1],word))
            
            elif afd_identifier(word)[0]:
                tokens_list.append(Token(afd_identifier(word)[1],word))
            
            else:
                tokens_list.append(Token("ERROR",word))

        return tokens_list
