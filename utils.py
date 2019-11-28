# -*- coding: utf-8 -*-

import math
import numpy as np
import config as cf


def gerarCenario(qtdNodes,distMax):
    nodes = []
    for i in range(1, qtdNodes+1):
        x = round(np.random.uniform(0, cf.area), 2)
        y = round(np.random.uniform(0, cf.area), 2)
        nodes.append([i, cf.bat_init, x, y, distMax, 0, 0, [], [], 0])
    return nodes


def generateNodes():
    print("Gerando nós")
    nodes = []
    for i in range(1,cf.qtdNodes+1):
        x = round(np.random.uniform(0, cf.area), 2)
        y = round(np.random.uniform(0, cf.area), 2)
        nodes.append([i, 0.5, x, y, cf.distMax, 0, 0, 0, 0, 0])       # formato do nó: [id, bat, x, y, dch, count_dch, ddt, count_ddt]
    
    return nodes


def distancia(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def gastoTx(bateria, distancia, tamPacote):
   return bateria-(0.00000005*tamPacote + 0.0000000001*tamPacote*(distancia*distancia))

def gastoRx(bateria, tamPacote):
   return bateria - 0.00000005 * tamPacote

def contEncaminhamento(id,listaID):
    cont = 0
    for k in listaID:
        if(k == id):
            cont += 1
    return cont

def localizaObjetoCH(id, CH):
    for k in CH:
        if (k[0] == id):
            return k

def verifica_eleitos(nodes):
  total = 0
  for k in nodes:
    total += k[6]
  if(total == len(nodes)):
    return True
  return False

def ajuste_alcance_nodeCH(CH):
  for nodeCH in CH:
    maior = 0
    # Verifica os elementos do cluster
    for node in nodeCH[8]:
      if(maior < node[3]):
        maior = node[3]
    # Escolhe a maior distância e configura o rádio
    nodeCH[4] = maior

def setorizacaoCH(listaDistancias,distancia,divisor):
    # Calculo entre o menor e o maior
    menor = min(listaDistancias)
    maior = max(listaDistancias)

    valor = (maior - menor) / divisor

    if(distancia <= menor + 1*valor):
        return 1
    elif(distancia <= menor + 2*valor):
        return 2
    elif(distancia <= menor + 3*valor):
        return 3
    elif(distancia <= menor + 4*valor):
        return 4
    elif(distancia <= menor + 5*valor):
        return 5
    elif(distancia <= menor + 6*valor):
        return 6
    elif(distancia <= menor + 7*valor):
        return 7
    else:
        return 8

def setorizacao(lista,divisor):
    if(lista != []):
        # Vetor das Distâncias
        ordenado = []
        for k in lista:
            ordenado.append(k[3])
        # Calculo entre o menor e o maior
        ordenado.sort()
        valor = (ordenado[-1] - ordenado[0]) / divisor
        # Setorização
        for k in lista:
            if(k[3] <= ordenado[0] + 1*valor):
                k[4] = 1
            elif(k[3] <= ordenado[0] + 2*valor):
                k[4] = 2
            elif(k[3] <= ordenado[0] + 3*valor):
                k[4] = 3
            elif(k[3] <= ordenado[0] + 4*valor):
                k[4] = 4
            elif(k[3] <= ordenado[0] + 5*valor):
                k[4] = 5
            elif(k[3] <= ordenado[0] + 6*valor):
                k[4] = 6
            elif(k[3] <= ordenado[0] + 7*valor):
                k[4] = 7
            else:
                k[4] = 8

    return lista

def checaBateria(nodes):
    for k in nodes:
        if(k[1] <= 0):
            nodes.remove(k)

def desvio_padrao(valores, media):
    soma = 0
    for valor in valores:
        soma += math.pow( (valor - media), 2)
    return math.sqrt( soma / float( len(valores) ) )

