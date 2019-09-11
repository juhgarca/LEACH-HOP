# -*- coding: utf-8 -*-
'''
Definição das configurações dos nós, rede e simulação
'''
totalSimulacoes = 33

tamPacoteConfig = 300

bat_init = 2.5

modosHop = [[0,0]]
#modosHop = [[0,0], [0,1], [1,0], [1,1]]

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

BS = [0, area+25.0, area/2, 0.0, 0]

# [gorlatova2012networking]
cell_size = 10      # cm^2
cell_efic = 0.01
round_len = 20      # segundos
max_bat = 5.0       # Joules

# DC-LEACH
kmin = 5
kmax = 20
kopt = 0
Ts = 0.1    # tempo de slot (segundo)
Lr = 500    # tamanho do round (timeslots)
Tr = Lr * Ts    # tempo do round (segundos)
Lhor = 10   # horizonte de predição (rounds)

cz = 0.000154   # m^2
ez = 0.22
Io = 200    # W/m^2

Pmax_tx = 0.0801    # W
Prx = 0.0222    # W
p = 0.5     # pacotes/s