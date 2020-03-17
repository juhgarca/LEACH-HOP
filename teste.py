# ch[11] deve ser uma lista de nós, mas com menos informações: [id, x, y, dist/setor]

"""# Calcula a distância para todos os nós
menor = distMax
maior = 0
for ch in CH:
   for no in ch[11]:
      no[3] = dist(ch[1], no[1], ch[2], no[2])
      # Pega mais próximo e mais distante
      if no[3] < menor:
         menor = no[3]
      if no[3] > maior:
         maior = no[3]
      # Subtrai os dois
      area_cluster = maior - menor
      # Divide por NUM_SETORES
      setor_size = area_cluster / NUM_SETORES

# Preciso de uma função que receba setor_size e a distância e retorne o setor ao qual o nó pertence

#def setor(setor_size, n[3], NUM_SETORES):


setor = 1
start = closest_node
end = start+tam_setor
for start, end in zip(colecao1, colecao2):
   for d in lista_distancias:
      if d > start and d < end:
         d = setor
   setor += 1
"""
# start itera de closest_node até farthest_node - tam_setor, passo do tamanho do setor, para ambos
# end itera de closest_node + tam_setor até farthest_node
# exemplo: cluster_area = 20  nó mais próximo = 1     nó mais distante = 20      tam_setor = 4
#            range_start = range(1, 20-tam_setor, tam_setor)
#              range_end = range(1+tam_setor, 20, tam_setor)

range_start = range(1, 20, 4)
range_end = range(1+4, 20, 4)
print("Range start:", range_start, "\nRange end:", range_end)
i = 1
for start, end in zip(range_start, range_end):
   print("Setor", i,":", start, "-", end)