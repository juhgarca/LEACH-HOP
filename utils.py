# -*- coding: utf-8 -*-

import math
import numpy as np
from config import *


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
    for i in range(1,qtdNodes+1):
        x = round(np.random.uniform(0, area), 2)
        y = round(np.random.uniform(0, area), 2)
        nodes.append([i, 0.5, x, y, distMax, 0, 0, 0, 0])       # formato do nó: [id, bat, x, y, dch, count_dch, ddt, count_ddt]
    
    return nodes


def calculaOCHP(self, ener_r_har):

    print("Calculando porcentagem ótima de cluster heads")
    ener_r_net = 0
    kopt = 0
    for k in range(kmin, kmax+1):
        num_frames = round_length*k/qtdNodes
        cluster_len = qtdNodes/k
        ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
        ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_nch_tx    # Joules
        ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
        ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx      # Joules
        temp = k * (ener_ch_round + ener_nch_round)
    
        if (temp <= ener_r_har and temp > ener_r_net):
            kopt = k
            ener_r_net = temp
    
    return kopt


def calculaCHDC(ener_har):

    print("Calculando duty-cycle do cluster head")
    kopt = calculaOCHP(ener_har)
    pi = kopt/qtdNodes
    dcch = 1/pi
    if (dcch >= 1):
        Dch = math.ceil(dcch)
    else:
        Dch = 1
    
    count = np.random.randint(1, Dch+1)
        
    return Dch, count, kopt
        

def calculaDTDC(Dch):

    print("Calculando duty-cycle de transmissão de dados")
    num_nch_rounds = horizon - (horizon/Dch)
    ener_rem_nch = (harv_pwr*horizon - ener_ch_round*(horizon-num_nch_rounds))/ num_nch_rounds
    
    pt1 = (ener_ch_tx*num_frames)/ener_rem_nch
    print("\nPt1 =", pt1)
    if (pt1 >= 1 and pt1 <= num_frames):
       Dene_dt = math.ceil(pt1)
    else:
        Dene_dt = 1
    print("Dene_dt =", Dene_dt)
    
    pt2 = num_frames/(packet_rate*round_time)
    print("Pt2 =", pt2)
    if (pt2 >= 1 and pt2 <= num_frames):
        Ddata_dt = math.floor(pt2)
    else:
        Ddata_dt = 1
    print("Ddata_dt =", Ddata_dt)
    
    dtdc = max(Dene_dt, Ddata_dt)
    print("\nDT-DC =", dtdc)
    if (dtdc > num_frames):
        Ddt = 0
    elif (dtdc >= 1 and dtdc <= num_frames):
        Ddt = dtdc
    print("Ddt =", Ddt)
    
    return Ddt


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

def calculaOCHP():
    Er_har = cf.qtdNodes*n*Lr*Ts             # Joules
    Er_net = 0
    consumo = list()

    for k in range(kmin, kmax+1):
        pi = k/N
        Nf = Lr*k/N
        Lc = N/k
        Eagg = (5*10**-9 * payload) * (Lc-1)         # Joules
        Esetup = Emax_tx + ((Lc-1)*Erx) + Emax_tx    # Joules
        Er_ch = Nf * (Emax_tx + (Lc-1)*Erx + Eagg) + Esetup     # Joules
        Er_nch = Nf * (Lc-1) * Ts * Pch_tx                      # Joules
        temp = k * (Er_ch + Er_nch)
        consumo.append(temp)
        
        if(temp < Er_har and temp > Er_net):
            kopt = k
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    