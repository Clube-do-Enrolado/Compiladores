class Generator:
    def __init__(self, AST):
        """
        Classe que gera o código a partir de n ASTs.

        Parameters:
        -----------
        AST (Class.AST): Um conjunto de árvores semânticas
        abstratas.
        """

        # Lista com todas as ASTs geradas
        self.trees = AST
        # Posição para percorrer a lista de ASTs
        self.pos = 0
        # Árvore atual lida
        self.current_tree = self.trees[self.pos]
        # Nível de identação
        self.identlevel = 0
        
        # Operadores especiais considerados
        self.atr_opr = ["+=","-=","/=","*=","="]
        self.atr_log = ["in","and","or","not"]
        self.atr_ari = ["+","-","/","*"]
        self.atr_cmp = ["<",">","<=",">=","==","!="]

    def solve_ident(self):
        """
        Método utilitário que soluciona a identação do código
        final.
        """
        return "\t"*self.identlevel

    def solve_tree(self,inner_tree):
        """
        Método recursivo que percorre toda a AST
        para gerar o código.

        Dada uma AST base, acessa-se todos os nós,
        seguindo a sintaxe da linguagem, de forma que
        o código seja gerado.

        Parameters:
        -----------
        inner_tree (tuple): Estrutura da AST, baseado em
        tupla (nível mais alto) e podendo variar entre tuplas
        internas, listas ou somente strings, de acordo
        com a estruturação do código montado.

        Return:
        (string): Código gerado por uma AST.
        """
        ########################
        #   Declaração de IF   #
        ########################
        if "if" in inner_tree:
            # Adquire o index da raiz de uma declaração de if
            father_idx = inner_tree.index("if")
            code =""

            code += "if "

            # Resolve a expressão do IF
            expr = self.solve_tree(inner_tree[father_idx - 1])
            
            # Termina a geração da linha do IF
            code += expr+":"+"\n"

            # Aumenta identação para a próxima etapa
            self.identlevel += 1
            
            # Resolve o bloco do IF
            if isinstance(inner_tree[father_idx +1], list):
                child = self.solve_tree(inner_tree[father_idx + 1])
            else:
                child = self.solve_ident()+self.solve_tree(inner_tree[father_idx + 1])

            # Adiciona o bloco ao código
            code+= child
            # Reduz a identação
            self.identlevel -= 1

            # Ocorrência de um ELSE
            if len(inner_tree) == 4:
                elseBlock = self.solve_tree(inner_tree[father_idx + 2])
                code += elseBlock
                return code
            else:
                return code

        #######################
        # Declaração de else  #
        #######################
        if "else" in inner_tree:
            # Adquire o index da raiz de uma declaração de else
            father_idx = inner_tree.index("else")
            code = ""
            code += "else:\n"

            self.identlevel += 1
            if isinstance(inner_tree[father_idx +1], list):
                child = self.solve_tree(inner_tree[father_idx + 1])
            else:
                child = self.solve_ident()+self.solve_tree(inner_tree[father_idx + 1])
            
            code += child
            self.identlevel -= 1
            return code


        ########################
        # Declaração de função #
        ########################
        if "def" in inner_tree:
            # Adquire o index da raiz de uma declaração de função
            father_idx = inner_tree.index("def")
            code = ""
            
            # Salva a primeira linha da função
            code += "def " + inner_tree[father_idx-1] + "():\n"
            self.identlevel += 1

            if isinstance(inner_tree[father_idx +1], list):
                child = self.solve_tree(inner_tree[father_idx + 1])
            else:
                child = self.solve_ident()+self.solve_tree(inner_tree[father_idx + 1])
            
            code += child
            self.identlevel -= 1
            return code

        #####################
        # Declaração de FOR #
        #####################
        if "for" in inner_tree:
            # Adquire o index da raiz de uma declaração FOR
            father_idx = inner_tree.index("for")
            code = ""
            # Adiciona a raiz ao código
            code += "for "
            # Chama recursivamente a solução para o lado esquerdo da árvore
            # percorrendo toda a expressão que define o for.
            expr = self.solve_tree(inner_tree[father_idx - 1])
            code += expr+":"+"\n"

            self.identlevel += 1
            
            if isinstance(inner_tree[father_idx +1], list):
                # Chama recursivamente a solução para o lado direito da árvore
                # percorrendo todo o filho.
                child = self.solve_tree(inner_tree[father_idx + 1])
            else:
                child = self.solve_ident()+self.solve_tree(inner_tree[father_idx + 1])

            code += child
            self.identlevel-=1
            return code
        
        #######################
        # Declaração do while #
        #######################
        if "while" in inner_tree:
            # Adquire o index da raiz de uma declaração WHILE
            father_idx = inner_tree.index("while")
            code = ""

            code += "while "

            # Resolve o lado esquerdo da árvore
            expr = self.solve_tree(inner_tree[father_idx - 1])

            code += expr+":"+"\n"

            self.identlevel += 1
            
            if isinstance(inner_tree[father_idx +1], list):
                # Chama recursivamente a solução para o lado direito da árvore
                # percorrendo todo o filho.
                child = self.solve_tree(inner_tree[father_idx + 1])
            else:
                child = self.solve_ident()+self.solve_tree(inner_tree[father_idx + 1])
            
            code += child
            self.identlevel-=1
            return code

        # Verifica a ocorrência de uma lista na árvore
        # analisando, nesse caso, um bloco.
        elif isinstance(inner_tree,list):
            code = ""
            for i in inner_tree:
                code += self.solve_ident()+self.solve_tree(i)+"\n"
            return code
        

        #########
        # print #
        #########
        elif "print" in inner_tree:
            code = ""
            # Encontra o index da árvore interna que tem a palavra print
            father_idx = inner_tree.index("print")
            # Soluciona o print
            code += "print ("
            
            if isinstance(inner_tree[father_idx - 1],tuple):
                # Soluciona o filho esquerdo (expressão)
                expr = self.solve_tree(inner_tree[father_idx - 1])

            else:
                expr = inner_tree[father_idx - 1]

            code += expr+")"
            return code

        #############
        #   Range   #
        #############
        elif "range" in inner_tree:
            father_idx = inner_tree.index("range")
            return f'{inner_tree[father_idx]}({inner_tree[father_idx-2]},{inner_tree[father_idx-1]},{inner_tree[father_idx+1]})'  

        ##########################
        #    Operações lógicas   #
        ##########################
        elif any(x in inner_tree for x in self.atr_log): # Verifica se existe um operador lógico
            for i in self.atr_log:                       # para todo i no operador lógico
                if i in inner_tree:                      # se i estiver na árvore interna
                    father_idx = inner_tree.index(i)     # salva o index da raiz. 
            
            # Se o filho possuir filhos (representados por nós por tuplas dentro de tuplas)
            if isinstance(inner_tree[father_idx + 1],tuple):
                # Resolve o neto
                right = self.solve_tree(inner_tree[father_idx+1]) 
                # Retorna toda a árvore
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {right}'
            else:
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {inner_tree[father_idx + 1]}'

        ####################
        #    Atribuição    #
        ####################
        elif any(x in inner_tree for x in self.atr_opr): # Verifica se existe um operador de atribuição
            for i in self.atr_opr:                       # para todo i no operador de atribuição
                if i in inner_tree:                      # se i estiver na árvore interna
                    father_idx = inner_tree.index(i)     # salva o index da raiz.
            
            if isinstance(inner_tree[father_idx + 1],tuple):
                # Resolve o neto
                right = self.solve_tree(inner_tree[father_idx+1])
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {right}'
            else:
                if inner_tree[father_idx+1] == "input":
                    return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {self.solve_ident()}input()'
                else:
                    return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {inner_tree[father_idx+1]}'

        ####################
        #    Aritmética    #
        ####################
        elif any(x in inner_tree for x in self.atr_ari): # Verifica se existe um operador de atribuição
            for i in self.atr_ari:                       # para todo i no operador de atribuição
                if i in inner_tree:                      # se i estiver na árvore interna
                    father_idx = inner_tree.index(i)     # salva o index da raiz.
            
            if isinstance(inner_tree[father_idx + 1],tuple):
                # Resolve o neto
                right = self.solve_tree(inner_tree[father_idx+1])
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {right}'
            else:
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {inner_tree[father_idx+1]}'


        ####################
        #    Comparação    #
        ####################
        elif any(x in inner_tree for x in self.atr_cmp): # Verifica se existe um operador de atribuição
            for i in self.atr_cmp:                       # para todo i no operador de atribuição
                if i in inner_tree:                      # se i estiver na árvore interna
                    father_idx = inner_tree.index(i)     # salva o index da raiz.
            
            if isinstance(inner_tree[father_idx + 1],tuple):
                # Resolve o neto
                right = self.solve_tree(inner_tree[father_idx+1])
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {right}'
            else:
                return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {inner_tree[father_idx+1]}'

        ######################
        #   Tokens sozinhos  #
        ######################
        elif isinstance(inner_tree, str):
            return inner_tree

        else:
            raise Exception("Erro fatal! x_x")

    def generate_code(self):
        """
        Método que gera o código a partir de ASTs.
        """
        with open('tb.py','w') as f:
            # Percorre a lista de árvores
            for i in range(len(self.trees)):
                f.write("%s"%self.solve_tree(self.trees[i]))
                f.write("\n")
        f.close()

