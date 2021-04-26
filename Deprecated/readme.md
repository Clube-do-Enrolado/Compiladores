# Deprecated

Esse diretório contém códigos que já foram utilizados em versões passadas,
e atualmente está descontinuado, não sendo mais utilizado nas versões
atuais.

+ **dfa.py:** Código utilizado para reconhecer cadeias de Autômatos
Finitos Determinísticos. A lógica implementada foi generalista, em
busca de atender qualquer autômato que fosse previamente estruturado.
Essa versão foi descontinuada por não atender necessidades mais
específicas de cada autômato utilizado na linguagem.

+ **expressionreader.py:** Código complementar ao arquivo citado acima,
a ideia seria gerar um dicionário o qual o arquivo dfa.py conseguisse
interpretar. Como o **dfa.py** foi descontinuado, seu complemento também
foi.

+ **stringSplitter.py:** Código o qual dividia toda a string lida
pelo algoritmo, de forma que o analisador léxico poderia avaliar
palavra por palavra. Foi descontinuado por conta de suas operações
complexas, mas serviu de base para a nova versão **strspl.py**.

+ **tokenGenerator.py:** Código que avaliava a palavra lida pelo
arquivo citado acima e interpretava qual regex a reconhecia. 
Descontinuado por utilizar funções *built-in* do Python e não
Autômatos Finitos Determinísticos.

*Todos os códigos foram utilizados para atingir a versão final
do trabalho.*

