from config import *
from energySource import prediction, harvest
from utils import generateNodes, gastoTx, gastoRx, gastoAgg, checaBateria, grafico_clusters
import numpy as np
import math

def calculaOCHP(ener_r_har):

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

    num_nch_rounds = horizon - (horizon/Dch)
    ener_rem_nch = (harv_pwr*horizon - ener_ch_round*(horizon-num_nch_rounds))/ num_nch_rounds
    
    pt1 = (ener_ch_tx*num_frames)/ener_rem_nch
    if (pt1 >= 1 and pt1 <= num_frames):
       Dene_dt = math.ceil(pt1)
    else:
        Dene_dt = 1
    
    pt2 = num_frames/(packet_rate*round_time)
    if (pt2 >= 1 and pt2 <= num_frames):
        Ddata_dt = math.floor(pt2)
    else:
        Ddata_dt = 1
    
    dtdc = max(Dene_dt, Ddata_dt)
    if (dtdc > num_frames):
        Ddt = 0
    elif (dtdc >= 1 and dtdc <= num_frames):
        Ddt = dtdc

    count = np.random.randint(1, Ddt+1)
    
    return Ddt, count


#############################################################################

Round = 1
horizon_ctrl = 0
nodes = generateNodes()

arquivo_setup = open('log_setup_phase.txt', 'w')
arquivo_transm = open('log_dt_phase', 'w')
arquivo_batt = open('bateria.csv', 'w')

arquivo_batt.write("CONSUMO ")
for n in nodes:
    arquivo_batt.write(str(n[0])+" ")

