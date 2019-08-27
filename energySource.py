# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import config as c

df = pd.read_csv('trace_days.txt')

def harvest(Round):
    d = c.cell_size * c.cell_efic * (df['energia'][Round] * 10 ** -6) * c.round_len
    #d = c.cell_size * c.cell_efic * df['energia'][Round] * c.round_len
    print(d)
    return d
