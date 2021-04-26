"""
    
    Este código possuí uma solução genérica através do uso de dicionários
    para a tomada de decisão sobre qual é o próximo estado do automato.

    Cada item do exercício possuí um dicionário.

    |DICIONÁRIOS|:
    a) a_dict
        Expressão Regular: 010

    b) b_dict
        Expressão Regular: 0*|1*

    c) c_dict
        Expressão Regular: 0*11+

    
    Descrição:

    Implementação de autômatos finitos determinísticos capazes
    de reconhecer expressões regulares/cadeias.

    O funcionamento baseia-se em dicionários encadeados:
    
    {
    Estado_0 : { "SimboloAceito": Prox_estado, ... "SimboloAceito": Prox_estado },
        .               .            .         ...        .            .         ,
    Estado_i : {        .            .         ...        .            .        },
        .               .            .         ...        .            .         ,
    Estado_f : {" ": -1}
    }

    -> Perceba que, o SimboloAceito deve ser uma string.
    
    -> O próximo estado e o estado atual (representado por
    Prox_estado e Estado_i) são inteiros.
    
    -> O possível estado final sempre terá a flag (key) " "
    para indicar o reconhecimento da cadeia. Note que,
    em algumas sequências, a flag está entre os n simbolos
    aceitos para aquele estado (e.g. 0*|1*, 0*11+).

    --- Operações -------------------------------------------------
    -> A operação * corresponde à: "O atual caractere (ou simbolo)
    pode repetir 0 ou n vezes".

    -> A operação | corresponde à operação de OR (OU).

    -> A operação + corresponde à: "O atual caractere (ou simbolo)
    pode repetir 1 ou n vezes".


    Autor: Vitor Acosta da Rosa
"""


# Dicionário da sequência 010
a_dict = {
        0:{"0":1},
        1:{"1":2},
        2:{"0":3},
        3:{" ":-1}
        }

# Dicionário da sequência 0*|1*
b_dict = {
        0:{"0":1, "1":2, " ":-1},
        1:{"0":1," ":-1},
        2:{"1":2," ":-1}
        }

# Dicionário da sequência 0*11+
c_dict = {
        0:{"0":0, "1":1},
        1:{"1":2},
        2:{"1":2, " ":-1}
        }

alphabet = ["0","1"]

def recognize(transition_table, initial_state, sequence, min_len, alphabet):
    if len(sequence) < min_len:
        return "Rejected because the string is less than acceptable according to the regular expression."
    else:
        for letter in sequence:
            if letter not in alphabet:
                return "Rejected because it contains a character not contained in the alphabet."
    """
    Retorna se a sequência é aceita, dada a tabela de transição.

    Parameters
    ----------
    transition_table: Dict
        Dicionário encadeado com o estado atual, simbolos aceitos
        e próximos estados.
    initial_state: Int
        Estado inicial, por convenção dos autores, utilize 0.
    sequence: str
        Sequência a ser avaliada levando em consideração a tabela
        de transição dada.
    """

    current_state = initial_state
    for char in sequence:
        print(f"Entry symbol: {char}",end=" - ")
        if char not in transition_table[current_state].keys():
            print(f" Invalid symbol  - ")
            return "Rejected because it does not comply with the regular expression rule"

        else: # Muda de estado

            print(f"  Valid symbol  ",end=" - ")
            current_state = transition_table[current_state][char]  
            print(f"Next state: {current_state}")

    # If utilizado para sequências que contam com a Kleene star
    # (operador *) o qual pode não contar com o símbolo em questão.
    # Perceba que " " é uma flag definida no dicionário, e
    # representa um possível estado final.
    if " " in transition_table[current_state].keys():
        return True

    return "Rejected because it does not comply with the regular expression rule"

print("Which expression use?\n option | expression\n    1   | 010\n    2   | 0*|1*\n    3   | 0*11+\n\n-->Option:")
op = int(input())
s = str(input("Insert sequence: "))

if op == 1:
    print(recognize(a_dict, 0, s, 3, alphabet))
elif op == 2:
    print(recognize(b_dict, 0, s, 0, alphabet))
elif op == 3:
    print(recognize(c_dict, 0, s, 2, alphabet))
else:
    print("Invalid option\nClosing program...")