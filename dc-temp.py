# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:18:15 2019

@author: Juliana
"""
from energySource import prediction, harvest
import math
import numpy as np
from utils import generateNodes, calculaCHDC, calculaDTDC, gerarCenario, gastoRx, gastoTx, ajuste_alcance_nodeCH, checaBateria, contEncaminhamento, desvio_padrao, distancia, localizaObjetoCH, setorizacao, setorizacaoCH, verifica_eleitos
from config import *



###################################################################################################   

Round = 1
horizon_ctrl = 0
num_frames = 2
horizon = 4

nodes = generateNodes()
arquivo = open('novo-arquivo.txt', 'w')

while Round <= 20:           # <---------------------------------------------- Início da Simulação

    if horizon_ctrl == 0:
        harv_pwr = prediction(Round)
        #ener_r_har = qtdNodes*harv_pwr            # Joules
        ener_r_har = qtdNodes*energy*round_length*timeslot
        print(">>>>>>>>>>>>", ener_r_har)
        for n in nodes:
            n[4], n[5], k = calculaCHDC(ener_r_har)

    num_frames = round_length*k/qtdNodes
    cluster_len = qtdNodes/k
    ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
    ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_nch_tx    # Joules
    ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
    ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx      # Joules

    print(">>>>>>>>> INÍCIO DO ROUND", Round)
    arquivo.write("Round "+ str(Round) + ": ")

    eh = harvest(Round)
    for n in nodes:
        n[1] += eh
        if n[1] >= 5.0: n[1] = 5.0

    for n in nodes:
        if n[6] == 1:
            if n[2] >= ener_ch_round:
                print(n[0], " SOU CH")
                arquivo.write(str(n[0])+ " | ")
            else:
                n[6] = 0
                print(n[0], "recharging...")
    arquivo.write("\n")
    
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
        if n[6] < n[5]:
            n[6] +=1
        elif n[6] == n[5]:
            print("Reset count")
            n[6] = 1
    
    Round += 1
    