# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


setupC = pd.read_csv('setupC.txt', delimiter='\t', low_memory=False)
setupC.columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

print(setupC.shape)

setupC = setupC[setupC.b != '        NaN']         # setupC: '     NaN', nos demais: '        NaN'

print(setupC.shape)

# Mês
#energia = np.array(setupC['b'][(setupC["c"]==2009) & (setupC["d"]==11)])

# 24h
#energia = np.array(setupC['b'][(setupC["c"]==2010) & (setupC["d"]==3) & (setupC["e"]==16)])

# 48h
energia = np.array(setupC['b'][(setupC["c"]==2010) & (setupC["d"]==3) & (setupC["e"]==16)])
energia2 = np.array(setupC['b'][(setupC["c"]==2010) & (setupC["d"]==3) & (setupC["e"]==17)])


print("Min:", min(setupC['b']))
print("Max:", max(setupC['b']))
with open('trace_setupC_48h.txt', 'w') as file:
    for i in range(1, len(energia)):
         file.write("{}\n".format(energia[i].strip(" ")))
    for i in range(1, len(energia2)):
         file.write("{}\n".format(energia[i].strip(" ")))

#plt.plot(range(len(energia_setupC)), energia_setupC)









