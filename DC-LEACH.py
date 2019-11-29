# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:18:15 2019

@author: Juliana
"""
from energySource import prediction, harvest
import math
import numpy as np
from utils import generateNodes, gerarCenario, gastoRx, gastoTx, ajuste_alcance_nodeCH, checaBateria, contEncaminhamento, desvio_padrao, distancia, localizaObjetoCH, setorizacao, setorizacaoCH, verifica_eleitos
from config import *


def calculaOCHP(ener_r_har):

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


###################################################################################################   

CH = []
Round = 1
horizon_ctrl = 0
qtdSetores = 2

modosHop = [[0,0]]

for modoOp in modosHop:
    intraCluster = modoOp[0]
    interCluster = modoOp[1]

    framesSimulacao = []  # <<<<<<<<<<< ATENTION!!!
    roundsSimulacao = []

    # Iteração para realizar várias iterações (total de simulações)
    for simulacao in range(total_simulacoes):
        Round = 1
        totalRounds = 0
        nodes = generateNodes()
        arquivo = open('novo-arquivo.txt', 'w')
        nosVivos = list()

        if(interCluster == 1):
            # CONFIGURAÇÕES INICIAIS (Setorização intercluster)
            # Trasmite as localizações à BS
            distanciasBS = []
            for n in nodes:
                dist = distancia(n[2], n[3], BS[1], BS[2])
                distanciasBS.append( dist )
                n[1] = gastoTx(n[1], dist, tamPacoteConfig)
            # Recebe os setores da BS
            for n in nodes:
                n[9] = setorizacaoCH(distanciasBS, distanciasBS[n[0]-1], qtdSetores)
                n[1] = gastoRx(n[1], tamPacoteConfig)


        while Round <= 20:  # <------------------------- Início da Simulação

            if horizon_ctrl == 0:   # <----------------- Controle do horizonte de predição
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

            eh = harvest(Round)     # <------------------- Captura de energia
            for n in nodes:
                n[1] += eh
                if n[1] >= 5.0: n[1] = 5.0

            for n in nodes:         # <------------------- "Seleção" de CH
                if n[6] == 1:
                    if n[2] >= ener_ch_round:
                        CH.append(n)
                        print(n[0], " SOU CH")
                        arquivo.write(str(n[0])+ " | ")
                    else:
                        n[6] = 0
                        print(n[0], "recharging...")
            arquivo.write("\n")

            # Conta os frames que foram executados
            totalFramesExecutados = 0

            if(len(CH) != 0):
            
            print("CHs se anunciam")
            # TRANSMISSÃO  CH: Envio do Broadcast
                pacotesBroadcast = []
                for k in CH:
                    pacotesBroadcast.append( [k[0],k[2],k[3],0.0,k[9]] )
                    # Registro da BS para envio
                    k[7].append(BS)
                    k[1] = gastoTx(k[1],k[4],tamPacoteConfig)
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
    