# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import config as c

df = pd.read_csv('trace_days.txt')


def harvest(bateria, Round):
    d = c.cell_size * c.cell_efic * (df['energia'][Round] * 10**-6) * 20
    #d = c.cell_size * c.cell_efic * df['energia'][Round] * 20
    bateria += d
