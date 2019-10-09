import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error





rssf = list()

for i in range(100):
    pos_x = np.random.uniform(0, 100)
    pos_y = np.random.uniform(0, 100)
    rssf.append([pos_x, pos_y])
    
plt.scatter(list(range(100)), list(range(100)), 'ro')
plt.axis(rssf)
plt.show()

# =============================================================================
# df = pd.read_csv('trace_setupC_48h.txt')
# 
# 
# #Define função para calcular o MAPE
# def mape(y_pred,y_true):
#     return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
# 
# 
# #--------------------------- EWMA ---------------------------
# #ener = np.array(energia)
# ener = df['energia']
# ener_ewma = df.ewm(span=500).mean()
# 
# plt.xlabel('Tempo')
# plt.ylabel('Energia')
# plt.title('Modelo EWMA')
# plt.plot(df.index, ener, label='Trace Real')
# plt.plot(df.index, ener_ewma, color='red', label='EWMA')
# plt.legend(loc='best')
# plt.show()
# 
# #Cálculo de erros
# rmse = np.sqrt(mean_squared_error(ener, ener_ewma['energia']))
# print('========================== ERROS EWMA ==========================')
# print('Root Mean Square Error: %.3f' % rmse)
# print('\nMean Absolute Percentage Error', mape(ener_ewma['energia'],ener))
# print('================================================================')
# =============================================================================
