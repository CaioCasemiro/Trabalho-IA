from puzzle import PuzzleState
from utils import exibir_caminho_com_estados
import time
from collections import deque

MAX_NOS = 1_000_000
# Limites de profundidade por tamanho
LIMITE_PROFUNDIDADE = {3: 50, 4: 150, 5: 300}
TIMEOUT = 30  # segundos

def bfs(estado_inicial, objetivo, tamanho, gui_mode=False):
    inicio = time.perf_counter()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = deque([estado_inicial_obj])
    visitados = set([estado_inicial_obj.estado])
    arvore = {estado_inicial_obj.estado: None}
    nos_expandidos = 0

    while fronteira:
        if time.perf_counter() - inicio > TIMEOUT:
            return None, time.perf_counter() - inicio, nos_expandidos, 0, "Timeout excedido", None, None
        atual = fronteira.popleft()
        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            return None, time.perf_counter() - inicio, nos_expandidos, 0, "Limite de nós excedido", None, None
        if atual.is_objetivo(objetivo):
            tempo = time.perf_counter() - inicio
            return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

        for filho in atual.gerar_filhos(tamanho):
            if filho.estado not in visitados:
                fronteira.append(filho)
                visitados.add(filho.estado)
                arvore[filho.estado] = atual.estado

    return None, time.perf_counter() - inicio, nos_expandidos, 0, "Solução não encontrada", arvore, None

def dfs(estado_inicial, objetivo, tamanho, gui_mode=False):
    inicio = time.perf_counter()
    limite = LIMITE_PROFUNDIDADE.get(tamanho, 300)
    estado_inicial_obj = PuzzleState(estado_inicial)
    pilha = [(estado_inicial_obj, 0)]
    visitados = set([estado_inicial_obj.estado])
    arvore = {estado_inicial_obj.estado: None}
    nos_expandidos = 0

    while pilha:
        if time.perf_counter() - inicio > TIMEOUT:
            return None, time.perf_counter() - inicio, nos_expandidos, 0, "Timeout excedido", None, None
        atual, prof = pilha.pop()
        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            return None, time.perf_counter() - inicio, nos_expandidos, 0, "Limite de nós excedido", None, None
        if atual.is_objetivo(objetivo):
            tempo = time.perf_counter() - inicio
            return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

        if prof < limite:
            for filho in atual.gerar_filhos(tamanho):
                if filho.estado not in visitados:
                    pilha.append((filho, prof + 1))
                    visitados.add(filho.estado)
                    arvore[filho.estado] = atual.estado

    return None, time.perf_counter() - inicio, nos_expandidos, 0, "Solução não encontrada", arvore, None

def ids(estado_inicial, objetivo, tamanho, gui_mode=False):
    inicio = time.perf_counter()
    nos_expandidos = 0
    limite_max = LIMITE_PROFUNDIDADE.get(tamanho, 300)

    for limite_atual in range(limite_max + 1):
        pilha = [(PuzzleState(estado_inicial), 0)]
        visitados = set()
        arvore = {tuple(estado_inicial): None}

        while pilha:
            if time.perf_counter() - inicio > TIMEOUT:
                return None, time.perf_counter() - inicio, nos_expandidos, 0, "Timeout excedido", None, None
            atual, prof = pilha.pop()
            estado = atual.estado

            if estado in visitados:
                continue
            visitados.add(estado)
            nos_expandidos += 1

            if nos_expandidos > MAX_NOS:
                return None, time.perf_counter() - inicio, nos_expandidos, 0, "Limite de nós excedido", None, None
            if atual.is_objetivo(objetivo):
                tempo = time.perf_counter() - inicio
                return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

            if prof < limite_atual:
                for filho in atual.gerar_filhos(tamanho):
                    if filho.estado not in visitados:
                        pilha.append((filho, prof + 1))
                        arvore[filho.estado] = estado

    return None, time.perf_counter() - inicio, nos_expandidos, 0, "Solução não encontrada", arvore, None