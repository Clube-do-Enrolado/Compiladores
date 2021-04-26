"""
    Classe auxiliar para transformar input normal
    em um dicionário viável para aplicação de AFD's.
"""
import collections


class ExpReader:
    def __init__(self, exp):
        self.operators = []
        self.chars = []
        self.exp_size = 0
        self.exp_dict = collections.defaultdict(dict)

        self.generate_info(exp)

    def generate_info(self, exp):
        for c in exp:          
            self.chars.append(c)
            
            self.exp_size += 1

    def get_dictionary(self):
        i = 0
        
        for i in range(0, self.exp_size):
            opr = False    
            
            if self.chars[i] == "+" or self.chars[i] == "*" or self.chars[i] == "|":
                               
                if self.chars[i] == "*":
                    if i+1 <= self.exp_size:
                        # Operação * pode não considerar o caractere
                        self.exp_dict[str(i-1)][str(self.chars[i-1])] = str(i+1)
                    
                    # ou pode considerar o caractere infinitas vezes
                    # ou seja, o caractere chars[i] leverá ao estado i 
                    self.exp_dict[str(i-1)][str(self.chars[i-1])] = str(i-1)

                
                elif self.chars[i] == "+": 
                    
                    # Operação pode considerar várias vezes o
                    # atual caractere
                    self.exp_dict[str(i-1)][str(self.chars[i-1])] = str(i-1)

                    if i+1 <= self.exp_size:
                        # entretanto, o atual caractere deve ter
                        # no mínimo uma ocorrência para transitar
                        # a um novo estado.
                        self.exp_dict[str(i-1)][str(self.chars[i-1])] = str(i + 1)
                
                # Operação |
                else: pass
                
            else:                                           
                if i + 1 == self.exp_size:
                    self.exp_dict[str(i)][str(self.chars[i])] = str(-1)
                else: 
                    self.exp_dict[str(i)][str(self.chars[i])] = str(i + 1)

        return self.exp_dict 
