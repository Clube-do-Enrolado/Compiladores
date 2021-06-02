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
        # Código lido
        self.fullcode = ""

        self.identlevel = 0
        self.atr_opr = ["+=","-=","/=","*=","="]
        self.atr_log = ["in","and","or","not"]

    def next_tree(self):
        self.pos += 1
        self.current_tree = self.trees[self.pos]

    
    def solve_ident(self):
        return "\t"*self.identlevel

    def solve_tree(self,inner_tree):
        print(inner_tree)
        if "for" in inner_tree:
            # Adquire o index da raiz de uma declaração FOR
            father_idx = inner_tree.index("for")
            code = ""
            # Adiciona a raiz ao código
            code +=  self.solve_ident() + "for "
            # Chama recursivamente a solução para o lado esquerdo da árvore
            # percorrendo toda a expressão que define o for.
            expr = self.solve_tree(inner_tree[father_idx - 1])
            code += expr+":"+"\n"

            self.identlevel += 1
            # Chama recursivamente a solução para o lado direito da árvore
            # percorrendo todo o filho.
            child = self.solve_tree(inner_tree[father_idx + 1])

            code += child
            self.identlevel-=1
            return code

        # Verifica a ocorrência de uma lista na árvore
        # analisando, nesse caso, um bloco.
        elif isinstance(inner_tree,list):
            code = ""
            for i in inner_tree:
                code += self.solve_ident()+self.solve_tree(i)
            return code
        
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

            return f'{inner_tree[father_idx - 1]} {inner_tree[father_idx]} {inner_tree[father_idx + 1]}\n'

        else:
            return


    def generate_code(self):
        codigo = []
        # Percorre a lista de árvores
        for i in range(len(self.trees)):
            print(self.solve_tree(self.trees[i]))
        
        print(self.fullcode)
        print(codigo)


