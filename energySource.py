# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd


df = pd.read_csv('trace_24h.txt')
a = 0

def harvest(bateria):
    
    bateria += df['energia'][a]
    a += 1
