from lexicalAnalyser import *
from intsub import *


lexer = Lexer()
token_objs =[]


with open('code.txt') as f:
    obj = Interpreter(f.read())

f.close()

obj.decl(False)

print(obj.return_a())
