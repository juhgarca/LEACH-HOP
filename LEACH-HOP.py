# -*- coding: utf-8 -*-
import random
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from energySource import irradiacao, harvest
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


############################### Variables ################################
CH = []
tamPacoteConfig = 300

#modosHop = [[0,0],[0,1],[1,0],[1,1]]
modosHop = [[0,0]]

list_qtdNodes = [100]
list_qtdFrames = [10]
list_tamPacoteTransmissao = [2000]
list_percentualCH = [0.05]
list_qtdSetores = [4]
list_area = [100]

total_simulacoes = 1
arquivo = open('novo-arquivo.txt', 'w')
arquivo_bat = open('bateria.txt', 'a')

############################### Main ################################
# Realiza a variação de um dos cenários (Quem usar a variável: cenario)

qtdNodes =                         list_qtdNodes[0]
qtdFrames =                       list_qtdFrames[0]
tamPacoteTransmissao = list_tamPacoteTransmissao[0]
percentualCH =                 list_percentualCH[0]
qtdSetores =                     list_qtdSetores[0]
area =                                 list_area[0]

distMax = distancia(0,0, area,area)
BS = [0, area+25.0, area/2, 0.0, 0]

print("\n\nCENÁRIO: " + str(qtdNodes) + ' nodes, '
                  + str(qtdFrames) + ' frames, '
                  + str(tamPacoteTransmissao) + ' bits, '
                  + str(int(percentualCH*100)) + '%, '
                  + str(int(qtdSetores)) + ' setores, '
                  + str(int(area)) + ' m2')

