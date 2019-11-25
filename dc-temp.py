# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:18:15 2019

@author: Juliana
"""
from energySource import prediction, harvest
import math
import numpy as np


qtdNodes = 100
kmin = 5
kmax = 20
kopt = kmin
timeslot = 0.1    # tempo de slot (segundo)
round_length = 500    # tamanho do round (timeslots)
round_time = round_length * timeslot    # tempo do round (segundos)
horizon = 10   # horizonte de predição (rounds)
payload = 2000
area = 100

cluster_len = qtdNodes/kopt

pwr_max_tx = 0.0801    # W
pwr_rx = 0.0222    # W
packet_rate = 0.5     # pacotes/s

ener_max_tx = pwr_max_tx * timeslot
ener_rx = pwr_rx * timeslot
ener_nch_tx = 0.0444    # W (valor aproximado para a primeira vez, já que não tem como calcular)
ener_agg = 0.00001*(cluster_len-1)
ener_setup = ener_max_tx + (cluster_len-1)*ener_rx + ener_nch_tx
ener_ch_tx = ener_nch_tx    # W (valor aproximado para a primeira vez, já que não tem como calcular)

def generateNodes():
    print("Gerando nós")
    nodes = []
    for i in range(1,qtdNodes+1):
        x = round(np.random.uniform(0, area), 2)
        y = round(np.random.uniform(0, area), 2)
        nodes.append([i, 0.5, x, y, 0, 0, 0, 0])       # formato do nó: [id, bat, x, y, dch, count_dch, ddt, count_ddt]
    
    return nodes


def calculaOCHP():

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
    
        if(temp <= ener_r_har and temp > ener_r_net):
            kopt = k
            ener_r_net = temp
    
    return kopt

def calculaCHDC():

    print("Calculando duty-cycle do cluster head")
    kopt = calculaOCHP()
    pi = kopt/qtdNodes
    dcch = 1/pi
    if (dcch >= 1):
        Dch = math.ceil(dcch)
    else:
        Dch = 1
    
    count = np.random.randint(1, Dch+1)
        
    return Dch, count
        
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


""" pi = kopt/qtdNodes
num_frames = round_length*kopt/qtdNodes
cluster_len = qtdNodes/kopt
ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_max_tx    # Joules
ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx                      # Joules
ener_r_net = kopt * (ener_ch_round + ener_nch_round) """


# Início da simulação    

Round = 1
horizon_ctrl = 0
num_frames = 2
horizon = 4

nodes = generateNodes()
arquivo = open('novo-arquivo.txt', 'w')

while Round <= 20:

    if horizon_ctrl == 0:
        harv_pwr = prediction(Round)
        ener_r_har = qtdNodes*harv_pwr            # Joules
        for n in nodes:
            n[4], n[5] = calculaCHDC()

    print(">>>>>>>>> INÍCIO DO ROUND", Round)
    arquivo.write("Round ", Round, ":  ")

    eh = harvest(Round)
    for n in nodes:
        n[1] += eh
        if n[1] >= 5.0: n[1] = 5.0

    for n in nodes:
        if n[5] == 1:
            print(n[5], " SOU CH")
            arquivo.write(n[0], " | ")

    
    print("CHs se anunciam")
    print("NCHs se associam")
    print("Chs enviam TDMA")
    print("NCHs calculaDTDC()\n")

    frames_ctrl = 1
    while frames_ctrl <= num_frames:
        print("--> Frame", frames_ctrl)
        print("     NCHs enviam dados para CHs")
        print("     CHs agregam dados")
        print("     CHs enviam dados para BS")

        frames_ctrl += 1
    
    horizon_ctrl += 1
    if horizon_ctrl == horizon: horizon_ctrl = 0
    
    print(">>>>>>>>> FIM DO ROUND", Round, "\n")
    
    #Controle do contador do Dch
    for n in nodes:
        if n[5] < Dch:
            n[5] +=1
        elif n[5] == Dch:
            print("Reset count")
            n[5] = 1
    
    Round += 1
    