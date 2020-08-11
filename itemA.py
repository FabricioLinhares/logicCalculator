"""
TestaTautologia.py (Python)

Criado por Fabricio Linhares Rodrigues
Turma: COMP0410 - T03
Último teste: 20/01/2020
Versão Python: 3.7.3

Operadores
~ (Negação)
% (Bicondicional)
> (Condicional)
& (Conjunção)
| (Disjunção)
"""

from copy import deepcopy


def listar(tupla):
    """
    Tudo vindo de um input do usuário é retornado à programação como uma string, em forma de tupla.
    Como toda tupla é imutável, surge a necessidade de transformamos ela em uma lista, um objeto mutável.
    Essa função resolve esse problema, colocando cada elemento da tupla dentro de uma lista, sem espaçõs em branco

    :param tupla: expressão lógica a ser transformada em lista
    :return: tupla transformada em uma lista
    """
    lista = []
    global valorBool
    for elemento in tupla.replace(" ", ''):
        lista.append(elemento)
    listaaux = []
    listaaux2 = []
    while True:
        if len(lista) == 0:
            break
        elif lista[0] in '&|~>%()':
            listaaux.append([lista[0]])
            del lista[0]
        else:
            while True:
                if len(lista) == 0:
                    break
                elif lista[0] not in '&|~>%()':
                    listaaux2.append(lista[0])
                    del lista[0]
                else:
                    break
            listaaux.append(listaaux2)
            listaaux2 = []
    lista = []
    for elemento in listaaux:
        lista.append(''.join(elemento))
    return lista


def organizar(exp, lista=False, dentro=False):
    """
    Como a resolução do teste é feito apenas de forma bruta, isso é, testar cada uma das possibilidades. É necessário
    que, após um teste, a lista contendo a expressão lógica seja atualizada.
    Essa função também é responsável por transformar os elementos dentro de um parêntese em um único elemento, isto é,
    transformar tudo em apenas uma lista. Definindo assim a ordem de precedência mais alta.

    O valor True é necessário para toda chamada dessa função em que a expressão dada é na verdade uma lista que já foi
    organizada pela função anteriormente.
    A troca do argumento string para o valor booleano é feito justamente ao ser dado a variável lista como True. Ela é
    feita a partir de um dicionário, que, troca o nome da key por um valor lógico guardado dentro dela. Assim, só é
    necessário trocar esses valores e chamar a função organizar novamente para termos todas as possibilidades testadas.
    Assim é feito na função: "equivalente"

    :param exp: expressão a ser organizada
    :param lista: se é ou não uma lista a ser organizada mais uma vez
    :param dentro: identifica se a lista a ser organizada está dentro de outra
    :return: expressão organizada
    """
    if not lista:
        if dentro:
            for c in range(0, len(exp)):
                exp[c] = exp[c][0]
        for pos, elemento in enumerate(exp):
            if elemento == "(":
                q = 1
                posf = 0
                expl = [elemento]
                for c in range(pos + 1, len(exp)):
                    expl.append([exp[c]])
                    if exp[c] == '(':
                        q += 1
                    elif exp[c] == ')':
                        q -= 1
                    if q == 0:
                        posf = c + 1
                        break
                exp.insert(pos, expl)
                del exp[pos][0]
                del exp[pos][-1]
                for c in range(pos + 1, posf + 1):
                    del exp[pos + 1]
                if ["("] in exp[pos]:
                    exp[pos] = organizar(exp[pos], dentro=True)
            else:
                if exp[pos] not in '()&|>%~':
                    exp[pos] = [elemento]
                else:
                    exp[pos] = [exp[pos]]
    else:
        for pos, elemento in enumerate(exp):
            if len(elemento) > 1:
                organizar(elemento, True)
            else:
                if elemento[0] not in '()&|>%~':
                    exp[pos] = [valorBool[elemento[0]]]
    return exp


def inputfrase(frase):
    """
    Função que cria as keys para cada argumento da expressão lógica e começa o programa com a string arrumada pelas
    funções "listar" e "organizar".

    :param frase: Frase a ser colocada no input do usuário
    :return: retorna a expressão lógica dada pelo usuário, no formato utilizado pelo programa
    """
    expressao = input(frase)
    expressao = listar(expressao)
    for elemento in expressao:
        if elemento not in '()&|>%~':
            valorBool[elemento] = True
    return organizar(expressao)


def procurar(expressao, procura):
    """
    Uma sub função utilizada na função "precedente", com a finalidade de saber se ainda existe um operador a ser
    utilizado na expressão lógica

    :param expressao: expressão em que será procurado
    :param procura: elemento procurado
    :return: primeira posição do elemento procurado | = -1 se não existir
    """
    for pos, elemento in enumerate(expressao):
        if elemento[0] == procura:
            return pos
    return -1


