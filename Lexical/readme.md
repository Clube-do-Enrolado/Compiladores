# Implementação do analisador léxico

Diretório contendo a implementação de um analisador léxico.
A função de um analisador léxico é retornar os tokens de cada
palavra reconhecida de uma determinada linguagem, dado um
arquivo fonte com as sentenças.

O reconhecimento dessas palavras é feito através de AFDs, 
com transições previamente definidas e obedecendo as
expressões regulares da linguagem.

## Instruções para o uso do analisador léxico
 
### Estruturação dos arquivos

É de suma importância que os arquivos "lexicalAnalyser.py",
"strspl.py", "afds.py", "main.py" e um arquivo de leitura
que pode ser modificado, mas deve ter o nome "code.txt"

+ **strspl.py:** Dado uma string (um código fonte), é
realizada a sepação entre palavras levando em conta delimitadores
e caracteres especiais (como espaços, dois pontos, sinais de
adição, subtração etc.)

+ **afds.py:** Dado uma sequência de caracteres, avalia se um
autômato finito determinístico pode lê-lo. Os AFDs criados
são referentes à: *integer, float, string, identifier, keyword,
delimiter, operators e boolean*.

+ **lexicalAnalyser.py:** Dado um lexema, avalia qual afd o
reconhece, retornando a tupla (TOKEN, value).

+ **main.py:** Lê um código fonte, invocando o analisador
léxico e adquirindo todos os tokens do código.

Uma vez que todos os  arquivos encontram-se no mesmo diretório,
basta executar o arquivo "main.py":
 + Caso esteja em linux basta utilizar ``` python3 main.py ```
 + Caso esteja em windows basta clicar duas vezes no arquivo.
 + Independente do sistema operacional, verifique se o python 3.8.5
 (ou superior) está instalado.

Ao executar o arquivo "main.py", o programa realizará
a leitura do arquivo "code.txt" que deve estar no mesmo
diretório, e, ao ler todo arquivo, o analisador léxico faz
seu papel, retornando todos os tokens de todas palavras encontradas.

## Autores
   Vitor Acosta da Rosa						    (22.218.006-9)
	 Rubens de Araújo Rodrigues Mendes	(22.218.009-3)
	 Rafael Zacarias Palierini		      (22.218.030-9)
	 Andy Silva Barbosa			            (22.218.025-9)

