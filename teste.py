from config import *

print(bat_init)

""" 
Round = 1
horizon_ctrl = 0
num_frames = 2
horizon = 4

while Round <= 20:

    print(">>>>>>>>> INÍCIO DO ROUND", Round)

    if horizon_ctrl == 0:
        print("   calculaOCHP()")
        print("   calculaCHCD()\n")
    
    print("CHs se anunciam")
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
    Round += 1
     """

""" import numpy as np

Dch = 3
energia = 3
limiar = 3

count_dch = np.random.randint(1, Dch+1)
i=1
while i < 21:
    
    if count_dch == 1:
        if energia >= limiar:
            print(count_dch, " SOU CH")
        else:
            count_dch = 0
            print("recharging...")
    else:
        print(count_dch, " SOU NCH")
        
    if count_dch < Dch:
        count_dch +=1
    elif count_dch == Dch:
        print("Reset count")
        count_dch = 1

    if i == 12:
        energia = 2

    if i == 17:
        energia +=1

    i +=1 """