def precedente(expressao):
    """
    Função que opera os argumentos, seguindo a seguinte ordem de precedência: ~, %, >, &, |. Ou seja, opera com todos
    os operadores de um tipo, para depois operar com outros, dando a ideia de prioridade de um operador sobre outro

    :param expressao: expressão lógica a ser operada
    :return: expressão com o valor lógico resultante
    """
    pos = procurar(expressao, "~")
    while pos != -1:
        expressao[pos][0] = not expressao[pos + 1][0]
        del expressao[pos + 1]
        pos = procurar(expressao, "~")
    pos = procurar(expressao, "%")
    while pos != -1:
        if expressao[pos - 1][0] == expressao[pos + 1][0]:
            expressao[pos - 1][0] = True
        else:
            expressao[pos - 1][0] = False
        del expressao[pos]
        del expressao[pos]
        pos = procurar(expressao, "%")
    pos = procurar(expressao, ">")
    while pos != -1:
        expressao[pos - 1][0] = not expressao[pos - 1][0] or expressao[pos + 1][0]
        del expressao[pos]
        del expressao[pos]
        pos = procurar(expressao, ">")
    pos = procurar(expressao, "&")
    while pos != -1:
        expressao[pos - 1] = [expressao[pos - 1][0] and expressao[pos + 1][0]]
        del expressao[pos]
        del expressao[pos]
        pos = procurar(expressao, "&")
    pos = procurar(expressao, "|")
    while pos != -1:
        expressao[pos - 1][0] = expressao[pos - 1][0] or expressao[pos + 1][0]
        del expressao[pos]
        del expressao[pos]
        pos = procurar(expressao, "|")
    return expressao


def operar(expressao):
    """
    Trabalha em conjunto com a função "precedente", só que esse é responsável por definir a prioridade dos parênteses
    mais internos sobre as outras operações. Assim como tirar o resultado da lista interna criado anteriormente, por
    seu conjunto dentro de parênteses.

    :param expressao: expressão a ser operada
    :return: função operada
    """
    for pos, elemento in enumerate(expressao):
        if len(elemento) > 1:
            expressao[pos] = operar(elemento)
            expressao[pos] = expressao[pos][0]
    expressao = precedente(expressao)
    return expressao


def tautologia(exp1):
    """
    Função que utiliza da "operar" para fazer testes repetitivos, apenas trocando os valores lógicos dos argumentos,
    para assim atingir todas as possibilidades.

    O número de vezes em que a função será rodada é definida por 2^n, sendo n o número de argumentos da expressão.
    O número de argumentos da expressão é definido pelo número de keys presente em nosso dicionário que foi preenchido
    na função "inputfrase"

    --------------------------------------------------------------------------------------------------------------------

    O programa defini a hora certa de permutar o valor lógico de um argumento quando a quantidade de repetições é
    divisível por 2^p, sendo p a posição dele em uma lista de argumentos que colocamos em uma variável composta no
    início dessa função.
    O exemplo a seguir demostra a acuracidade perfeita desse método.

    argumentos = [c, b, a]

    2^n = 2^3 = 2 . 2 . 2 = 8 (número de permutações diferentes)

    (quantidade de números a ser passados para o valor trocar)
    c: 2^p = 2^0 = 1
    b: 2^p = 2^1 = 2
    a: 2^p = 2^2 = 4

    Na tabela abaixo vemos que isso é válido para contemplar todas as possibilidades.

        1 2 3 4 5 6 7 8
    A | V V V V F F F F
    B | V V F F V V F F
    C | V F V F V F V F

    :param exp1: expressão 1 da possível tautologia
    """
    r1 = []
    wff = []
    global valorBool
    n = len(valorBool)
    for k in valorBool.keys():
        wff.append(k)
    for c in range(0, 2 ** n):
        exp1s = deepcopy(exp1)
        exp1s = organizar(exp1s, True)
        r1.append(operar(exp1s)[0])
        print(f'TESTE {c + 1}')
        print(f'Valores lógicos: {valorBool}')
        print(f'Resultado: {r1[c][0]}')
        print()
        for pos, elemento in enumerate(wff):
            if c % 2 ** pos == 0:
                valorBool[elemento] = not valorBool[elemento]
    r2 = []
    for elemento in r1:
        r2.append(elemento[0])
    return r2


# Programa principal:
valorBool = dict()
f1 = inputfrase('Digite a expressão lógica: ')
print()
tautologia(f1)
input('Aperte enter para finalizar...')
