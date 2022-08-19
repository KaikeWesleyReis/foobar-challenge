# -*- coding: utf-8 -*-

from math import factorial
from functools import reduce
from collections import Counter

def generate_integer_partitions(n):
  '''
  Implementar o gerador de particoes de inteiros.
  Creditos para: Jerome Kelleher em https://jeromekelleher.net/generating-integer-partitions.html
  '''
  a = [0 for i in range(n + 1)]
  k = 1
  y = n - 1
  while k != 0:
      x = a[k - 1] + 1
      k -= 1
      while 2 * x <= y:
          a[k] = x
          y -= x
          k += 1
      l = k + 1
      while x <= y:
          a[k] = x
          a[l] = y
          yield a[:k + 2]
          x += 1
          y -= 1
      a[k] = x + y
      y = x + y - 1
      yield a[:k + 1]

def calculate_gcd(a, b):
  '''
  Implementar GCD usando recursao com algoritmo euclidiano entre dois valores.
  '''
  if (a == 0):
    return b
  return calculate_gcd(b % a, a)

def solution(w,h,s):
  # Prepare
  '''
  Implementar teorema de enumeração de Polia seguindo a formula abaixo.
  Creditos para: https://franklinvp.github.io/2020-06-05-PolyaFooBar/
  '''
  # Definir lista para segurar valores
  ST2 = list()

  # Loop sobre todas as partições na dimensão w
  for partition_w in generate_integer_partitions(w):
    # Calculo da primeira fracao em uma particao de w
    st2_w_numerator = factorial(w)  
    st2_w_denominator = reduce(lambda x, y: x*y, [factorial(k)*(i**k) for i, k in Counter(partition_w).items()])
    st2_w = st2_w_numerator // st2_w_denominator

    # Loop sobre todas as partições na dimensão w
    for partition_h in generate_integer_partitions(h):
      # Calculo da primeira fracao em uma particao de h
      st2_h_numerator = factorial(h)
      st2_h_denominator = reduce(lambda x, y: x*y, [factorial(k)*(j**k) for j, k in Counter(partition_h).items()])
      st2_h = st2_h_numerator // st2_h_denominator
      
      # Calcular a parte exponencial que contém somatorio de GCD
      st2_exponent = list()
      # Calculate exponents
      for a in partition_w:
        for b in partition_h:
          st2_exponent.append(calculate_gcd(a,b))

      # Calcular termo s elevado ao exponencial do somatorio anterior
      st2_sum_exp = s**reduce(lambda x, y: x+y, st2_exponent)
      # Adicionar os termos na lista criada
      ST2.append((st2_w*st2_h*st2_sum_exp))

  # Gerar N como mostrado no link
  N = str(reduce(lambda x, y: x+y, ST2)/(factorial(w)*factorial(h)))
  return N