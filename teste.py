from energySource import harvest


nodes = []

for i in range(100):
    nodes.append([i+1, 0.5])

#print(nodes)

for i in range(5):
    print(nodes)
    for n in nodes:
        n[1] += harvest(i)
        #print(n)
    print(nodes, '\n\n\n')

#    print('Round: ', i)
#    print('Baterias: ', nodes)



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
