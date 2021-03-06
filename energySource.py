# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:42:49 2019

@author: Juliana
"""
import pandas as pd
import config as c
from sympy import integrate, symbols

df = pd.read_csv('trace_setupC_48h.txt')
ener_ewma = df.ewm(span=c.horizon).mean()

def harvest(Round):
    I = df['energia'][Round] * 10 ** -6
    x = symbols('x')
    def f(x): return I*x
    H = integrate(f(x),(x,0,c.round_len))
    d = c.cell_size * c.cell_efic * H
    return d


def prediction(Round):
    I = ener_ewma['energia'][Round] * 10 ** -6
    x = symbols('x')
    def f(x): return I*x
    H = integrate(f(x),(x,0,c.round_len))
    d = c.cell_size * c.cell_efic * H
    return d