# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 08:18:15 2019

@author: Juliana
"""
from energySource import prediction
import math


qtdNodes = 100
kmin = 5
kmax = 20
kopt = kmin
timeslot = 0.1    # tempo de slot (segundo)
round_length = 500    # tamanho do round (timeslots)
round_time = round_length * timeslot    # tempo do round (segundos)
horizon = 10   # horizonte de predição (rounds)
payload = 2000

cluster_len = qtdNodes/kopt

pwr_max_tx = 0.0801    # W
pwr_rx = 0.0222    # W
packet_rate = 0.5     # pacotes/s

ener_max_tx = pwr_max_tx * timeslot
ener_rx = pwr_rx * timeslot
ener_nch_tx = 0.0444    # W (valor aproximado para a primeira vez, já que não tem como calcular)
ener_agg = 0.00001*(cluster_len-1)
ener_setup = ener_max_tx + (cluster_len-1)*ener_rx + ener_nch_tx
ener_ch_tx = ener_nch_tx    # W (valor aproximado para a primeira vez, já que não tem como calcular)





def calculaOCHP():
    
    ener_r_net = 0
    for k in range(kmin, kmax+1):
        num_frames = round_length*k/qtdNodes
        cluster_len = qtdNodes/k
        ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
        ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_nch_tx    # Joules
        ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
        ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx      # Joules
        temp = k * (ener_ch_round + ener_nch_round)
    
        if(temp <= ener_r_har and temp > ener_r_net):
            kopt = k
            ener_r_net = temp
    
    return kopt

def calculaCHDC():
    
    dcch = 1/pi
    if (dcch >= 1):
        Dch = math.ceil(dcch)
    else:
        Dch = 1
        
    return Dch
        
def calculaDTDC(Dch):
    
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


pi = kopt/qtdNodes
num_frames = round_length*kopt/qtdNodes
cluster_len = qtdNodes/kopt
ener_agg = (5*10**-9 * payload) * (cluster_len-1)         # Joules
ener_setup = ener_max_tx + ((cluster_len-1)*ener_rx) + ener_max_tx    # Joules
ener_ch_round = num_frames * (ener_max_tx + (cluster_len-1)*ener_rx + ener_agg) + ener_setup     # Joules
ener_nch_round = num_frames * (cluster_len-1) * ener_ch_tx                      # Joules
ener_r_net = kopt * (ener_ch_round + ener_nch_round)

rounds = 10

for rnd in range(1, rounds+1):
    
    harv_pwr = prediction(rnd)
    ener_r_har = qtdNodes*harv_pwr            # Joules
    
    kopt = calculaOCHP()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    