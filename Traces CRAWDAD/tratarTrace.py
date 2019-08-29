# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


setupF = pd.read_csv('setupF.txt', delimiter='\t', low_memory=False)
setupF.columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

print(setupF.shape)

setupF = setupF[setupF.b != '        NaN']

print(setupF.shape)

# Mês
#energia = np.array(setupF['b'][(setupF["c"]==2009) & (setupF["d"]==11)])

#Dia
energia = np.array(setupF['b'][(setupF["c"]==2010) & (setupF["d"]==3) & (setupF["e"]==16)])

print("Min:", min(setupF['b']))
print("Max:", max(setupF['b']))
# =============================================================================
# 
# #Dia
# energia = np.array(setupF['b'][(setupF["c"]==2009) & (setupF["d"]==8) & (setupF["e"]==15)])
# energia2 = np.array(setupF['b'][(setupF["c"]==2009) & (setupF["d"]==8) & (setupF["e"]==16)])
# energia3 = np.array(setupF['b'][(setupF["c"]==2009) & (setupF["d"]==8) & (setupF["e"]==17)])
# energia4 = np.array(setupF['b'][(setupF["c"]==2009) & (setupF["d"]==8) & (setupF["e"]==18)])
# 
# 
# #print(energia)
# 
# with open('trace_setupF_mes.txt', 'w') as file:
#     for i in range(1, len(energia)):
#         file.write("{}\n".format(energia[i].strip(" ")))
#     for i in range(1, len(energia2)):
#         file.write("{}\n".format(energia2[i].strip(" ")))
#     for i in range(1, len(energia3)):
#         file.write("{}\n".format(energia3[i].strip(" ")))
#     for i in range(1, len(energia4)):
#         file.write("{}\n".format(energia4[i].strip(" ")))
# 
# 
# =============================================================================
with open('trace_setupF_24h.txt', 'w') as file:
     for i in range(1, len(energia)):
         file.write("{}\n".format(energia[i].strip(" ")))

#plt.plot(range(len(energia_setupF)), energia_setupF)









