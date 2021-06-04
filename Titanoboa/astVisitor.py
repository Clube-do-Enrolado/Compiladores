"""
Arquivo que contém a implementação do padrão de design Visitor,
considerando a estruturação pré-definida da sintaxe e da AST.

Autores:
    Vitor Acosta da Rosa
    Rubens de Araujo Rodrigues Mendes
    Rafael Zacarias Palierini
    Geraldo Lucas do Amaral
    Andy da Silva Barbosa
"""

class NodeVisitor(object):
    """
    Classe responsável por visitar cada nó da AST.
    """

    def visit(self, node):
        """
        Método que visita o nó.
        
        Método que acessa uma função recursiva para a resolução dos nós
        da AST gerada pelo Parser.

        Parameters:
        -----------
        node (object): Um objeto do tipo das classes que formam
        os nós da AST gerada pelo Parser.

        Return:
        Tupla contendo os nós da árvore lida.
        """
        node_name =  'visit_' + type(node).__name__
        visitor = getattr(self, node_name, self.visit_error)
        return visitor(node)

    def visit_error(self,node):
        """
        Método de erro de visita.
        Gera uma exceção de erro de acesso do nó. 
        """
        raise Exception ('Sem nós visit_{}'.format(type(node).__name__))

class Visitor(NodeVisitor):
    """
    Classe que acessa cada tipo de nó da AST retornando seus dados.
    """
    def __init__(self, tree):
        self.tree = tree

    def visit_DeclOp(self, node):
        """
        Método que resolve uma AST de declaração de variáveis.
        """
        return self.visit(node.left), self.visit(node.op), self.visit(node.right)

    def visit_BinOp(self, node):
        """
        Método que resolve uma AST de expressão binária.
        """
        return self.visit(node.left), self.visit(node.op), self.visit(node.right)

    def visit_DeclPrint(self, node):
        """
        Método que resolve uma AST de declaração de impressão.
        """
        return self.visit(node.left), self.visit(node.op)

    def visit_DeclFunc(self, node):
        """
        Método que resolve uma AST de uma função.
        """
        resolved_block = []
        if isinstance(node.right,list):
            for i in node.right:
                resolved_block.append(self.visit(i))
            
            return self.visit(node.left), self.visit(node.op), resolved_block
        
        else:
            return self.visit(node.left), self.visit(node.op), self.visit(node.right)

    def visit_DeclWhile(self, node):
        """
        Método que resolve uma AST da estrutura de repetição While
        """
        resolved_block = []
        
        # Verifica se o bloco estruturado dentro do If possui
        # n filhos. Pois é necessário visitar todos.
        if isinstance(node.right,list):
            for i in node.right:
                resolved_block.append(self.visit(i))
        
            return self.visit(node.left), self.visit(node.op), resolved_block
        
        else:
            return self.visit(node.left), self.visit(node.op), self.visit(node.right)
    
    def visit_DeclFor(self, node):
        """
        Método que resolve uma AST da estrutura de repetição For
        """
        resolved_block = []
        
        # Verifica se o bloco estruturado dentro do If possui
        # n filhos. Pois é necessário visitar todos.
        if isinstance(node.right,list):
            for i in node.right:
                resolved_block.append(self.visit(i))
        
            return self.visit(node.left), self.visit(node.op), resolved_block
        
        else:
            return self.visit(node.left), self.visit(node.op), self.visit(node.right)

    def visit_DeclIf(self, node):
        """
        Método que resolve uma AST da estrutura condicional IF
        """

        resolved_block = []
        is_nlines = False  # Avalia se o bloco possui diversas instruções
        
        # Verifica se o bloco estruturado dentro do If possui
        # n filhos. Pois é necessário visitar todos.
        if isinstance(node.block,list):
            is_nlines = True
            for i in node.block:
                resolved_block.append(self.visit(i))

        # Verifica se o IF tem ligação com um elif ou else
        if node.nested is None:
            if is_nlines:
                return self.visit(node.expr), self.visit(node.op), resolved_block
            else:
                return self.visit(node.expr), self.visit(node.op), self.visit(node.block)
        
        else:
            if is_nlines:
                return self.visit(node.expr), self.visit(node.op), resolved_block, self.visit(node.nested)
            else:
                return self.visit(node.expr), self.visit(node.op), self.visit(node.block), self.visit(node.nested)

    def visit_DeclElif(self, node):
        """
        Método que resolve uma AST referente à estrutura Elif.
        """
        resolved_block = []
        is_nlines = False  # Avalia se o bloco possui diversas instruções
        
        # Verifica se o bloco estruturado dentro do If possui
        # n filhos. Pois é necessário visitar todos.
        if isinstance(node.block,list):
            is_nlines = True
            for i in node.block:
                resolved_block.append(self.visit(i))

        # Verifica se o IF tem ligação com um elif ou else
        if node.nested is None:
            if is_nlines:
                return self.visit(node.expr), self.visit(node.op), resolved_block
            else:
                return self.visit(node.expr), self.visit(node.op), self.visit(node.block)
        
        else:
            if is_nlines:
                return self.visit(node.expr), self.visit(node.op), resolved_block, self.visit(node.nested)
            else:
                return self.visit(node.expr), self.visit(node.op), self.visit(node.block), self.visit(node.nested)


    def visit_DeclElse(self, node):
        """
        Método que resolve uma AST referente à estrutura Else.
        """
        resolved_block = []

        # Verifica se o bloco estruturado dentro do Else possui
        # n filhos. Pois é necessário visitar todos.
        if isinstance(node.block,list):
            for i in node.block:
                resolved_block.append(self.visit(i))

            return self.visit(node.op), resolved_block
        
        else:
            return self.visit(node.op), self.visit(node.block)

    def visit_DeclRange(self, node):
        """
        Método que resolve a declaração de um RANGE
        """
        return self.visit(node.left), self.visit(node.mid), self.visit(node.father), self.visit(node.right)

    def visit_Node(self, node):
        """
        Método que resolve um nó, retornando seu valor.
        """
        return node.value

    def visit_Token(self, node):
        """
        Método que resolve um token, o nível mais baixo de toda AST.
        """
        return node.value

    def visitall(self):
        """
        Método que resolve uma AST completa.
        """
        return self.visit(self.tree)

