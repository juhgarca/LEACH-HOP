# -*- coding: utf-8 -*-
import random
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import config as cf
from energySource import harvest, prediction
from utils import gerarCenario, gastoRx, gastoTx, ajuste_alcance_nodeCH, checaBateria, contEncaminhamento, desvio_padrao, distancia, localizaObjetoCH, setorizacao, setorizacaoCH, verifica_eleitos


def selecao_CH(nodes, Round, Porcentagem):
  CH = []
  for k in nodes:
    rand = random.random()
    limiar = Porcentagem / (1.0 - Porcentagem * (Round % (1.0 / Porcentagem)))
    if(limiar > rand) and (k[6] != 1):
      k[6] = 1
      CH.append(k)
      nodes.remove(k)
  return CH

def calculaOCHP():
    for k in range(cf.kmin, cf.kmax+1):
        pi = k/cf.qtdNodes
        num_frames = cf.round_length*k/cf.qtdNodes
        cluster_len = cf.qtdNodes/k
        ener_agg = (5*10**-9 * cf.payload) * (cluster_len-1)         # Joules
        ener_setup = cf.ener_max_tx + ((cluster_len-1)*cf.ener_rx) + cf.ener_nch_tx    # Joules
        ener_ch_round = num_frames * (cf.ener_max_tx + (cluster_len-1)*cf.ener_rx + ener_agg) + ener_setup     # Joules
        ener_nch_round = num_frames * (cluster_len-1) * cf.ener_ch_tx      # Joules
        temp = k * (ener_ch_round + ener_nch_round)
    
        if(temp < Er_har and temp > Er_net):
            kopt = k
    
    pi = kopt/N
    Nf = Lr*kopt/N
    Lc = N/kopt
    Eagg = (5*10**-9 * payload) * (Lc-1)         # Joules
    Esetup = Emax_tx + ((Lc-1)*Erx) + Emax_tx    # Joules
    Er_ch = Nf * (Emax_tx + (Lc-1)*Erx + Eagg) + Esetup     # Joules
    Er_nch = Nf * (Lc-1) * Ts * Pch_tx                      # Joules
    Er_net = kopt * (Er_ch + Er_nch)


############################### Variables ################################
CH = []

arquivo = open('novo-arquivo.txt', 'w')
arquivo_bat = open('bateria.txt', 'a')

############################### Main ################################
# Realiza a variação de um dos cenários (Quem usar a variável: cenario)

distMax = distancia(0,0, cf.area,cf.area)

print("\n\nCENÁRIO: " + str(cf.qtdNodes) + ' nodes, '
                  + str(cf.qtdFrames) + ' frames, '
                  + str(cf.tamPacoteTransmissao) + ' bits, '
                  + str(int(cf.percentualCH*100)) + '%, '
                  + str(int(cf.qtdSetores)) + ' setores, '
                  + str(int(cf.area)) + ' m2')

