from strspl import *
from afds import *

class Lexer:

    def getTokens(self, string):
        tokens_list = []
        # Lista com todas os lexemas separados.
        lexeme = strspl(string)
        # Loop para verificar os lexemas e criar os tokens.
        for word in lexeme:
            if afd_keywords(word)[0]:
               tokens_list.append((afd_keywords(word)[1], word))
    
            elif afd_operator(word)[0]:
                tokens_list.append((afd_operator(word)[1],word))
            
            elif afd_boolean(word)[0]:
                tokens_list.append(("BOOLEAN",word))
            
            elif afd_delimiters(word)[0]:
                tokens_list.append((afd_delimiters(word)[1],word))

            elif afd_numeric(word)[0]:
                tokens_list.append((afd_numeric(word)[1],word))
            
            elif afd_string(word)[0]:
                tokens_list.append((afd_string(word)[1],word))
            
            elif afd_identifier(word)[0]:
                tokens_list.append((afd_identifier(word)[1],word))
            
            else:
                tokens_list.append(("ERROR",word))

        return tokens_list
