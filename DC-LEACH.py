# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:18:15 2019

@author: Juliana
"""
from energySource import prediction, harvest
import math
import numpy as np
from utils import generateNodes, gerarCenario, gastoRx, gastoTx, ajuste_alcance_nodeCH, checaBateria, contEncaminhamento, desvio_padrao, distancia, localizaObjetoCH, setorizacao, setorizacaoCH
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

    count = np.random.randint(1, Dch+1)
    
    return Ddt, count


##################################################################################

CH = []
Round = 1
horizon_ctrl = 0
qtdSetores = 2
qtdFrames = 10

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
                
                for n in nodes: # <--------------------- Cálculo do Dch
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
                for ch in CH:
                    pacotesBroadcast.append([ch[0], ch[2], ch[3], 0.0, ch[9]])
                    # Registro da BS para envio
                    ch[10].append(BS)
                    ch[1] = gastoTx(ch[1],ch[4],tamPacoteConfig)

                # RECEPÇÃO CH: Chs recebem o broadcast dos outros CHs
                for ch in CH:
                    for node in pacotesBroadcast:
                        if(node[0] != ch[0]):
                            ch[10].append(node)
                    ch[1] = gastoRx(ch[1], tamPacoteConfig)

                if(nodes != []):
                    # RECEPÇÃO NCH: Recepção dos Pacotes de Bradcast
                    for n in nodes:
                        menorDistancia = n[4]
                        nodeMenorDistancia = []
                        # Escolha do CH (o mais próximo)
                        for nodeCH in pacotesBroadcast:
                            dist = distancia(n[2], n[3], nodeCH[1], nodeCH[2])
                            if(dist < menorDistancia):
                                menorDistancia = dist
                                nodeMenorDistancia = nodeCH
                        # Atualização dos valores
                        n[10] = [ nodeMenorDistancia ]
                        n[4] = menorDistancia
                        n[1] = gastoRx(n[1], tamPacoteConfig)
                
                    print("NCHs se associam")
                    # TRANSMISSÃO NCH: Envio de Pacotes Resposta
                    for n in nodes:
                        node = [n[0], n[2], n[3], n[4], 0]
                        # localiza o CH escolhido na lista de CH e coloca seu node em ListCL do CH
                        for nodeCH in CH:
                            if(n[10][0][0] == nodeCH[0]):
                                nodeCH[11].append(node)
                        n[1] = gastoTx(n[1], n[4], tamPacoteConfig)

                    # RECEPÇÃO CH: Recepção de Pacotes de Resposta
                    for ch in CH:
                        # Nodes atribuídos na função anterior
                        for l in range(len(ch[11])):
                            ch[1] = gastoRx(ch[1], tamPacoteConfig)

                    print("Chs enviam TDMA")
                    # TRANSMISSÃO CH: Envio da Tabela TDMA
                    ajuste_alcance_nodeCH(CH)
                    clusters = []
                    for ch in CH:
                        clusters.append( [ch[0], setorizacao(ch[11], qtdSetores)] )
                        ch[1] = gastoTx(ch[1],ch[4], tamPacoteConfig)

                    # RECEPÇÃO NCH: Recepção da Tabela TDMA
                    for n in nodes:
                        idCH = n[10][0][0]
                        # Localiza o cluster do CH
                        for ch in clusters:
                            if(ch[0] == idCH):
                                n[11] = ch[1]
                        n[1] = gastoRx(n[1], tamPacoteConfig)

                    # CONFIGURAÇÃO DE RADIO DOS CH PARA ALCANÇAR A BS
                    for ch in CH:
                        ch[4] = distancia(ch[2], ch[3], BS[1], BS[2])

                    # MULTI-HOP INTRACLUSTER
                    if(intraCluster == 1):
                        for n in nodes:
                            # Acho o setor dentro do clusters
                            setor = 0
                            for node in n[11]:
                                if(n[0] == node[0]):
                                    setor = node[4]
                                    break
                            # Achar node vizinho mais proximo
                            id = n[10][0][0]
                            menor = n[4]
                            for node in n[11]:
                                dist = distancia(n[2], n[3], node[1], node[2])
                                if(dist < menor and node[4] < setor):
                                    id = node[0]
                                    menor = dist
                            k[10] = [[id, 0, 0, menor, 0]]
                            k[4] = menor

                    # MULTI-HOP INTERCLUSTER
                    if(interCluster == 1):
                        for ch in CH:
                            menor = ch[4]
                            for node in ch[10]:
                                dist = distancia(ch[2], ch[3], node[1], node[2])
                                if(dist < menor and node[4] < ch[9]):
                                    menor = dist
                                    ch[4] = menor
                                    ch[7] = [node]

                    # MAPEAMENTO DE ENCAMINHAMENTO NCH (Ids de destino dos nodes)
                    mapaEncaminhamento = []
                    for n in nodes:
                        mapaEncaminhamento.append( n[10][0][0] )

                    print("NCHs calculaDTDC()\n")
                    for n in nodes: # <--------------------- Cálculo do Ddt
                        n[7], n[8] = calculaDTDC(n[5])
                   
                    # FRAMES
                    for frame in range(qtdFrames):
                        print("--> Frame", frame)
                        confirmaFrame = 0

                        print("     NCHs enviam dados para CHs")
                        # NCH: Transmite Pacote
                        for n in nodes:
                            if n[8] == 1:
                                if n[2] >= ener_nch_round:
                                    print(n[0], "---------- sending data...")
                                    if(intraCluster == 1):
                                        # Gasto de agregação de dados
                                        totalContEnc = contEncaminhamento(n[0], mapaEncaminhamento)
                                        if(totalContEnc > 0):
                                            n[1] = n[1] - (0.000000005*payload*(totalContEnc + 1))
                                    n[1] = gastoTx(n[1], n[4], payload)
                                else:
                                    n[8] = 0
                                    print(n[0], "---------- can't send data now")

                    
                        # CH: Recebe Pacote
                        for ch in CH:
                            for l in range( contEncaminhamento(ch[0], mapaEncaminhamento) ):
                                ch[1] = gastoRx(ch[1], payload)
                        
                        # NCH: Recebe Pacote  # <--------------- Intra-cluster !!!! não deveria ser antes do CH receber??
                        if(intraCluster == 1):
                            for n in nodes:
                                for l in range( contEncaminhamento(n[0], mapaEncaminhamento) ):
                                    n[1] = gastoRx(n[1], payload)
                        
                        print("     CHs agregam dados")
                        print("     CHs enviam dados para BS")
                        # CH: Envia Pacote para a BS
                        for ch in CH:
                            # Gasto de agregação de dados
                            totalContEnc = contEncaminhamento(ch[0], mapaEncaminhamento)
                            if(totalContEnc > 0):
                                ch[1] = ch[1] - (0.000000005*payload*(totalContEnc + 1))
                            node = ch
                            idDestino = node[10][0][0]
                            print("==========> ", idDestino)
                            while(idDestino != 0):
                                print("infinite loop??")
                                node[1] = gastoTx(node[1], node[4], payload)
                                node = localizaObjetoCH(idDestino, CH)
                                # Gasto Recepção do node destino
                                node[1] = gastoRx(node[1], payload)
                                idDestino = node[10][0][0]
                                print("==========>>> ", idDestino)
                                break
                            node[1] = gastoTx(node[1], node[4], payload)
                            if(node[1] >= 0):   # <----------------------- Que é que tem a ver?!
                                # Confirma que houve um envio a BS
                                confirmaFrame += 1

                        #Controle do contador do Ddt
                        for n in nodes:
                            if n[8] < n[7]:
                                n[8] +=1
                            elif n[8] == n[7]:
                                print("Reset count")
                                n[8] = 1

                        # Aumenta apenas se algum pacote foi enviado para a BS
                        if(confirmaFrame > 0):
                            totalFramesExecutados += 1
                        
            # Encerramento do Round
            bat = list()
            for ch in CH:
                nodes.append(ch)
            for n in nodes:  # <--------------- Reseta valores
                n[4] = distMax
                n[10] = []
                n[11] = []
                bat.append({n[0]: n[1]})

            #Exclui zerados
            checaBateria(nodes)

            nosVivos.append(len(nodes))
            resultados = 'Round: ' + str(Round) + ' #Nós Vivos: ' + str(len(nodes)) + '\n'
            #print('Simulação: ' + str(simulacao) + ' Round: ' + str(Round) + ' #Nós Vivos: ' + str(len(nodes)) + '\n')
            arquivo.write(resultados)
            
            horizon_ctrl += 1
            if horizon_ctrl == horizon: horizon_ctrl = 0

            CH = []
            print("Round", Round, "Nós vivos: ", len(nodes))
            
            print(">>>>>>>>> FIM DO ROUND", Round, "\n")
            
            #Controle do contador do Dch
            for n in nodes:
                if n[6] < n[5]:
                    n[6] +=1
                elif n[6] == n[5]:
                    print("Reset count")
                    n[6] = 1
            
            Round += 1
            # FIM DE UM ROUND ##########

        #arquivo_bat.write(str(Round) + str(bat) + "\n")
        #df = pd.DataFrame(nosVivos, columns=['NosVivos'])
        #print('Simulacao ' + str(simulacao+1) + ": " + str(Round))
        #roundsSimulacao.append(Round-1)

        #resultados = 'Simulacao: ' + str(simulacao) + ' Rounds: ' + str(Round-1) + ' Nos Vivos: ' + str(len(nodes)) + '\n'
        #arquivo.write(resultados)

        # Estatísticas

        arquivo.close()
        #arquivo_bat.close()