# Altera entre os modos de operação do multi-hop
for modoOp in cf.modosHop:
    intraCluster = modoOp[0]
    interCluster = modoOp[1]

    framesSimulacao = []
    roundsSimulacao = []

    # Iteração para realizar várias iterações (total de simulações)
    for simulacao in range(cf.total_simulacoes):
        Round = 1
        totalRounds = 0
        nodes = gerarCenario(cf.qtdNodes,distMax)
        nosVivos = list()

        if(interCluster == 1):
            # CONFIGURAÇÕES INICIAIS (Setorização intercluster)
            # Trasmite as localizações à BS
            distanciasBS = []
            for k in nodes:
                dist = distancia(k[2],k[3],cf.BS[1],cf.BS[2])
                distanciasBS.append( dist )
                k[1] = gastoTx(k[1],dist,cf.tamPacoteConfig)
            # Recebe os setores da BS
            for k in nodes:
                k[9] = setorizacaoCH(distanciasBS,distanciasBS[k[0]-1],cf.qtdSetores)
                k[1] = gastoRx(k[1],cf.tamPacoteConfig)


        # INICIO DA EXECUÇÃO DA SIMULAÇÃO
        while(Round <= 5000 and len(nodes) != 0):
            

            
            
            
            

            # Energy Harvesting
            eh = harvest(Round)
            for n in nodes:
                n[1] += eh
                if n[1] >= 5.0:
                    n[1] = 5.0

            # Realiza seleção de CH
            CH = selecao_CH(nodes, Round, cf.percentualCH)

            # Conta os frames que foram executados
            totalFramesExecutados = 0

            # Execução após seleção
            if(len(CH) != 0):

                # TRANSMISSÃO  CH: Envio do Broadcast
                pacotesBroadcast = []
                for k in CH:
                    pacotesBroadcast.append( [k[0],k[2],k[3],0.0,k[9]] )
                    # Registro da BS para envio
                    k[7].append(cf.BS)
                    k[1] = gastoTx(k[1],k[4],cf.tamPacoteConfig)

                # RECEPÇÃO     CH: Chs recebem o broadcast dos outros CHs (os rádios estão ligados)
                for k in CH:
                    for node in pacotesBroadcast:
                        if(node[0] != k[0]):
                            k[7].append(node)
                    k[1] = gastoRx(k[1],cf.tamPacoteConfig)

                if(nodes != []):
                    # RECEPÇÃO    NCH: Recepção dos Pacotes de Bradcast
                    for k in nodes:
                        menorDistancia = k[4]
                        nodeMenorDistancia = []
                        # Escolha do CH (o mais próximo)
                        for nodesCH in pacotesBroadcast:
                            dist = distancia(k[2],k[3],nodesCH[1],nodesCH[2])
                            if(dist < menorDistancia):
                                menorDistancia = dist
                                nodeMenorDistancia = nodesCH
                        # Atualização dos valores
                        k[7] = [ nodeMenorDistancia ]
                        k[4] = menorDistancia
                        k[1] = gastoRx(k[1],cf.tamPacoteConfig)

                    # TRANSMISSÃO NCH: Envio de Pacotes Resposta
                    for k in nodes:
                        node = [k[0],k[2],k[3],k[4],0]
                        # localiza o CH escolhido na lista de CH e coloca seu node em ListCL do CH
                        for nodeCH in CH:
                            if(k[7][0][0] == nodeCH[0]):
                                nodeCH[8].append(node)
                        k[1] = gastoTx(k[1],k[4],cf.tamPacoteConfig)

                    # RECEPÇÃO     CH: Recepção de Pacotes de Resposta
                    for k in CH:
                        # Nodes atribuídos na função anterior
                        for l in range( len(k[8]) ):
                            k[1] = gastoRx(k[1],cf.tamPacoteConfig)

                    # TRANSMISSÃO  CH: Envio da Tabela TDMA
                    ajuste_alcance_nodeCH(CH)
                    clusters = []
                    for k in CH:
                        clusters.append( [k[0], setorizacao(k[8],cf.qtdSetores)] )
                        k[1] = gastoTx(k[1],k[4],cf.tamPacoteConfig)

                    # RECEPÇÃO    NCH: Recepção da Tabela TDMA
                    for k in nodes:
                        idCH = k[7][0][0]
                        # Localiza o cluster do CH
                        for clstr in clusters:
                            if(clstr[0] == idCH):
                                k[8] = clstr[1]
                        k[1] = gastoRx(k[1],cf.tamPacoteConfig)

                    # CONFIGURAÇÃO DE RADIO DOS CH PARA ALCANÇAR A BS
                    for k in CH:
                        k[4] = distancia(k[2],k[3], cf.BS[1],cf.BS[2])

                    # MULTI-HOP INTRACLUSTER
                    if(intraCluster == 1):
                        for k in nodes:
                            # Acho o setor dentro do clusters
                            setor = 0
                            for node in k[8]:
                                if(k[0] == node[0]):
                                    setor = node[4]
                                    break
                            # Achar node vizinho mais proximo
                            id = k[7][0][0]
                            menor = k[4]
                            for node in k[8]:
                                dist = distancia(k[2],k[3], node[1],node[2])
                                if(dist < menor and node[4] < setor):
                                    id = node[0]
                                    menor = dist
                            k[7] = [[id,0,0,menor,0]]
                            k[4] = menor

                    # MULTI-HOP INTERCLUSTER
                    if(interCluster == 1):
                        for k in CH:
                            menor = k[4]
                            for node in k[7]:
                                dist = distancia(k[2],k[3], node[1],node[2])
                                if(dist < menor and node[4] < k[9]):
                                    menor = dist
                                    k[4] = menor
                                    k[7] = [node]

                    # MAPEAMENTO DE ENCAMINHAMENTO NCH (Ids de destino dos nodes)
                    mapaEncaminhamento = []
                    for k in nodes:
                        mapaEncaminhamento.append( k[7][0][0] )

                    # FRAMES
                    for contFrame in range(cf.qtdFrames):
                        confirmaFrame = 0
                        # NCH: Transmite Pacote
                        for k in nodes:
                            if(intraCluster == 1):
                                # Gasto de agregação de dados
                                totalContEnc = contEncaminhamento(k[0], mapaEncaminhamento)
                                if(totalContEnc > 0):
                                    k[1] = k[1] - (0.000000005*cf.tamPacoteTransmissao*(totalContEnc + 1))
                            k[1] = gastoTx(k[1],k[4],cf.tamPacoteTransmissao)
                        # CH: Recebe Pacote
                        for k in CH:
                            for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                k[1] = gastoRx(k[1],cf.tamPacoteTransmissao)
                        # NCH: Recebe Pacote
                        if(intraCluster == 1):
                            for k in nodes:
                                for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                    k[1] = gastoRx(k[1],cf.tamPacoteTransmissao)
                        # CH: Envia Pacote para a BS
                        for k in CH:
                            # Gasto de agregação de dados
                            totalContEnc = contEncaminhamento(k[0], mapaEncaminhamento)
                            if(totalContEnc > 0):
                                k[1] = k[1] - (0.000000005*cf.tamPacoteTransmissao*(totalContEnc + 1))
                            node = k
                            idDestino = node[7][0][0]
                            while(idDestino != 0):
                                node[1] = gastoTx(node[1],node[4],cf.tamPacoteTransmissao)
                                node = localizaObjetoCH(idDestino,CH)
                                # Gasto Recepção do node destino
                                node[1] = gastoRx(node[1],cf.tamPacoteTransmissao)
                                idDestino = node[7][0][0]
                            node[1] = gastoTx(node[1],node[4],cf.tamPacoteTransmissao)
                            if(node[1] >= 0):
                                # Confirma que houve um envio a BS
                                confirmaFrame += 1

                        # Aumenta apenas se algum pacote foi enviado para a BS
                        if(confirmaFrame > 0):
                            totalFramesExecutados += 1

                # FECHAMENTO DO ROUND
                # Encerramento do Round
                bat = list()
                for k in CH:
                    nodes.append(k)
                for k in nodes:
                    k[4] = distMax
                    k[7] = []
                    k[8] = []
                    bat.append({k[0]: k[1]})
                
                #Exclui zerados
                checaBateria(nodes)

                nosVivos.append(len(nodes))
                resultados = 'Round: ' + str(Round) + ' #Nós Vivos: ' + str(len(nodes)) + '\n'
                #print('Simulação: ' + str(simulacao) + ' Round: ' + str(Round) + ' #Nós Vivos: ' + str(len(nodes)) + '\n')
                #arquivo.write(resultados)

                CH = []
                Round = Round + 1


                # FIM DE UM ROUND ##########
        arquivo_bat.write(str(Round) + str(bat) + "\n")
        df = pd.DataFrame(nosVivos, columns=['NosVivos'])
        print('Simulacao ' + str(simulacao+1) + ": " + str(Round))
        roundsSimulacao.append(Round-1)

        resultados = 'Simulacao: ' + str(simulacao) + ' Rounds: ' + str(Round-1) + ' Nos Vivos: ' + str(len(nodes)) + '\n'
        #arquivo.write(resultados)

        # FIM DE UMA SIMULAÇÃO ##########
    ############################### Estatísticas ################################
    media = sum(roundsSimulacao) / cf.total_simulacoes

    print('\nResultado do ' + str(modoOp[0]) + str(modoOp[1]) +"-LEACH-HOP:")
    print('Rounds: ', roundsSimulacao)
    print('Média: ' + str(media))
    print('Erro: ' + str(1.96*(desvio_padrao(roundsSimulacao, media) / math.sqrt(cf.total_simulacoes) )))
    arquivo.write("\nResultado do " + str(modoOp[0]) + str(modoOp[1]) +"-LEACH-HOP:\nRounds: "+ str(roundsSimulacao) +"\nMédia: " + str(media) +'\nErro: ' + str(1.96*(desvio_padrao(roundsSimulacao, media) / math.sqrt(cf.total_simulacoes) )))
    # FIM DE TODOS OS EXPERIMENTOS DE UM MODO DE OPERAÇÃO ##########

#plt.plot(df.index, df['NosVivos'])
#print("Last round:", max(df.index))

arquivo.close()
arquivo_bat.close()
