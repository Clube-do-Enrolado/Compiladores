"""
Implementação do Parser Recursivo Descendente.

Autores:
    
    Vitor Acosta da Rosa
    Rubens de Araujo Rodrigues Mendes
    Rafael Zacarias Palierini
    Geraldo Lucas do Amaral
    Andy da Silva Barbosa

"""


class AST(object):
    pass

class BinOp(AST):
    """
    Classe representando uma operação binária.

    A árvore fica da seguinte maneira:
                operador
               /        \\
            left       right

    Sendo o operador [+,-,/,*,+=,-=,/=,*=,=,<=,<,>,>=,==,in,and,not,in]
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def solve(self):
         return f'{self.left} {self.op} {self.right}' 

class DeclOp(AST):
    """
    Classe representando a declaração.

    A ávore fica da seguinte maneira:
                operador
               /        \\
            left       right

    Sendo o operador =.
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def solve(self):
         return f'{self.left} {self.op} {self.right}' 

class DeclParam(AST):
    """
    Classe representando a declaração de parâmetros.
    Todos são nós folhas, pois a declaração de parâmetros
    terá pais em diferentes locais.     
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def solve(self):
        return f'{self.left} {self.right}'

class DeclPrint(AST):

    def __init__(self, op, left):
        self.op = op   # print
        self.left = left # expr

    def solve(self):
        return f'{self.left} {self.op}'

class DeclRet(AST):

    def __init__(self, op, left):
        self.op = op   # return
        self.left = left # expr

    def solve(self):
        return f'{self.left} {self.op}'

class DeclFor(AST):
    """
    Classe representando a declaração de um for.

    A árvore fica da seguinte forma:
                    for
                   /  \\     
                  /    \\
                in     DeclBlock
               /  \\
            Node  Node|DeclRange
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def solve(self):
        return f'{self.left} {self.op} {self.right}'

class DeclRange(AST):
    """
    Classe representando a declaração de range.
    
    A árvore fica da seguinte forma:

                    range
                   /  |  \\
                Node Node Node
    
    Sendo os nós folhas os intervalos do range.
    """
    def __init__(self, left, mid, father, right):
        self.left = left
        self.mid = mid
        self.father = father
        self.right = right

    def solve(self):
        return f'{self.left} {self.mid} {self.father} {self.right}'


