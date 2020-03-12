# ch[11] deve ser uma lista de nós, mas com menos informações: [id, x, y, dist/setor]

# Calcula a distância para todos os nós
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

def setor(setor_size, n[3], NUM_SETORES):