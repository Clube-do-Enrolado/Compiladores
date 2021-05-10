from lexicalAnalyser import *

class Interpreter:
  def __init__(self,string):
    # Instancia da classe
    lexer = Lexer()
    
    # Adquire todos os tokens
    self.tokens = lexer.getTokens(string)

    # Posição atual para varrer a lista de tokens
    self.pos = 0
    
    self.reconhecidos = []
    self.hasParen = False

    self.returnValue = ""
    self.operators = ["+","-","*","/","==","!=","+=","-=","*=","/=","<",">","<=",">=","IN","AND","OR","NOT"]
    
    print([x.type for x in self.tokens])

  def size_tokens(self):
    return len(self.tokens)

  def return_a(self):
    return self.reconhecidos

  def current_token(self):
    '''
    Método que retorna o token atual entre os n tokens 
    retornados do analisador léxico.
    '''
    return self.tokens[self.pos]

  def invalid_error(self):
    '''
    Método que joga uma exceção para uma sintaxe incorreta.
    '''
    raise Exception('Sintaxe inválida!')

  def eat(self, token_type):
    '''
    Método que verifica o token atual com o token continueado.

    Método que analisa se o token atual é o mesmo que o token
    continueado, caso seja, esse token é consumido e o próximo
    token estará pronto para o mesmo processo.

    Parameters:
    -----------
    token_type(string): Tipo do token lido.

    Return:
    None

    '''
    if self.current_token().type == token_type:
        # Garante que a chamada do método current_token
        # retornorá o próximo token.
        self.reconhecidos.append(self.current_token().type)
        self.pos+=1
    else:
        self.invalid_error()

  def decl(self,need_response):
    """
    Método referente ao símbolo inicial decl da linguagem.
    Pode derivar para outros sete símbolos não terminais.

    Parameters: None
    Returns: None
    """
    resp = None
    while self.pos < len(self.tokens):
      resp = self.decl_variavel()
      if not resp:
        resp = self.decl_if()
        if not resp:
          resp = self.decl_for()
          if not resp:
            resp = self.decl_while()
            if not resp:
              resp = self.decl_func()
              if not resp:
                resp = self.decl_print()
                if not resp:
                  resp = self.decl_input()
                  if not resp:
                    if self.current_token().type == "\n":
                      self.eat("\n")
                      resp = "\n"
                    else:
                      print("ESSE CARA MORREU: ", self.current_token().type, " COM VALOR: ", self.current_token().value, " POS: ", self.pos)
                      if not need_response:
                        return self.invalid_error()
      
      if(need_response):
          return resp
      else:
          #Salva a árvore
          continue
             

  def decl_variavel(self):
    """
    Método que implementa o símbolo decl_variavel.
    Esse símbolo deriva, após ler os símbolos terminais
    IDENTIFIER e opr_atrib(), uma expressão.

    Parameters: None
    Returns: None
    """
    
    if self.current_token().type == "IDENTIFIER":
      self.eat("IDENTIFIER")
      # node("IDENTIFIER") <- Deve criar o nó
      a = self.opr_atrib()
      if a:
        b = self.expr()
        if b:
          return b  # Monta o nó
        else:
          b = self.decl_input()
          if b:
            return b # Monta o nó
          else:
            return False
      else:
        return False
    else:
      return self.decl_func()

  def decl_for(self):
    """
    Método que implementa o laço de repetição FOR.

    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "FOR"):
      self.eat("FOR")
      if(self.current_token().type == "IDENTIFIER"):
        self.eat("IDENTIFIER")        
        if(self.current_token().type == "IN"):
          self.eat("IN")          
          if(self.current_token().type == "STRING"):
            self.eat("STRING")
            if self.current_token().type == ":":
              self.eat(":")
              if self.current_token().type == "\n":
                self.eat("\n")
                resposta = self.bloco()
                if(resposta):
                  return True

          else:
            resposta = self.decl_range()
            if(resposta):
               if self.current_token().type == ":":
                  self.eat(":")
                  if self.current_token().type == "\n":
                    self.eat("\n")
                    resposta = self.bloco()
                    if(resposta):
                      return True
             
    return False
  
  def decl_while(self):
    """
    Método que implementa o método WHILE

    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "WHILE"):
      self.eat("WHILE")
      resposta = self.expr()
      if(resposta):
        if(self.current_token().type == ":"):
          self.eat(":")
          if self.current_token().type == "\n":
            self.eat("\n")
            resposta = self.bloco()
            if(resposta):
              return resposta
              
    return False
    

  def decl_func(self):
    """
    Método que implementa a declaração de uma função

    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "DEF"):
      self.eat("DEF")
      if(self.current_token().type == "IDENTIFIER"):
        self.eat("IDENTIFIER")
        if(self.current_token().type == "("):
          self.eat("(")
          resultado = self.decl_param()
          if(self.current_token().type == ")"):
            self.eat(")")
            if(self.current_token().type == ":"):
              self.eat(":")
              if self.current_token().type == "\n":
                self.eat("\n")
                return self.bloco()

    return False

  def decl_if(self):
    """
    Método que implementa a declaração de IF.
        
    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "IF"):
      self.eat("IF")
      resposta = self.expr()
      if(resposta):
        if(self.current_token().type == ":"):
          self.eat(":")
          if self.current_token().type == "\n":
              self.eat("\n")
              resposta = self.bloco()
              if(resposta):
                resposta = self.decl_elif()
                if(resposta):
                  return True
              else:
                resposta = self.decl_else()
                if(resposta):
                  return True
                else:
                  return True   
    return False

  def decl_elif(self):
    """
    Método que implementação de um ELIF

    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "ELIF"):
      self.eat("ELIF")
      resposta = self.expr()
      if(resposta):
        if(self.current_token().type == ":"):
          self.eat(":")
          if self.current_token().type == "\n":
              self.eat("\n")
              resposta = self.bloco()
              if(resposta):
                return resposta
          
    return False

  def decl_else(self):
    """
    Método que implementa o ELSE

    Parameters: None
    Returns: None
    """
    if(self.current_token().type == "ELSE"):
      self.eat("ELSE")
      if(self.current_token().type == ":"):
        self.eat(":")
        if self.current_token().type == "\n":
           self.eat("\n")
           resposta = self.bloco()
           if(resposta):
            return resposta
        
    return False

  def bloco(self):
    if(self.current_token().type == "\t"):
      self.eat("\t")
      resposta = self.decl(True)
      if(resposta):
        # Ainda existem declarações no bloco
        while self.current_token().type in ("\n","\t"):
          token = self.current_token().type
          self.eat(token)
          resposta = self.bloco()
        
        if not resposta:
          resposta = self.decl_ret()
          if not resposta:
              if(self.current_token().type == "BREAK"):
                  self.eat("BREAK")
                  resposta = True

        return resposta #Retorna o nó

      else:
        resposta = self.decl_ret()
        if(resposta):
          return resposta #Retorna o nó
        else:
          if(self.current_token().type == "BREAK"):
              self.eat("BREAK")
              return True

    return False

  def decl_ret(self):
    if(self.current_token().type == "RETURN"):
      self.eat("RETURN")
      resposta = self.expr()
      if(resposta):
        return resposta
      
    return False

  def decl_input(self):
    if(self.current_token().type == "INPUT"):
      self.eat("INPUT")
      resposta = self.expr()
      if(resposta):
        return True
      
    return False

  def decl_print(self):
    if(self.current_token().type == "PRINT"):
      self.eat("PRINT")
      resposta = self.expr()
      if(resposta):
        return True
      
    return False

  def decl_param(self):
    if(self.current_token().type == "IDENTIFIER"):
      self.eat("IDENTIFIER")
      if(self.current_token().type == ","):
        self.eat(",")
        resposta = self.decl_param()
        if(resposta):
          return True
      else:
        return True

    return False

  def decl_range(self):
    type_readed = 0
    if self.current_token().type == "RANGE":
      self.eat("RANGE")
      if self.current_token().type == "(":
        self.eat("(")
        while (self.current_token().type in ["INTEGER","FLOAT",","]) and type_readed < 3:
          if self.current_token().type == "," and type_readed == 0:
            return False
          else:
            token = self.current_token().type
            if(token != ","):
              type_readed += 1
                
            self.eat(token)

        if (type_readed > 0 and type_readed <= 3) and (self.current_token().type == ")"):
          self.eat(")")
          return True

    return False


  def expr(self):
    """
    Método que resolve a gramática de uma expressão.
    """
    if(self.current_token().type == "("): 
      self.eat("(")
      a = self.expr()
      while self.current_token().type != ")":
        b = self.expr()
      self.eat(")")
      self.expr()
      return True # Deve retornar a árvore de a,b

    else:
      resp = self.expr_comp()    
      while self.current_token().type in self.operators:
        resp = self.expr()
      return resp
      
  def expr_comp(self):
    # Expr_Comp = Opr_Comp Expr
        
    comp_opr = self.opr_comp()
    if(comp_opr):
        resposta = self.expr()
        if(resposta):
            return True
        else:
            return False
    else:
        return self.expr_arit()

  def expr_arit(self):
    # Expr_Arit = Opr_Arit Expr

    arit_opr = self.opr_arit()
    if(arit_opr):
        resposta = self.expr()
        if(resposta):
            return True
        else:
            return False
    else:
        return self.expr_logi()

  def expr_logi(self):
    # Expr_Logi = Opr_Logi Expr
            
    logic_opr = self.opr_logi()
    if(logic_opr):
        resposta = self.expr()
        if(resposta):
            return True
        else:
            return False
    else:
        return self.expr_simples()

  def expr_simples(self):
    """
    Método que representa o símbolo terminal "expr_simples".
    """
    result = None
    if self.current_token().type in ["IDENTIFIER","INTEGER","FLOAT","STRING","BOOLEAN"]:
        token = self.current_token()

        if token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            result = token.value

        elif token.type == "INTEGER":
            self.eat("INTEGER")
            result = token.value

        elif token.type == "FLOAT":
            self.eat("FLOAT")
            result = token.value

        elif token.type == "STRING":
            self.eat("STRING")
            result = token.value
        
        elif token.type == "BOOLEAN":
            self.eat("BOOLEAN")
            result = token.value

    return result

  def opr_atrib(self): 
    """
    Método que representa o símbolo terminal "opr_atrib".
    """
    result = None
    if self.current_token().type in ["+=","-=","*=","/=","="]:
        token = self.current_token()

        if token.type == "+=":
            self.eat("+=")
            result = token.value

        elif token.type == "-=":
            self.eat("-=")
            result = token.value

        elif token.type == "*=":
            self.eat("*=")
            result = token.value

        elif token.type == "/=":
            self.eat("/=")
            result = token.value
        
        elif token.type == "=":
            self.eat("=")
            result = token.value
    
    return result

  def opr_arit(self):
    """
    Método que representa o símbolo terminal "opr_arit".
    """
    result = None
    if self.current_token().type in ["+","-","*","/"]:
        token = self.current_token()

        if token.type == "+":
            self.eat("+")
            result = token.value

        elif token.type == "-":
            self.eat("-")
            result = token.value

        elif token.type == "*":
            self.eat("*")
            result = token.value

        elif token.type == "/":
            self.eat("/")
            result = token.value

    return result

  def opr_comp(self):
    """
    Método que representa o símbolo terminal "opr_comp".
    """
    result = None
    if self.current_token().type in ["<","<=",">",">=","==","!="]:
        token = self.current_token()

        if token.type == "<":
            self.eat("<")
            result = token.value

        elif token.type == "<=":
            self.eat("<=")
            result = token.value

        elif token.type == ">":
            self.eat(">")
            result = token.value

        elif token.type == ">=":
            self.eat(">=")
            result = token.value
        
        elif token.type == "==":
            self.eat("==")
            result = token.value
    
        elif token.type == "!=":
            self.eat("!=")
            result = token.value

    return result

  def opr_logi(self):
    """
    Método que representa o símbolo terminal "opr_logi".
    """
    result = None
    if self.current_token().type in ["AND","OR","NOT","IN"]:
        token = self.current_token()

        if token.type == "AND":
            self.eat("AND")
            result = token.value

        elif token.type == "OR":
            self.eat("OR")
            result = token.value

        elif token.type == "NOT":
            self.eat("NOT")
            result = token.value

        elif token.type == "IN":
            self.eat("IN")
            result = token.value

    return result