class DeclFuncCall(AST):
    """
    Classe representado a chamada de uma função.

    A árvore será estruturada da seguinte maneira:
            identifier                                       identifier
                |          ou, de maneira equivalente       /   ..... \\
            DeclParam                                     Node  .....  Node
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def solve(self):
        return f'{self.left} {self.right}'

class Node(AST):
    """
    Classe representando terminais.
    """
    def __init__(self, token):
        self.token = token

    def solve(self):
        return f' {self.token.value} '

class Interpreter():
    def __init__(self, token_list):

        self.token_list = token_list

        self.pos = 0

        self.loop = 1

        self.current_token = self.token_list[self.pos]

        self.recognized = []

        self.lang_loop()

    def invalid_error(self, message):
        raise Exception(message)

    def retreat(self, flag):
        """
        Método para voltar o token atual para um token definido pela flag.

        Parameters:
        -----------
        flag(int): Posição que acessa a lista de tokens.
        Utilizado para retornar a um "checkpoint".

        Returns:
        None
        """
        # Retorna o token atual para o token ativo pela flag
        self.current_token = self.token_list[flag]
        # Salva a posição da flag para iteração
        i = flag
        # Retira os tokens consumidos erroneamentes
        while i < self.pos:
            self.recognized.pop()
            i+=1
        # Retorna a posição
        self.pos = flag
        # Reativa o loop se necessário
        if self.loop == 0:
            self.loop = 1

    def eat(self):
        """
        Método que consome o token atual se for válido.
        Método que consome o token n de uma cadeia de n tokens
        de saida do analisador léxico, avançando para um token
        n + 1.
        Parameters:
        -----------
        None
        Returns:
        None
        """
        self.pos += 1
        self.recognized.append(self.current_token.type)
        if self.pos == len(self.token_list):
            # Para a execução do método lang_loop.
            self.loop = 0
        else:
            # Avança para o próximo token da cadeia.
            self.current_token = self.token_list[self.pos]

    def lang_loop(self):
        """
        Método de loop que percorre todos as possibilidades.
        Método que mantém um loop enquanto houverem tokens a
        serem consumidos. Caso todas as derivações possíveis
        falhem, o loop é quebrado.
        """
        while self.loop:
            try:
                print(self.decl(True))
                print(self.recognized)
            except:
                return

        print("Reconhecidos: ",self.recognized)


    def decl(self, consider_newline):
        """
        Método referente ao símbolo inicial decl da linguagem.
        Pode derivar para outros sete símbolos não terminais.
        
        Parameters:
        -----------
        consider_newline(Boolean): Variável de controle que verifica se o
        token '\n' deve ser considerado na atual execução.

        Return:
        """
        nao_terminais = [self.decl_variavel, self.decl_if, self.decl_elif, self.decl_else,\
                self.decl_for, self.decl_while, self.decl_func, self.decl_print, self.decl_input]

        for producao in nao_terminais:
            try:
                a = producao()
                
                if consider_newline and self.current_token.type == "\n":
                    self.eat()
                
                if a is not None:
                    return a
            except:
                return

    def decl_variavel(self):
        """
        Método que implementa a declaração de variaveis
        decl_variavel -> IDENTIFIER opr_atrib expr
                       | IDENTIFIER opr_atrib decl_input
                       | IDENTIFIER( decl_param )
        """

        if self.current_token.type == "IDENTIFIER":
            c = self.current_token
            self.eat()
            a = self.opr_atrib()                # Busca por operadores de atribuição.
            if a is not None:                   # se o operador de atribuição foi encontrado
                b = self.expr()                 # tenta derivar uma expressão.
                if b is not None:               # Se a derivação foi bem sucedida
                    node = DeclOp(c, a, b)
                    return node                 # retorna a expressão reconhecida.

                else:                           # A declaração de expressão não foi concretizada.
                    b = self.decl_input()       # Verifica se um input foi definido
                    if b is not None:           # retorna a expressão reconhecida.
                        node = DeclOp(c,a,b)
                        return node
            else:
                if self.current_token.type == "(":
                    self.eat()
                    b = self.decl_param()
                    if self.current_token.type == ")":
                        self.eat() 
                        if b is not None:
                            node = DeclFuncCall(Node(c),b) 
                            return node
                        else:
                            return Node(c)

        # Qualquer token/produção que não siga a definição da
        # gramática, retorna None
        return None

    def decl_for(self):
        """
        Método que implementa o laço de repetição FOR
        decl_for -> FOR IDENTIFIER IN STRING|decl_range : bloco
        """
        # Posição relativa em relação à declaração.
        rel_pos = 0
        rng = None
        c = None
        # Enquanto o ponteiro "rel_pos" não chegar à última posição 5, avalia
        while rel_pos < 6:
            if self.current_token.type == "FOR" and rel_pos == 0:
                declpai = self.current_token
                self.eat() # Consome o token FOR
                rel_pos+=1
            
            elif self.current_token.type == "IDENTIFIER" and rel_pos == 1:
                a = self.current_token
                self.eat() # Consome o token IDENTIFIER
                rel_pos+=1

            elif self.current_token.type == "IN" and rel_pos == 2:
                b = self.current_token
                self.eat() # Consome o token IN
                rel_pos+=1

            # Verifica se a sintaxe segue STRING ou decl_range na posição 3
            elif rel_pos == 3:
                if self.current_token.type == "STRING": 
                    c = self.current_token
                    self.eat()            # Consome o token STRING
                    rel_pos+=1
                else:
                    rng = self.decl_range() # Tenta derivar para a declaração de range
                    if rng is not None:     # se a derivação foi feita com sucesso 
                        rel_pos+=1        # avança o "ponteiro".
                    else:                 # A sintaxe não utilizou STRING nem decl_range
                        return None       # portanto é inválida.

            elif self.current_token.type == ":" and rel_pos == 4:
                self.eat() # Consome o token :
                rel_pos+=1

            elif rel_pos == 5:
                block = self.bloco() # Derivação do conteúdo do FOR, obrigatório
                rel_pos+=1       # retorno diferente de None.

            else:
                return None

        if block is not None:
            if rng is not None:  # Se o FOR baseou-se em RANGE
                node = DeclFor(rng,Node(declpai),block)
                return node      # retorna somente o bloco
            elif c is not None:  # Se o FOR baseou-se em STRING 
                innernode = BinOp(Node(a),Node(b),Node(c))
                node = DeclFor(innernode,Node(declpai),block)
                return node
            
        return None


    def decl_while(self):
        """
        Método que resolve a declaração do laço de repetição WHILE
        decl_while -> WHILE expr : bloco
        """
        if self.current_token.type == "WHILE":
            self.eat()               # Consome o token WHILE
            a = self.expr()          # e tenta derivação para uma expressão
            if a is None:            # caso essa expressão não seja bem sucedida
                return None          # retorne None.
            else:
                if self.current_token.type == ":": 
                    self.eat()       # Consome o token :
                    b = self.bloco() # tenta derivar para um bloco

                    if b is not None:
                        return (a,b) # Retorna a expressão e o bloco

        # Caso o token saia de qualquer possibilidade apresentada.
        return None

    def decl_func(self):
        """
        Método que implementa a declaração de uma função
        decl_func -> DEF IDENTIFIER ( [decl_param] ) : bloco
        """

        rel_pos = 0 # Posição relativa a declaração
        a = None    # resposta possível para os parâmetros
        b = None    # resposta possível para o bloco

        while rel_pos < 7:

            if self.current_token.type == "DEF" and rel_pos == 0:
                self.eat()  # Consome DEF
                rel_pos+=1

            elif self.current_token.type == "IDENTIFIER" and rel_pos == 1:
                self.eat()  # Consome IDENTIFIER
                rel_pos+=1

            elif self.current_token.type == "(" and rel_pos == 2:
                self.eat() # Consome (
                rel_pos+=1

            # Declaração de parametros é opcional
            elif rel_pos == 3:
                a = self.decl_param() # Tenta derivação de parâmetros
                rel_pos+=1

            elif self.current_token.type == ")" and rel_pos == 4:
                self.eat()   # Consome )
                rel_pos+=1

            elif self.current_token.type == ":" and rel_pos == 5:
                self.eat()   # Consome :
                rel_pos+=1

            elif rel_pos == 6:
                b = self.bloco() # Tenta derivação para um bloco
                rel_pos+=1

            else:
                return None
        
        if b is not None:
            if a is None:
                return ("DEF",b)
            else:
                return (a,b)

        return False
    

    def decl_if(self):
        """
        Método que implementa uma estrutura condicional
        decl_if -> IF expr : bloco [decl_elif|decl_else]
        """
        if self.current_token.type == "IF":
            self.eat()
            a = self.expr()
            if a is None:   # Caso o IF não possua uma expressão
                return None # retorne None para erro.
            
            if self.current_token.type == ":":
                self.eat()
                
                b = self.bloco() 

                if b is None:   # O conteúdo dentro do IF não pode
                    return None # ser vazio, retorne None.

                else:                            # Se existe conteúdo dentro do if, é possível
                    elif_resp = self.decl_elif() # utilizar um elif,
                    if elif_resp is not None:
                        return (a,b,elif_resp)
                    else:                       # um else
                        else_resp = self.decl_else()
                        if else_resp is not None:
                            return (a,b,else_resp)

                        else:
                            return (a,b)         # ou somente a estrutura do IF.

    def decl_elif(self):
        """
        Método de implementação de ELIF
        decl_elif -> ELIF expr : bloco [decl_elif | decl_else]
        """

        if self.current_token.type == "ELIF":
            self.eat()                      # Consome o token ELIF
            a = self.expr()                 # Tenta derivar a expressão
            if a is None:                   # caso falhe,
                return None                 # retorna None.
            else:                           # Caso contrário
                if self.current_token.type == ":": 
                    self.eat()              # consome o token :
                    b = self.bloco()        # e tenta derivar o bloco (conteúdo do elif)
                    if b is None:           # se o bloco não foi bem sucedido
                        return None         # retorna None.

                    c = self.decl_elif()    # Tenta derivar um novo elif
                    if c is not None:       # se a derivação foi bem sucedida,
                        return (a,b,c)      # Retorna.

                    c = self.decl_else()    # Caso a derivação elif não funcionou
                    if c is not None:       # tenta derivar um ELSE
                        return (a,b,c)      # e retorná-lo.
                    
                    # Caso nenhuma derivação entre elif e else
                    # seja concretizada, retorna somente o ELIF inicial.
                    return (a,b)
        else:
            return None

    def decl_else(self):
        """
        Método que trata a declaração de um ELSE
        decl_else -> ELSE : bloco
        """
        if self.current_token.type == "ELSE":
            a = self.current_token
            self.eat()                   # Consome o token ELSE
            if self.current_token.type == ":":
                self.eat()               # Consome o token :
                b = self.bloco()         # Tenta derivar um bloco
                if b is not None:        # Caso a derivação seja bem sucedida
                    return (a,b)    # retorna o ELSE mais o bloco.
                else:
                    return None
        else:
            return None

    def bloco(self):
        """
        Método que identifica um bloco de expressões.
        Esse bloco serve para garantir a identação em
        expresões condicionais, laços de repetição e
        funções.
        bloco -> \n \t decl
               | \n \t decl_ret
               | \n \t BREAK
        """
        if self.current_token.type == "\n":
            self.eat()              # Consome \n
            if self.current_token.type == "\t": 
                while self.current_token.type == "\t":
                    self.eat()      # Consome \t

                if self.current_token.type == "BREAK":
                    self.eat()      # Consome BREAK
                    return "BREAK"  # retorna o token reconhecido.

                a = self.decl_ret() # Tenta derivar para uma declaração de retorno.
                if a is not None:   # Caso a tentativa retorne sucesso
                    return a        # retorna a resposta da derivação

                a = self.decl(False) # Tenta derivar para uma declaração genérica.
                if a is not None:   # Se a tentativa retornar sucesso
                    b = self.bloco()
                    return (a,b)        # retorna a resposta da derivação

    
        return None         # retorna None para nova avaliação.

    def bloco_sub(self):
        
        """
        Método que identifica um bloco de expressões.
        Esse bloco serve para garantir a identação em
        expresões condicionais, laços de repetição e
        funções.
        bloco -> \n \t decl
               | \n \t decl_ret
               | \n \t BREAK
        """
        if self.current_token.type == "\n":
            self.eat()              # Consome \n
            if self.current_token.type == "\t": 
                while self.current_token.type == "\t":
                    self.eat()      # Consome \t

                if self.current_token.type == "BREAK":
                    self.eat()      # Consome BREAK
                    return "BREAK"  # retorna o token reconhecido.

                a = self.decl_ret() # Tenta derivar para uma declaração de retorno.
                if a is not None:   # Caso a tentativa retorne sucesso
                    return a        # retorna a resposta da derivação

                a = self.decl(False) # Tenta derivar para uma declaração genérica.
                if a is not None:   # Se a tentativa retornar sucesso
                    b = self.bloco()
                    if b is not None:
                        # a e b devem ser ligados por um nó "BLOCO".
                        return (a,b)        # retorna a resposta da derivação

    
        return None         # retorna None para nova avaliação.

    def decl_ret(self):
        """
        Método que resolve a declaração de um RETURN
        decl_ret -> RETURN expr
        """
        if self.current_token.type == "RETURN":
            a = self.current_token
            self.eat()      # Consome o token RETURN
            c = self.expr()
            if c is not None:
                node = DeclRet(a,c)
                return node
        # Caso a declaração não foi realizada de forma satisfatória
        return None 
    
    def decl_input(self):
        """
        Método que resolve a declaração de um INPUT.
        decl_input -> INPUT()
        """

        if self.current_token.type == "INPUT":
            a = self.current_token
            self.eat()                                 # Consome o token INPUT.
            if self.current_token.type == "(":         # Verifica o token (
                self.eat()                             # consome o token (
                if self.current_token.type == ")":     # tenta fechar o parentese
                    self.eat()                         # consome o token )
                    node = Node(a)
                    return node                        # retorna a expressão.

        return None

    def decl_print(self):
        """
        Método que resolve a declaração de um PRINT.
        decl_print -> PRINT(expr)
        """

        if self.current_token.type == "PRINT":
            a = self.current_token
            self.eat()                                 # Consome o token PRINT.
            if self.current_token.type == "(":         # Verifica o token (
                self.eat()                             # consome o token (
                resposta = self.expr()                 # Tenta derivação de uma expressão
                if resposta is not None:               # caso a derivação funcione
                    if self.current_token.type == ")": # tenta fechar o parentese
                        self.eat()                     # consome o token )
                        node = DeclPrint(a,resposta)
                        return node                    # retorna a expressão.
                    else:                              # Se não fechou parenteses
                        return None                    # retorna erro!
            else:
                return None

        return None
    
    def decl_param(self):
        """
        Método que define uma declaração de parâmetros.
        decl_param -> IDENTIFIER
                    | IDENTIFIER, decl_param
        """
        if self.current_token.type == "IDENTIFIER":
            b = self.current_token
            self.eat()
            if self.current_token.type == ",":
                self.eat()
                a = self.decl_param()

                if a is not None:
                    return DeclParam(Node(b),a)
            else:
                return Node(b)
        return None
        
    def decl_range(self):
        """
        Método que resolve a declaração de um RANGE
        decl_range -> RANGE ( INTEGER|FLOAT, INTEGER|FLOAT, INTEGER|FLOAT ) 
        """
        # Posição relativa à sintaxe do range, serve para
        # visitar cada lexema a fim de verificar a correta estruturação.
        rel_pos = 0

        # Lista com as respostas (para retorno ao método que chamar)
        range_resp = []

        while rel_pos < 6:

            if self.current_token.type == "RANGE" and rel_pos == 0:
                range_resp.append(self.current_token)
                self.eat()
                rel_pos+=1

            elif self.current_token.type == "(" and rel_pos == 1:
                self.eat()
                rel_pos+=1

            elif rel_pos == 2 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT" or self.current_token.type == "IDENTIFIER"):
                    range_resp.append(self.current_token)
                    self.eat() 
                    rel_pos+=1
                    if self.current_token.type == ",":
                        self.eat() # Consome ,
                        rel_pos+=1

            elif rel_pos == 3 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT" or self.current_token.type == "IDENTIFIER"):
                    range_resp.append(self.current_token)
                    self.eat()
                    if self.current_token.type == ",":
                        self.eat() # Consome ,
                        rel_pos+=1

            elif rel_pos == 4 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT" or self.current_token.type == "IDENTIFIER"):
                    range_resp.append(self.current_token)
                    self.eat()
                    rel_pos+=1

            elif rel_pos == 5:
                # Fecha o range com parênteses
                if self.current_token.type == ")":
                    self.eat()
                    node = DeclRange(Node(range_resp[1]),Node(range_resp[2]),Node(range_resp[0]),Node(range_resp[3]))
                    return node

            else:
                return None

    def expr(self):
        """
        Método que resolve a gramática de uma expressão.
        expr -> expr_comp
              | expr_arit
              | expr_logi
              | expr_simples
        """
        # Percorre todas as expressões possíveis
        expressions = [self.expr_comp, self.expr_arit, self.expr_logi, self.expr_simples]
        for producao in expressions:
            try:
                a = producao() 
                if a is not None:
                    return a
            except:
                return

    def expr_comp(self):
        """
        Método que implementa uma expressão de comparação
        expr_comp -> expr_simples opr_comp expr_simples
        """
        # Salva o token atual (utilizado para o retreat se necessario)
        flag = self.pos
        # Tenta a derivação para uma expressão simples
        a = self.expr_simples()
        # Tenta derivar para operador de comparação
        opr_resp = self.opr_comp()
        # Caso esse operador seja um operador de comparação
        if opr_resp is not None:
            b = self.expr_simples()
            # Toda expressão foi montada corretamente
            if b:
                node = BinOp(Node(a), opr_resp, b) 
                return node                         # retorna o simbolo terminal, o operador e a expressão.

            # A expressão não foi montada corretamente
            # (a expressão final não retornou resposta)
            else:
                return None

        # Se não for um operador de comparação
        else:
            # Vomita o token consumido na derivação imediatamente anterior
            # para uma nova derivação (expr_arit, expr_logi, expr_simples)
            self.retreat(flag)
            return None

    def expr_arit(self):
        """
        Método que implementa uma expressão aritmética
        expr_arit -> expr_simples opr_arit expr_simples
        """
        # Salva o token atual (utilizado para o retreat se necessario)
        flag = self.pos
        # Tenta a derivação para uma expressão simples
        a = self.expr_simples()

        opr_resp = self.opr_arit()
        if opr_resp is not None:                    # Existe um operador aritmético
            b = self.expr_simples()
            if b:                                   # Se existe a expressão após o operador
                node = BinOp(Node(a), opr_resp, b) 
                return node                         # retorna o simbolo terminal, o operador e a expressão.

            # A expressão não foi montada corretamente
            # (a expressão final não retornou resposta)
            else:
                return None

	# Se o operador não for um aritmético
        else:
            # Vomita o último token consumido para uma nova análise
            self.retreat(flag)
            return None

    def expr_logi(self):
        """
        Método que implementa uma expressão aritmética
        expr_logi -> expr_simples opr_logi expr_simples
        """
        # Salva o token atual (utilizado para o retreat se necessario)
        flag = self.pos
        # Tenta derivar uma expressão simples
        a = self.expr_simples()

        opr_resp = self.opr_logi()
        if opr_resp is not None:                    # Se existe um operador lógico
            b = self.expr_simples()
            if b is not None:                       # Se existe uma expressão
                node = BinOp(Node(a), opr_resp, b)
                return node                         # retorna o simbolo terminal, o operador e a expressão.

            # A expressão não foi montada corretamente
            else:
                return None
        else:
            self.retreat(flag)
            return None 

    def expr_simples(self):
        """
        Método que representa o símbolo "expr_simples".
        expr_simples -> IDENTIFIER|INTEGER|FLOAT|STRING|BOOLEAN|(expr)
        """
        token = self.current_token
        result = None

        if token.type in ["IDENTIFIER","INTEGER","FLOAT","STRING","BOOLEAN"]:
            self.eat()
            result = Node(token)
        
        else:
            if self.current_token.type == "(":
                self.eat() # Consome o parenteses (
                result = self.expr()  # Resolve toda expressão dentro dos parênteses
                self.eat() # Consome o parenteses )
                 
        return result


    ####################################################
    ###             SIMBOLOS TERMINAIS               ###
    ####################################################
    
    def opr_atrib(self): 
        """
        Método que representa o símbolo terminal "opr_atrib".
        """
        token = self.current_token
        result = None
        
        if token.type in ["+=","-=","*=","/=","="]: 
            result = token
            self.eat()

        return result

    def opr_arit(self):
        """
        Método que representa o símbolo terminal "opr_arit".
        """
        token = self.current_token
        result = None

        if token.type in ["+","-","*","/"]:
            self.eat()
            result = token
        
        return result

    def opr_comp(self):
        """
        Método que representa o símbolo terminal "opr_comp".
        """
        
        token = self.current_token
        result = None

        if token.type in ["<","<=",">",">=","==","!="]:
            self.eat()
            result = token

        return result

    def opr_logi(self):
        """
        Método que representa o símbolo terminal "opr_logi".
        """
        token = self.current_token
        result = None

        if token.type in ["AND","OR","NOT","IN"]:
            self.eat()
            result = token

        return result