# Altera entre os modos de operação do multi-hop
for modoOp in modosHop:
    intraCluster = modoOp[0]
    interCluster = modoOp[1]

    framesSimulacao = []
    roundsSimulacao = []

    # Iteração para realizar várias iterações (total de simulações)
    for simulacao in range(total_simulacoes):
        Round = 1
        totalRounds = 0
        nodes = gerarCenario(qtdNodes,distMax)
        nosVivos = list()

        if(interCluster == 1):
            # CONFIGURAÇÕES INICIAIS (Setorização intercluster)
            # Trasmite as localizações à BS
            distanciasBS = []
            for k in nodes:
                dist = distancia(k[2],k[3],BS[1],BS[2])
                distanciasBS.append( dist )
                k[1] = gastoTx(k[1],dist,tamPacoteConfig)
            # Recebe os setores da BS
            for k in nodes:
                k[9] = setorizacaoCH(distanciasBS,distanciasBS[k[0]-1],qtdSetores)
                k[1] = gastoRx(k[1],tamPacoteConfig)


        # INICIO DA EXECUÇÃO DA SIMULAÇÃO
        while(Round <= 4000 and len(nodes) != 0):

            # Energy Harvesting
            start = time.time()
            H = irradiacao(Round)
            for n in nodes:
                n[1] += harvest(H)
                if n[1] >= 5.0:
                    n[1] = 5.0
            end = time.time()
            print(end-start)

            #Verifica Reset do Round Superior
            if(verifica_eleitos(nodes)):
                for k in nodes:
                    k[6] = 0

            # Realiza seleção de CH
            CH = selecao_CH(nodes, Round, percentualCH)

            # Conta os frames que foram executados
            totalFramesExecutados = 0

            # Execução após seleção
            if(len(CH) != 0):

                # TRANSMISSÃO  CH: Envio do Broadcast
                pacotesBroadcast = []
                for k in CH:
                    pacotesBroadcast.append( [k[0],k[2],k[3],0.0,k[9]] )
                    # Registro da BS para envio
                    k[7].append(BS)
                    k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                # RECEPÇÃO     CH: Chs recebem o broadcast dos outros CHs (os rádios estão ligados)
                for k in CH:
                    for node in pacotesBroadcast:
                        if(node[0] != k[0]):
                            k[7].append(node)
                    k[1] = gastoRx(k[1],tamPacoteConfig)

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
                        k[1] = gastoRx(k[1],tamPacoteConfig)

                    # TRANSMISSÃO NCH: Envio de Pacotes Resposta
                    for k in nodes:
                        node = [k[0],k[2],k[3],k[4],0]
                        # localiza o CH escolhido na lista de CH e coloca seu node em ListCL do CH
                        for nodeCH in CH:
                            if(k[7][0][0] == nodeCH[0]):
                                nodeCH[8].append(node)
                        k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                    # RECEPÇÃO     CH: Recepção de Pacotes de Resposta
                    for k in CH:
                        # Nodes atribuídos na função anterior
                        for l in range( len(k[8]) ):
                            k[1] = gastoRx(k[1],tamPacoteConfig)

                    # TRANSMISSÃO  CH: Envio da Tabela TDMA
                    ajuste_alcance_nodeCH(CH)
                    clusters = []
                    for k in CH:
                        clusters.append( [k[0], setorizacao(k[8],qtdSetores)] )
                        k[1] = gastoTx(k[1],k[4],tamPacoteConfig)

                    # RECEPÇÃO    NCH: Recepção da Tabela TDMA
                    for k in nodes:
                        idCH = k[7][0][0]
                        # Localiza o cluster do CH
                        for clstr in clusters:
                            if(clstr[0] == idCH):
                                k[8] = clstr[1]
                        k[1] = gastoRx(k[1],tamPacoteConfig)

                    # CONFIGURAÇÃO DE RADIO DOS CH PARA ALCANÇAR A BS
                    for k in CH:
                        k[4] = distancia(k[2],k[3], BS[1],BS[2])

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
                    for contFrame in range(qtdFrames):
                        confirmaFrame = 0
                        # NCH: Transmite Pacote
                        for k in nodes:
                            if(intraCluster == 1):
                                # Gasto de agregação de dados
                                totalContEnc = contEncaminhamento(k[0], mapaEncaminhamento)
                                if(totalContEnc > 0):
                                    k[1] = k[1] - (0.000000005*tamPacoteTransmissao*(totalContEnc + 1))
                            k[1] = gastoTx(k[1],k[4],tamPacoteTransmissao)
                        # CH: Recebe Pacote
                        for k in CH:
                            for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                k[1] = gastoRx(k[1],tamPacoteTransmissao)
                        # NCH: Recebe Pacote
                        if(intraCluster == 1):
                            for k in nodes:
                                for l in range( contEncaminhamento(k[0], mapaEncaminhamento) ):
                                    k[1] = gastoRx(k[1],tamPacoteTransmissao)
                        # CH: Envia Pacote para a BS
                        for k in CH:
                            # Gasto de agregação de dados
                            totalContEnc = contEncaminhamento(k[0], mapaEncaminhamento)
                            if(totalContEnc > 0):
                                k[1] = k[1] - (0.000000005*tamPacoteTransmissao*(totalContEnc + 1))
                            node = k
                            idDestino = node[7][0][0]
                            while(idDestino != 0):
                                node[1] = gastoTx(node[1],node[4],tamPacoteTransmissao)
                                node = localizaObjetoCH(idDestino,CH)
                                # Gasto Recepção do node destino
                                node[1] = gastoRx(node[1],tamPacoteTransmissao)
                                idDestino = node[7][0][0]
                            node[1] = gastoTx(node[1],node[4],tamPacoteTransmissao)
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
    media = sum(roundsSimulacao) / total_simulacoes

    print('\nResultado do ' + str(modoOp[0]) + str(modoOp[1]) +"-LEACH-HOP:")
    print('Rounds: ', roundsSimulacao)
    print('Média: ' + str(media))
    print('Erro: ' + str(1.96*(desvio_padrao(roundsSimulacao, media) / math.sqrt(total_simulacoes) )))
    arquivo.write("\nResultado do " + str(modoOp[0]) + str(modoOp[1]) +"-LEACH-HOP:\nRounds: "+ str(roundsSimulacao) +"\nMédia: " + str(media) +'\nErro: ' + str(1.96*(desvio_padrao(roundsSimulacao, media) / math.sqrt(total_simulacoes) )))
    # FIM DE TODOS OS EXPERIMENTOS DE UM MODO DE OPERAÇÃO ##########

#plt.plot(df.index, df['NosVivos'])
#print("Last round:", max(df.index))

arquivo.close()
arquivo_bat.close()
