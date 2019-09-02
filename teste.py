from energySource import harvest, irradiacao
from sympy import integrate, symbols


nodes = []

for i in range(100):
    nodes.append([i+1, 0.5])

#print(nodes)

for i in range(20):
    H = irradiacao(i)
    for n in nodes:
        n[1] += harvest(H)
        #print(n)
    #print(nodes, '\n\n\n')

#    print('Round: ', i)
#    print('Baterias: ', nodes)



# =============================================================================
# x = symbols('x')
# def f(x): return 0.04*x
# print(integrate(f(x),(x,0,20)))
# 
# result = 0
# for i in range(21):
#     result = result+((0.04*10**-6)*i)
# 
# print(result)
# =============================================================================
    