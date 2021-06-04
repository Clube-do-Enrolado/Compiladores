from lexicalAnalyser import *
from parserTitanoboa import *
from codeGenerator import *
from symbolTable import *


class Titanoboa:
    def __init__(self):
        self.program_tokens = []
        self.visitorNodes = []
        self.titanoboa_to_python()

    def titanoboa_to_python(self):
        lexer = Lexer()
        
        with open('code.txt','r') as f:
            token_list = lexer.getTokens(f.read())    
        self.program_tokens = token_list
        f.close()
        
        interpreter = Interpreter(token_list)
        tree = interpreter.retornaarvores()

        for t in tree:
            vis = Visitor(t)
            self.visitorNodes.append(vis.visitall())
        
        code = Generator(self.visitorNodes)
        code.generate_code()

if __name__ == "__main__":
    Titanoboa()

