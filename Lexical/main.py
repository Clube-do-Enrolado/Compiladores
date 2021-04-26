from lexicalAnalyser import *

lexer = Lexer()

with open('code.txt') as f:
     print(lexer.getTokens(f.read()))

f.close()

