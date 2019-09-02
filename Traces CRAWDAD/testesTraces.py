# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:29:19 2019

@author: Juliana
"""
import pandas as pd

traceC = pd.read_csv('trace_setupC_48h.txt')
traceC.columns = ["energia"]

print("Min:", min(traceC['energia']))
print("Max:", max(traceC['energia']))