while Round <= 100:  # <------------------------- Início da Simulação

    CH = []
    sleep_nodes = []
    frame = 1

    arquivo_setup.write(">>> Round "+ str(Round))

    if horizon_ctrl == 0:   # <----------------- Controle do horizonte de predição
        #harv_pwr = prediction(Round)
        #ener_r_har = qtdNodes*harv_pwr            # Joules
        ener_r_har = harv_pwr = qtdNodes*energy*round_length*timeslot
        arquivo_setup.write(" - Ener_har "+ str(ener_r_har) + "\nCH-DC: ")
        
        for n in nodes: # <--------------------- Cálculo do Dch
            n[5], n[6], k = calculaCHDC(ener_r_har)
            arquivo_setup.write("["+ str(n[0]) +", "+ str(n[5]) +", " + str(n[6]) + "] ")

    num_frames = round_length*k/qtdNodes
    cluster_len = qtdNodes/k
    ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
    ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_nch_tx    # Joules
    ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
    ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx      # Joules

    print("\nNumero de frames:", num_frames, "\nk = ", k, "\nTamanho do round: ", round_length, "\n")

    # INÍCIO DO ROUND

    checaBateria(nodes)

    arquivo_batt.write("\nInicio_round_"+str(Round)+" ")

    # Nós recebem energia do ambiente
    #eh = harvest(Round)
    for n in nodes:
        n[1] += energy*round_length*timeslot
        #n[1] += eh
        if n[1] > 5.0: n[1] = 5.0
        arquivo_batt.write(str(n[1])+" ")

    # Seleção dos nós que serão CH no round
    for n in nodes:
        if n[6] == 1:
            if n[2] >= ener_ch_round:
                CH.append(n)
                nodes.remove(n)
                print(n[0], " SOU CH")
            else:
                n[6] = 0
                print(n[0], "recharging...")

    arquivo_setup.write("\nCHs ("+ str(len(CH))+ "): " + str(np.array(CH)[:,0])+ "\n")

    checaBateria(nodes)
    checaBateria(CH)

    if(len(CH) != 0):   # <------------ Controle pro caso de nenhum nó ser CH no round

        # NCHs calculam o Ddt
        for n in nodes:
            n[7], n[8] = calculaDTDC(n[5])
            if n[7] == 0:   # <---------- Se Ddt = 0, permanece em silêncio por todo o round
                sleep_nodes.append(n)
                nodes.remove(n)

        print("CHs se anunciam")
        # TRANSMISSÃO CH: Envio do Broadcast
        for ch in CH:   # <------------ Envio de cada CH
            ch[1] = gastoTx(ch[1], ch[4], tamPacoteConfig)
            for n in nodes: # <-------- NCHs recebem mensagens
                n[11].append( [ch[0], ch[2], ch[3]] )
                n[1] = gastoRx(n[1], tamPacoteConfig)
            for i in range(1, len(CH)): # <----------- Recebe mensagens dos outros CHs
                ch[1] = gastoRx(ch[1], tamPacoteConfig)

        # NCHs se associam a um CH
        for n in nodes:
            closer_dist = n[4]
            for ch in n[11]:
                dist = distancia(n[2], n[3], ch[1], ch[2])
                if dist <= closer_dist:
                    closer_dist = dist
                    closer_node = ch[0]
            n[4] = closer_dist      # <---------- Reduz o alcance do radio
            n[11] = closer_node     # <---------- CH escolhido

            # Envia mensagem para o CH escolhido
            n[1] = gastoTx(n[1], n[4], tamPacoteConfig)
            for ch in CH:
                if n[11] == ch[0]:
                    ch[11].append( [n[0], n[2], n[3]])  # <------ Guarda id e posição dos nós
                    ch[1] = gastoRx(ch[1], tamPacoteConfig)

        checaBateria(nodes)
        checaBateria(CH)
        
        #Gerar gráfico dos clusters
        grafico_clusters(CH, Round)

        # CHs reduzem o alcance do radio e enviam tabela TDMA
        for ch in CH:
            farther = 0
            for c in ch[11]:
                dist = distancia(ch[2], ch[3], c[1], c[2])
                if dist >= farther:
                    farther = dist
            ch[4] = farther
            ch[1] = gastoTx(ch[1], ch[4], tamPacoteConfig)  # <-------- Envio TDMA

        arquivo_setup.write("\nDT-DC: ")

        # NCHs recebem tabela TDMA
        for n in nodes:
            n[1] = gastoRx(n[1], tamPacoteConfig)
            arquivo_setup.write("["+ str(n[0]) +", "+ str(n[7]) +", " + str(n[8]) + "] ")

        checaBateria(nodes)
        checaBateria(CH)

        ### INÍCIO DA FASE DE TRANSMISSÃO DE DADOS ###
        arquivo_transm.write("Total frames: "+str(num_frames)+"\n")
        while frame <= num_frames:

            arquivo_transm.write("\nFrame "+str(frame)+": ")
            # NCHs enviam dados
            for n in nodes:
                if n[8] == 1:
                    n[1] = gastoTx(n[1], n[4], tamPktTx)
                    arquivo_transm.write(str(n[0])+"  ")

            # CHs recebem, agregam e enviam mensagens para base
            for ch in CH:
                for n in ch[11]:
                    ch[1] = gastoRx(ch[1], tamPktTx)
                ch[1] = gastoAgg(ch[1], len(ch[11]))
                ch[1] = gastoTx(ch[1], distMax, tamPktTx)

            checaBateria(nodes)
            checaBateria(CH)

            #Controle do contador do Ddt
            for n in nodes:
                if n[8] < n[7]:
                    n[8] +=1
                elif n[8] == n[7]:
                    #print("Reset ddt count")
                    n[8] = 1

            frame += 1

    # ENCERRAMENTO DO ROUND
    for ch in CH:
        nodes.append(ch)
    for node in sleep_nodes:
        nodes.append(node)
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
    
    arquivo_batt.write("\nFim_round_"+str(Round)+" ")
    for n in nodes:
        arquivo_batt.write(str(n[1])+ " ")

    arquivo_setup.write("\n\n")
    
    Round += 1
    # FIM DE UM ROUND ##########

print(len(nodes))