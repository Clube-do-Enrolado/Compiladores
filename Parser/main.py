from lexicalAnalyser import *
from parserfinal import *
from codeGenerator import *

lexer = Lexer()

with open('code.txt','r') as f:
    token_list = lexer.getTokens(f.read())

f.close()

interpreter = Interpreter(token_list)


tree = interpreter.retornaarvores()
a = []
for t in tree:
    vis = Visitor(t)
    a.append(vis.visitall())

code = Generator(a)
code.generate_code()
