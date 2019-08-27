from energySource import harvest


nodes = []

for i in range(100):
    nodes.append(0.5)
    

for i in range(20):
    for n in nodes:
        #print(n)
        n += harvest(i)
        #print(n)
        
    print('Round: ', i)
    print('Baterias: ', nodes)



# =============================================================================
# arquivo = open('novo-arquivo.txt', 'w')
# 
# 
# for i in range(4):
#     string = 'nova linha ' + str(i) + '\n'
#     arquivo.write(string)
#     
#     
# arquivo.close()
# =============================================================================
