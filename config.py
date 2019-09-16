# -*- coding: utf-8 -*-
'''
Definição das configurações dos nós, rede e simulação
'''
totalSimulacoes = 33

tamPacoteConfig = 300

bat_init = 5.0

modosHop = [[1,1]]
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
payload = tamPacoteTransmissao

# [gorlatova2012networking]
cell_size = 10      # cm^2
cell_efic = 0.01
round_len = 20      # segundos
max_bat = 5.0       # Joules

# DC-LEACH
kmin = 5
kmax = 20
kopt = kmin
timeslot = 0.1    # tempo de slot (segundo)
round_length = 500    # tamanho do round (timeslots)
round_time = round_length * timeslot    # tempo do round (segundos)
horizon = 10   # horizonte de predição (rounds)

cluster_len = qtdNodes/kopt

cz = 0.000154   # m^2
ez = 0.22
Io = 200    # W/m^2

pwr_max_tx = 0.0801    # W
pwr_rx = 0.0222    # W
packet_rate = 0.5     # pacotes/s

ener_max_tx = pwr_max_tx * timeslot
ener_rx = pwr_rx * timeslot
ener_nch_tx = 0.0444    # W (valor aproximado para a primeira vez, já que não tem como calcular)
ener_agg = 0.00001*(cluster_len-1)
ener_setup = ener_max_tx + (cluster_len-1)*ener_rx + ener_nch_tx
ener_ch_tx = ener_nch_tx    # W (valor aproximado para a primeira vez, já que não tem como calcular)











