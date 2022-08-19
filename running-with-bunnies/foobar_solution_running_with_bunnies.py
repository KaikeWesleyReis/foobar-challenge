# -*- coding: utf-8 -*-
# Linha acima me salvou depois de 1h ...

from itertools import product, permutations

def encontrar_distancias_fonte(grafo, no_fonte):
    # Calcular quantidade de nos
    qtd_no = len(grafo)
    
    # Definir as distancias fonte-no iniciais como o maximo valor numerico - infinito
    distancias_fonte_no = [float('inf') for i in range(qtd_no)]
    
    # Definir distancia da fonte para propria fonte
    distancias_fonte_no[no_fonte] = grafo[no_fonte][no_fonte]

    # Criar grid do grafo de pesos
    grid = list(product(range(0, qtd_no), range(0, qtd_no)))

    # Loop #1 - Executar relaxamento para cada no N-1 vezes
    for relax in range(0, qtd_no - 1):
      # Loop #2 - Seja ns o no de origem e nd o no destino no grid de pesos
      for no, nd in grid:
        # Puxar peso do no --> nd
        peso = grafo[no][nd]
        # Avaliar distancia candidata do momento
        dist_candidata = distancias_fonte_no[no] + peso
        # Fazer checagem - Dist. Candidata eh menor que a a atual para nd?
        if dist_candidata < distancias_fonte_no[nd]:
          distancias_fonte_no[nd] = dist_candidata

    # Retornar vetor 1xN com menores distancias da fonte para demais nos
    return distancias_fonte_no

def verificar_ciclo_negativo(grafo, grafo_to_check):
    # Calcular quantidade de nós
    qtd_no = len(grafo_to_check)

    # Criar grid do grafo de pesos
    grid = list(product(range(0, qtd_no), range(0, qtd_no)))

    # Loop #0 - Para cada nó fonte
    for nf in range(0, qtd_no):
      # Loop #1 - Checar relaxamento para cada nó N-1 vezes
      for relax in range(0, qtd_no - 1):
        # Loop #2 - Seja ns o nó de origem e nd o nó destino no grid de pesos
        for no, nd in grid:
          # Checar condição do ciclo negativo
          if grafo_to_check[nf][no] + grafo[no][nd] < grafo_to_check[nf][nd]:
            # Se for True uma vez na busca, teremos ciclo negativo
            return True
    
    # Caso nenhum ciclo seja encontrado retornar falso
    return False

def calcular_algoritmo_bellman_ford(grafo):
    # Iniciar matriz de distâncias de cada nó para todos do grafo
    grafo_min_distancias = list()
    
    # Loop para aplicar BF em cada nó e calcular as distâncias
    for no_fonte in range(len(grafo)):
        # Calcular distâncias de todos os nós até o nó fonte
        no_distancias = encontrar_distancias_fonte(grafo, no_fonte=no_fonte)
        # Salvar valores encontrados
        grafo_min_distancias.append(no_distancias)

    # Retornar matrix de distâncias
    return grafo_min_distancias

def solution(times, time_limit):
  # Tamanho da matriz
  tam = len(times)

  # Definir quantos coelhos temos
  qtd_coelhos = tam - 2

  # Gerar grafo com distancia minima
  grafo_min_dist = calcular_algoritmo_bellman_ford(times)

  # Verificar presença de ciclo negativo no grafo minimo
  if verificar_ciclo_negativo(times, grafo_min_dist) is True:
    # Retornar máximo possível de coelhos 0 -> N - 2
    return list(range(0, qtd_coelhos - 1))
  
  else:
    # Criar lista de possíveis grupos a serem salvos
    grupos_salvamento = list()

    # Definir tamanho máximo de grupo encontrado
    tam_max = float('-inf')

    # Loop #1 - Definir quantidade máxima de coelhos buscados de 1 -> N - 2
    for qtd_salva in range(qtd_coelhos, 0, -1):
      # Gerar permutações possíveis para a possível quantidade salva
      perm_coelhos = list(permutations(range(1, qtd_coelhos + 1), qtd_salva))
      # Loop #2 - Checar possibilidades de percurso dado permutacoes
      for pc in perm_coelhos:
        # Criar percurso Inicio (fixo) + Coelhos (mutavel) + Porta final (fixo)
        percurso = [0] + list(pc) + [tam-1]

        # Definir custo de tempo
        custo_tempo_total = 0

        # Calcular custo de tempo do percurso via loop
        for idx in range(0, len(percurso)-1):
          # Puxar tempo min de origem (idx) para destino (idx + 1)
          tempo_busca = grafo_min_dist[percurso[idx]][percurso[idx+1]]
          # Somar este tempo ao custo total
          custo_tempo_total += tempo_busca
        
        # Checar se alcançamos a meta
        if custo_tempo_total <= time_limit:
          # Criar conjunto candidato ao salvamento
          grupo_candidato = [coelho - 1 for coelho in sorted(list(pc))]

          # Só permite um update visto que está em ordem decrescente
          if len(grupo_candidato) >= tam_max:
            # Fixar tamanho do grupo ótimo de salvamento
            tam_max = len(grupo_candidato)

            ## Salvar informações do possível grupo
            grupos_salvamento.append(grupo_candidato)
    
    # Retornar lista vazia caso seja impossível salvar algum ou resposta
    if len(grupos_salvamento) == 0:
      return []
    else:
      return sorted(grupos_salvamento,key=sum)[0]