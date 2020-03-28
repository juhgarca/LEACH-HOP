# -*- coding: utf-8 -*-

import math
import numpy as np
import config as cf
import matplotlib.pyplot as plt


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
        nodes.append([i, 0.5, x, y, cf.distMax, 0, 0, 0, 0, 0, [], []])       # formato do nó: [id, bat, x, y, distMax, dch, count_dch, ddt, count_ddt, inter, buffer, cluster]
    
    return nodes


def distancia(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def gastoTx(bateria, distancia, tamPacote):
   return bateria-(0.00000005*tamPacote + 0.0000000001*tamPacote*(distancia*distancia))

def sendMsg(tipo, origem):
    if tipo == 'ANNOUNCE_CH':
        if origem[1] >= gastoTx(origem[1], origem[4], 300):
            #contaPacotesEnviados += 1
            meio.append([origem[0], 'bcast', 'Sou CH', 'config'])

def gastoRx(bateria, tamPacote):
   return bateria - 0.00000005 * tamPacote

def gastoAgg(bateria, numNchCluster):
    return bateria - (0.00001*(numNchCluster))

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
    for node in nodeCH[11]:
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

""" def setorizacao(lista,divisor):
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

    return lista """

def checaBateria(nodes):
    for n in nodes:
        if(n[1] <= 0):
            print("******* Nó", n[0], "descarregou (",n[1],")")
            nodes.remove(n)

def desvio_padrao(valores, media):
    soma = 0
    for valor in valores:
        soma += math.pow( (valor - media), 2)
    return math.sqrt( soma / float( len(valores) ) )

def grafico_clusters(CH, Round):

    chs_x, chs_y, X, Y = [], [], [], []
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'orange', 'purple', 'olive', 'gray', 'pink', 'black', 'yellow', 'paleturquoise', 'chocolate', 'lightgreen']
    for ch in CH:
        x, y = [], []
        chs_x.append(ch[2])
        chs_y.append(ch[3])
        for node in ch[11]:
            x.append(node[1])
            y.append(node[2])
        X.append(x)
        Y.append(y)
            
    for x, y, ch_x, ch_y, cor in zip(X, Y, chs_x, chs_y, colors):
        plt.scatter(x, y, color=cor)
        plt.scatter(ch_x, ch_y, color=cor, marker='^', label=colors)
    nome_grafico = "clusters_round_"+str(Round)+".png"
    plt.savefig("graficos/"+nome_grafico, format='png')
    plt.clf()

    
def definir_setores(area_cluster, qtd_setores, closest_node):
   
   tam_setor = area_cluster / qtd_setores
   setores = []
   for i in range(0, qtd_setores):
      setor_inicio = closest_node + tam_setor*i
      setor_fim = setor_inicio + tam_setor
      setores.append([setor_inicio, setor_fim])
   
   return setores


def setorizacao(cluster, qtd_setores):
   
   closest_node = 100   # trocar por valor mais genérico !!!!
   farthest_node = 0
   for nch in cluster:
      if nch[3] <= closest_node:
         closest_node = nch[3]
      if nch[3] >= farthest_node:
         farthest_node = nch[3]
   area_cluster = farthest_node - closest_node
   setores = definir_setores(area_cluster, qtd_setores, closest_node)

   for nch in cluster:
      i = 1
      for setor in setores:
         if nch[3] >= setor[0] and nch[3] <= setor[1]:
            nch[3] = i
         i += 1
