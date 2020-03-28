
def definir_setores(area_cluster, qtd_setores, closest_node):
   
   tam_setor = area_cluster / qtd_setores
   setores = []
   for i in range(0, qtd_setores):
      setor_inicio = closest_node + tam_setor*i
      setor_fim = setor_inicio + tam_setor
      setores.append([setor_inicio, setor_fim])
   
   return setores


def setorizacao(cluster, qtd_setores):
   
   closest_node = distMax
   farthers_node = 0
   for nch in cluster:
      if nch[3] <= closest_node:
         closest_node = nch[3]
      if nch[3] >= farthest_node:
         farthest_node = nch[3]
   area_cluster = farthers_node - closest_node
   setores = definir_setores(area_cluster, qtd_setores, closest_node)

   for nch in cluster:
      i = 1
      for setor in setores:
         if nch[3] >= setor[1] and nch[3] <= setor[2]:
            nch[3] = i
         i += 1

