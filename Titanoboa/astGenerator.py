"""
Arquivo responsável pelas classes que estruturam a AST
da linguagem, utilizada para gerar código.


Autores:
    Vitor Acosta da Rosa
    Rubens de Araujo Rodrigues Mendes
    Rafael Zacarias Palierini
    Geraldo Lucas do Amaral
    Andy da Silva Barbosa
"""


class AST(object):
    """
    Classe base para a AST.
    """
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
         # return f'{self.left} {self.op} {self.right}' 
         return [self.left, self.op, self.right]

class DeclIf(AST):
    """
    Classe representando a árvore de
    uma declaração de if.
                if
              / | \\
             /  |  \\
            / block \\ 
         expr    [elif|else]
    """
    def __init__(self, expr, op, block, nested = None):
        self.expr = expr
        self.op = op
        self.block = block
        self.nested = nested

    def solve(self):
        return f' {self.expr} {self.op} {self.block} {self.nested} '

class DeclElif(AST):
    """
    Classe representando a árvore de
    uma declaração de elif
               elif
             /  |  \\
            /   |   \\
           /    |    \\
          expr  |  [elif|else]
              block

    """
    def __init__(self, expr, op, block, nested = None):
        self.expr = expr
        self.op = op
        self.block = block
        self.nested = nested

    def solve(self):
        return f' {self.expr} {self.op} {self.block} {self.nested} '

class DeclElse(AST):
    """
    Classe representando a árvore da declaração
    de um else.

    A árvore resultante:
                else
                 |
               block
    """
    def __init__(self, op, block):
        self.op = op
        self.block = block

    def solve(self):
        return f' {self.op} {self.block} '

class DeclFunc(AST):
    """
    Classe representando a árvore da declaração
    de uma função.

    A árvore resultante é parecida com:
                  def
                /    \\
               /      \\
              /        \\
        Identifier    bloco 
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def solve(self):
        return f' {self.left} {self.op} {self.right} '

class DeclPrint(AST):
    """
    Classe representando a árvore da
    declaração de um print.

    A árvore deve obedecer o seguinte modelo:
                    print
                      |
                     expr
    """
    def __init__(self, op, left):
        self.op = op   # print
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

class DeclWhile(AST):
    """
    Classe da declaração de uma árvore de 
    um laço de repetição while.

    A árvore resultante deve seguir o determinado modelo abaixo:
        
            while
           /    \\
        expr    [bloco]

    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def solve(self):
        return f' {self.left} {self.op} {self.right} '

class Node(AST):
    """
    Classe representando terminais.
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def solve(self):
        return f' {self.token.value} '

