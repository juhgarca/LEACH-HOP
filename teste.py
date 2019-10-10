
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
    