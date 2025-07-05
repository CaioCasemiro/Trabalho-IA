from puzzle import PuzzleState
from utils import exibir_caminho_com_estados
import time
from collections import deque

MAX_NOS = 1_000_000
LIMITE_PROFUNDIDADE_PADRAO = 50

def bfs(estado_inicial, objetivo, tamanho, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = deque([estado_inicial_obj])
    visitados = set([estado_inicial_obj.estado])
    arvore = {estado_inicial_obj.estado: None}
    nos_expandidos = 0

    while fronteira:
        atual = fronteira.popleft()
        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None
        if atual.is_objetivo(objetivo):
            tempo = time.time() - inicio
            return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

        for filho in atual.gerar_filhos(tamanho):
            if filho.estado not in visitados:
                fronteira.append(filho)
                visitados.add(filho.estado)
                arvore[filho.estado] = atual.estado

    return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None

def dfs(estado_inicial, objetivo, tamanho, limite=LIMITE_PROFUNDIDADE_PADRAO, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    pilha = [(estado_inicial_obj, 0)]
    visitados = set([estado_inicial_obj.estado])
    arvore = {estado_inicial_obj.estado: None}
    nos_expandidos = 0

    while pilha:
        atual, prof = pilha.pop()
        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None
        if atual.is_objetivo(objetivo):
            tempo = time.time() - inicio
            return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

        if prof < limite:
            for filho in atual.gerar_filhos(tamanho):
                if filho.estado not in visitados:
                    pilha.append((filho, prof + 1))
                    visitados.add(filho.estado)
                    arvore[filho.estado] = atual.estado

    return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None

def ids(estado_inicial, objetivo, tamanho, limite=LIMITE_PROFUNDIDADE_PADRAO, gui_mode=False):
    inicio = time.time()
    nos_expandidos = 0

    for limite_atual in range(limite + 1):
        pilha = [(PuzzleState(estado_inicial), 0)]
        visitados = set()
        arvore = {tuple(estado_inicial): None}

        while pilha:
            atual, prof = pilha.pop()
            estado = atual.estado

            if estado in visitados:
                continue
            visitados.add(estado)
            nos_expandidos += 1

            if nos_expandidos > MAX_NOS:
                return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None
            if atual.is_objetivo(objetivo):
                tempo = time.time() - inicio
                return atual.caminho(), tempo, nos_expandidos, atual.profundidade, exibir_caminho_com_estados(atual, tamanho), arvore, atual.estado

            if prof < limite_atual:
                for filho in atual.gerar_filhos(tamanho):
                    if filho.estado not in visitados:
                        pilha.append((filho, prof + 1))
                        arvore[filho.estado] = estado

    return None, time.time() - inicio, nos_expandidos, 0, "", arvore, None
