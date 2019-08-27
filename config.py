# -*- coding: utf-8 -*-
'''
Definição das configurações dos nós, rede e simulação
'''

tamPacoteConfig = 300

modosHop = [[0,0], [0,1], [1,0], [1,1]]

list_qtdNodes = [100]
list_qtdFrames = [10]
list_tamPacoteTransmissao = [2000]
list_percentualCH = [0.05]
list_qtdSetores = [4]
list_area = [100]

total_simulacoes = 1
framesSimulacao = []

qtdNodes =                         list_qtdNodes[0]
qtdFrames =                       list_qtdFrames[0]
tamPacoteTransmissao = list_tamPacoteTransmissao[0]
percentualCH =                 list_percentualCH[0]
qtdSetores =                     list_qtdSetores[0]
area =                                 list_area[0]

# [gorlatova2012networking]
cell_size = 10      # cm^2
cell_efic = 0.01
round_len = 20      # segundos

