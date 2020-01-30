from config import *
from energySource import prediction, harvest
from utils import generateNodes, gastoTx, gastoRx
import numpy as np
import math

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


#############################################################################

Round = 1
horizon_ctrl = 0
nodes = generateNodes()

arquivo_setup = open('log_setup_phase.txt', 'w')

while Round <= 2:  # <------------------------- Início da Simulação

    CH = []

    if horizon_ctrl == 0:   # <----------------- Controle do horizonte de predição
        harv_pwr = prediction(Round)
        #ener_r_har = qtdNodes*harv_pwr            # Joules
        ener_r_har = qtdNodes*energy*round_length*timeslot
        arquivo_setup.write("Round "+ str(Round) + " - Ener_har "+ str(ener_r_har) + ": ")
        
        for n in nodes: # <--------------------- Cálculo do Dch
            n[5], n[6], k = calculaCHDC(ener_r_har)
            arquivo_setup.write("["+ str(n[0]) +", "+ str(n[5]) +", " + str(n[6]) + "] ")

    num_frames = round_length*k/qtdNodes
    cluster_len = qtdNodes/k
    ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
    ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_nch_tx    # Joules
    ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
    ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx      # Joules

    # INÍCIO DO ROUND

    for n in nodes:         # <------------------- "Seleção" de CH
        if n[6] == 1:
            if n[2] >= ener_ch_round:
                CH.append(n)
                nodes.remove(n)
                print(n[0], " SOU CH")
            else:
                n[6] = 0
                print(n[0], "recharging...")
    arquivo_setup.write("\nCHs ("+ str(len(CH))+ "): " + str(np.array(CH)[:,0])+ "\n")

    if(len(CH) != 0):   # <------------ Controle pro caso de nenhum nó ser CH no round

        print("CHs se anunciam")
        # TRANSMISSÃO CH: Envio do Broadcast
        for ch in CH:   # <------------ Envio de cada CH
            ch[1] = gastoTx(ch[1], ch[4], tamPacoteConfig)
            for n in nodes: # <-------- NCHs recebem mensagens
                n[11].append( [ch[0], ch[2], ch[3]] )
                n[1] = gastoRx(n[1], tamPacoteConfig)
                arquivo_setup.write("\n\n"+ str(n[0]) + ">>"+ n[11]+"\n")
            for i in range(1, len(CH)): # <----------- Recebe mensagens dos outros CHs
                ch[1] = gastoRx(ch[1], tamPacoteConfig)

        # NCHs se associam a um CH
        


    # ENCERRAMENTO DO ROUND
    for ch in CH:
        nodes.append(ch)
    for n in nodes:  # <--------------- Reseta valores
        n[4] = distMax
        n[10] = []
        n[11] = []

    horizon_ctrl += 1
    if horizon_ctrl == horizon: horizon_ctrl = 0

    #Controle do contador do Dch
    for n in nodes:
        if n[6] < n[5]:
            n[6] +=1
        elif n[6] == n[5]:
            print("Reset count")
            n[6] = 1
    
    Round += 1
    # FIM DE UM ROUND ##########



