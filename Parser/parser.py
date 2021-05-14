"""
Implementação do Parser Recursivo Descendente.

Autores:
    
    Vitor Acosta da Rosa
    Rubens de Araujo Rodrigues Mendes
    Rafael Zacarias Palierini
    Geraldo Lucas do Amaral
    Andy da Silva Barbosa

"""

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
                       | IDENTIFIER opr_atrib IDENTIFIER (decl_param)
                       | IDENTIFIER( decl_param )
        """

        if self.current_token.type == "IDENTIFIER":
            self.eat()
            a = self.opr_atrib()                # Busca por operadores de atribuição.
            if a is not None:                   # se o operador de atribuição foi encontrado

                # Testa a atribuição de retorno de função
                if self.current_token.type == "IDENTIFIER":
                    self.eat()
                    if self.current_token.type == "(":
                        self.eat()
                        b = self.decl_param()
                        if self.current_token.type == ")":
                            self.eat() 
                            if b is not None:
                                return ("IDENTIFIER",b)
                            else:
                                return ("IDENTIFIER()")
                else:
                    b = self.expr()                 # tenta derivar uma expressão.
                    if b is not None:               # Se a derivação foi bem sucedida
                        return ("IDENTIFIER",a,b)   # retorna a expressão reconhecida.

                    else:                           # A declaração de expressão não foi concretizada.
                        b = self.decl_input()       # Verifica se um input foi definido
                        if b is not None:           # retorna a expressão reconhecida.
                            return ("IDENTIFIER",a,b)
            else:
                if self.current_token.type == "(":
                    self.eat()
                    b = self.decl_param()
                    if self.current_token.type == ")":
                        self.eat() 
                        if b is not None:
                            return ("IDENTIFIER",b)
                        else:
                            return ("IDENTIFIER()")

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
        # Possível retorno de declaração de range, pode ser usado ou não.
        a = None
        b = None
        # Enquanto o ponteiro "rel_pos" não chegar à última posição 5, avalia
        while rel_pos < 6:
            if self.current_token.type == "FOR" and rel_pos == 0:
                self.eat() # Consome o token FOR
                rel_pos+=1
            
            elif self.current_token.type == "IDENTIFIER" and rel_pos == 1:
                self.eat() # Consome o token IDENTIFIER
                rel_pos+=1

            elif self.current_token.type == "IN" and rel_pos == 2:
                self.eat() # Consome o token IN
                rel_pos+=1

            # Verifica se a sintaxe segue STRING ou decl_range na posição 3
            elif rel_pos == 3:
                if self.current_token.type == "STRING": 
                    self.eat()            # Consome o token STRING
                    rel_pos+=1
                else:
                    a = self.decl_range() # Tenta derivar para a declaração de range
                    if a is not None:     # se a derivação foi feita com sucesso 
                        rel_pos+=1        # avança o "ponteiro".
                    else:                 # A sintaxe não utilizou STRING nem decl_range
                        return None       # portanto é inválida.

            elif self.current_token.type == ":" and rel_pos == 4:
                self.eat() # Consome o token :
                rel_pos+=1

            elif rel_pos == 5:
                b = self.bloco() # Derivação do conteúdo do FOR, obrigatório
                rel_pos+=1       # retorno diferente de None.

            else:
                return None

        if b is not None:
            if a is None:   # Se o FOR baseou-se em STRING
                return b    # retorna somente o bloco
            else:           # Se o FOR baseou-se em RANGE
                return (a,b)# retorna o range e o bloco
        
        # Caso nenhuma condição foi satisfeita
        else:
            # O FOR não é aplicável.
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
            self.eat()                   # Consome o token ELSE
            if self.current_token.type == ":":
                self.eat()               # Consome o token :
                a = self.bloco()         # Tenta derivar um bloco
                if a is not None:        # Caso a derivação seja bem sucedida
                    return ("ELSE",a)    # retorna o ELSE mais o bloco.
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
                                

    def decl_ret(self):
        """
        Método que resolve a declaração de um RETURN
        decl_ret -> RETURN expr
        """
        if self.current_token.type == "RETURN":
            self.eat()      # Consome o token RETURN
            a = self.expr()
            if a is not None:
                return a
        # Caso a declaração não foi realizada de forma satisfatória
        return None 
    
    def decl_input(self):
        """
        Método que resolve a declaração de um INPUT.
        decl_input -> INPUT(expr)
                    | INPUT()
        """

        if self.current_token.type == "INPUT":
            self.eat()                                 # Consome o token INPUT.
            if self.current_token.type == "(":         # Verifica o token (
                self.eat()                             # consome o token (
                resposta = self.expr()                 # Tenta derivação de uma expressão
                if resposta is not None:               # caso a derivação funcione
                    if self.current_token.type == ")": # tenta fechar o parentese
                        self.eat()                     # consome o token )
                        return resposta                # retorna a expressão.
                    else:                              # Se não fechou parenteses
                        return None                    # retorna erro!

                else: # Caso não tenha uma expressão, tenta somente os parênteses.
                    if self.current_token.type == ")":
                        self.eat()
                        return "INPUT()"

        return None

    def decl_print(self):
        """
        Método que resolve a declaração de um PRINT.
        decl_print -> PRINT(expr)
        """

        if self.current_token.type == "PRINT":
            self.eat()                                 # Consome o token PRINT.
            if self.current_token.type == "(":         # Verifica o token (
                self.eat()                             # consome o token (
                resposta = self.expr()                 # Tenta derivação de uma expressão
                if resposta is not None:               # caso a derivação funcione
                    if self.current_token.type == ")": # tenta fechar o parentese
                        self.eat()                     # consome o token )
                        return resposta                # retorna a expressão.
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
            self.eat()
            if self.current_token.type == ",":
                self.eat()
                a = self.decl_param()

                if a is not None:
                    return a
            else:
                return "IDENTIFIER"
        return None
        


    def decl_range(self):
        """
        Método que resolve a declaração de um RANGE
        decl_range -> RANGE ( INTEGER|FLOAT )
                    | RANGE ( INTEGER|FLOAT, INTEGER|FLOAT )
                    | RANGE ( INTEGER|FLOAT, INTEGER|FLOAT, INTEGER|FLOAT ) 
        """
        # Posição relativa à sintaxe do range, serve para
        # visitar cada lexema a fim de verificar a correta estruturação.
        rel_pos = 0

        # Lista com as respostas (para retorno ao método que chamar)
        range_resp = []

        while rel_pos < 6:

            if self.current_token.type == "RANGE" and rel_pos == 0:
                self.eat()
                rel_pos+=1
                range_resp.append("RANGE")

            elif self.current_token.type == "(" and rel_pos == 1:
                self.eat()
                rel_pos+=1

            elif rel_pos == 2 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT"):
                    self.eat() # Consome INTEGER
                    rel_pos+=1
                    if self.current_token.type == ",":
                        self.eat() # Consome ,
                    range_resp.append(self.current_token.type)

            elif rel_pos == 3 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT"):
                    self.eat()
                    rel_pos+=1
                    if self.current_token.type == ",":
                        self.eat() # Consome ,
                    range_resp.append(self.current_token.type)

            elif rel_pos == 4 and (self.current_token.type == "INTEGER" or self.current_token.type == "FLOAT"):
                    self.eat()
                    rel_pos+=1
                    range_resp.append(self.current_token.type)

            # O intervalo de posições é [3,5]
            # pois é possível o range contar com somente um argumento (posição 3),
            # dois argumentos (posições 3 e 4) ou três (posições 3,4 e 5).
            elif rel_pos > 2 and rel_pos < 6:
                # Fecha o range com parênteses
                if self.current_token.type == ")":
                    self.eat()
                    return range_resp

            else:
                return None

    def expr(self):
        """
        Método que resolve a gramática de uma expressão.
        expr -> (expr)
              | expr_comp
              | expr_arit
              | expr_logi
              | expr_simples
        """
        if(self.current_token.type == "("):
            self.eat() # Consome o parenteses (
            a = self.expr()  # Resolve toda expressão dentro dos parênteses
            self.eat() # Consome o parenteses )
            b = self.expr() # Resolve nova expressão (se existir)
            if b is not None:
                return (a, b)  # Deve retornar a árvore de a,b
            else:
                return a # Deve retornar somente a expressão dentro dos parenteses
        else:
            # Se não começar com (, tenta encaixar em outra derivação
            return self.expr_comp()

    def expr_comp(self):
        """
        Método que implementa uma expressão de comparação
        expr_comp -> expr_simples opr_comp expr
        """

        # Tenta a derivação para uma expressão simples
        # perceba que o resto da derivação não depende necessariamente
        # do resultado desta derivação. Isso porque pode acontecer
        # quando expr recebe um operador (aritmético, comparação, lógico).
        a = self.expr_simples()
        
        # Tenta derivar para operador de comparação
        opr_resp = self.opr_comp()
        # Caso esse operador seja um operador de comparação
        if opr_resp is not None:
            resposta = self.expr()
            # Toda expressão foi montada corretamente
            if resposta:
                if a is not None:
                    return (a, opr_resp, resposta)
                else:
                    return (opr_resp, resposta)

            # A expressão não foi montada corretamente
            # (a expressão final não retornou resposta)
            else:
                return None

        # Se não for um operador de comparação
        else:
            if a is not None:
                b = self.expr_arit()
                if b is not None:
                    return (a, b)
                else:
                    return a
            else:
                return self.expr_arit()

    def expr_arit(self):
        """
        Método que implementa uma expressão aritmética
        expr_arit -> expr_simples opr_arit expr
        """
        a = self.expr_simples()
        opr_resp = self.opr_arit()
        if opr_resp is not None:                    # Existe um operador aritmético
            resposta = self.expr()                  # busca por uma expressão complementar.
            if resposta:                            # Se existe a expressão após o operador
                if a is not None:                   # e existe um simbolo terminal inicial
                    return (a, opr_resp, resposta)  # retorna o simbolo terminal, o operador e a expressão.
                else:                               # Caso contrário, 
                    return (opr_resp, resposta)     # retorna somente o operador e a expressão.

            # A expressão não foi montada corretamente
            # (a expressão final não retornou resposta)
            else:
                return None

	# Se o operador não for um aritmético
        else:
            if a is not None:
                b = self.expr_logi()
                if b is not None:
                    return (a, b)
                else:
                    return a
            else:
                # Verifica se a expressão é lógica
                return self.expr_logi()

    def expr_logi(self):
        """
        Método que implementa uma expressão aritmética
        expr_logi -> expr_simples opr_logi expr
        """

        a = self.expr_simples()

        opr_resp = self.opr_logi()
        if opr_resp is not None:                    # Se existe um operador lógico
            resposta = self.expr()                  # tenta encontrar uma expressão. 
            if resposta is not None:                # Se existe uma expressão  
                if a is not None:                   # e um simbolo terminal anterior
                    return (a, opr_resp, resposta)  # retorna o simbolo terminal, o operador e a expressão.
                else:                               # Caso não exista um simbolo terminal inicial
                    return (opr_resp, resposta)     # retorna somente o operador e a expressão.

            # A expressão não foi montada corretamente
            else:
                return None
        else:
            # Caso não reconheça um operador lógico
            # recorre ao símbolo terminal expr_simples (se existir)
            if a is not None:
                return a
            else:
                return None

    ####################################################
    ###             SIMBOLOS TERMINAIS               ###
    ####################################################

    def expr_simples(self):
        """
        Método que representa o símbolo terminal "expr_simples".
        """

        token = self.current_token

        if token.type == "IDENTIFIER":
            self.eat()
            result = token.type

        elif token.type == "INTEGER":
            self.eat()
            result = token.type

        elif token.type == "FLOAT":
            self.eat()
            result = token.type

        elif token.type == "STRING":
            self.eat()
            result = token.type
        
        elif token.type == "BOOLEAN":
            self.eat()
            result = token.type

        else:
            result = None

        return result

    def opr_atrib(self): 
        """
        Método que representa o símbolo terminal "opr_atrib".
        """
        token = self.current_token

        if token.type == "+=":
            self.eat()
            result = token.type

        elif token.type == "-=":
            self.eat()
            result = token.type

        elif token.type == "*=":
            self.eat()
            result = token.type

        elif token.type == "/=":
            self.eat()
            result = token.type
        
        elif token.type == "=":
            self.eat()
            result = token.type
        
        else:
            result = None

        return result

    def opr_arit(self):
        """
        Método que representa o símbolo terminal "opr_arit".
        """
        token = self.current_token

        if token.type == "+":
            self.eat()
            result = token.type

        elif token.type == "-":
            self.eat()
            result = token.type

        elif token.type == "*":
            self.eat()
            result = token.type

        elif token.type == "/":
            self.eat()
            result = token.type

        else:
            result = None

        return result

    def opr_comp(self):
        """
        Método que representa o símbolo terminal "opr_comp".
        """
        
        token = self.current_token

        if token.type == "<":
            self.eat()
            result = token.type

        elif token.type == "<=":
            self.eat()
            result = token.type

        elif token.type == ">":
            self.eat()
            result = token.type

        elif token.type == ">=":
            self.eat()
            result = token.type
        
        elif token.type == "==":
            self.eat()
            result = token.type
    
        elif token.type == "!=":
            self.eat()
            result = token.type
    
        else:
            result = None

        return result

    def opr_logi(self):
        """
        Método que representa o símbolo terminal "opr_logi".
        """
        token = self.current_token

        if token.type == "AND":
            self.eat()
            result = token.type

        elif token.type == "OR":
            self.eat()
            result = token.type

        elif token.type == "NOT":
            self.eat()
            result = token.type

        elif token.type == "IN":
            self.eat()
            result = token.type

        else:
            result = None

        return result
