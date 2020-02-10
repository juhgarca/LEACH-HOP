import numpy as np 
import matplotlib.pyplot as plt

ch = [[1,2,4],[2,2,1], [1,5,2],[5,1,6],[3,7,2]]

x = np.array(ch)[:,1]
y = np.array(ch)[:,2]

print(x, "\n", y)

plt.scatter(x, y)
plt.show()