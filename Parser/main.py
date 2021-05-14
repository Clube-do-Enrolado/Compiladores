from lexicalAnalyser import *
from parser import *


lexer = Lexer()
token_objs =[]


with open('code.txt') as f:
    token_list = lexer.getTokens(f.read())

f.close()

interpreter = Interpreter(token_list)
