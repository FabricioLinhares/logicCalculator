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


def listar(tupla):
    """
    Tudo vindo de um input do usuário é retornado à programação como uma string, em forma de tupla.
    Como toda tupla é imutável, surge a necessidade de transformamos ela em uma lista, um objeto mutável.
    Essa função resolve esse problema, colocando cada elemento da tupla dentro de uma lista, sem espaçõs em branco

    :param tupla: expressão lógica a ser transformada em lista
    :return: tupla transformada em uma lista
    """
    lista = []
    for elemento in tupla.replace(" ", '').replace("'", ''):
        lista.append(elemento)
    listaaux = []
    listaaux2 = []
    while True:
        if len(lista) == 0:
            break
        elif lista[0] in '[]':
            listaaux.append([lista[0]])
            del lista[0]
        elif lista[0] == ',':
            del lista[0]
        else:
            while True:
                if len(lista) == 0:
                    break
                elif lista[0] not in ",]":
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
    Função responsável por adaptar o input do usuário, que é em formato de string para uma lista de cláusulas,
    assim como aceita pela função "resolução".

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
            if elemento == "[":
                q = 1
                posf = 0
                expl = [elemento]
                for c in range(pos + 1, len(exp)):
                    expl.append([exp[c]])
                    if exp[c] == '[':
                        q += 1
                    elif exp[c] == ']':
                        q -= 1
                    if q == 0:
                        posf = c + 1
                        break
                exp.insert(pos, expl)
                del exp[pos][0]
                del exp[pos][-1]
                for c in range(pos + 1, posf + 1):
                    del exp[pos + 1]
                if ["["] in exp[pos]:
                    exp[pos] = organizar(exp[pos], dentro=True)
            else:
                if exp[pos] not in '[]':
                    exp[pos] = [elemento]
                else:
                    exp[pos] = [exp[pos]]
    else:
        for pos, elemento in enumerate(exp):
            if len(elemento) > 1:
                organizar(elemento, True)
            else:
                if elemento[0] not in '[]':
                    exp[pos] = [valorBool[elemento[0]]]
    expaux = []
    expaux2 = []
    for elemento in exp:
        for e in elemento:
            expaux.append(e[0])
        expaux2.append([expaux])
        expaux = []
    return expaux2


def oposto(a):
    """
    Faz a negação do literal de acordo com os moldes do algoritmo.

    :param a: literal
    :return: negação do literal
    """
    if a[0] == '~':
        aux = a[1:]
    else:
        aux = ''.join(['~', a])
    return aux


def combinar(l1, l2):
    """
    Função responsável por combinar duas cláusulas.

    :param l1: cláusula 1
    :param l2: cláusula 2
    :return: combinação das cláusulas | retorna -1 caso ela seja equivalente a True
    """
    l3 = []
    aux = []
    while len(l1) > 0:
        if l1[0][0] == '~':
            if oposto(l1[0][0:]) in l2:
                aux.append(oposto(l1[0][0:]))
                del l1[0]
            else:
                l3.append(l1[0])
                del l1[0]
        elif oposto(l1[0][0:]) in l2:
            aux.append(l1[0][0:])
            del l1[0]
        else:
            l3.append(l1[0])
            del l1[0]
    while len(l2) > 0:
        if l2[0] not in l3 and oposto(l2[0][0:]) not in l3 and oposto(l2[0][0:]) not in aux and l2[0][0:] not in aux:
            l3.append(l2[0])
            del l2[0]
        else:
            del l2[0]
    l3.sort()
    if len(aux) > 1:
        return -1
    return l3


def resolucao(l):
    """
    Aplica o metodo da resolução em uma lista de cláusulas.

    :param l: lista de cláusulas
    :return: Valor booleano para formula satisfatível ou não
    """
    l1 = []
    for elemento in l[0:]:
        aux = sorted(elemento)
        l1.append(aux)
    l2 = []
    for pos, elemento in enumerate(l1):
        if len(l1[pos + 1:]) == 0:
            break
        for e in l1[pos + 1:]:
            aux = combinar(elemento[0:], e[0:])
            if aux != -1:
                l2.append(aux)
    if [] in l2:
        return False
    while len(l2) > 0:
        for elemento in l1:
            aux = combinar(elemento[0:], l2[0][0:])
            if aux not in l1 and aux != -1:
                l2.append(aux)
            elif not aux:
                return False
        l1.append(l2[0])
        del l2[0]
    return True


# Programa Principal
f1 = organizar(listar(input('Digite a lista de cláusulas: ')))
f1 = f1[0][0]
print()
if resolucao(f1):
    print('A formula é satisfatível')
else:
    print('A formula não é satistatível')
print()
input('Aperte enter para finalizar...')
