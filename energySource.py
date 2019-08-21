# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import numpy as np


df = pd.read_csv('trace.csv', delimiter='\t')
df.columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

print(df.shape)

df = df[df.b != '     NaN']

print(df.shape)

#Mês
#energia = df['b'][(df["c"]==2009) & (df["d"]==11)]

#Dia
energia = np.array(df['b'][(df["c"]==2009) & (df["d"]==11) & (df["e"]==15)])

print(energia)


with open('trace_24h.txt', 'w') as file:
    for i in range(1, len(energia)):
        file.write("{}\n".format(energia[i]))
