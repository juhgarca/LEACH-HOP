

arquivo = open('novo-arquivo.txt', 'w')


for i in range(4):
    string = 'nova linha ' + str(i) + '\n'
    arquivo.write(string)
    
    
arquivo.close()