from puzzle import PuzzleState
from utils import exibir_caminho_com_estados
import time
from collections import deque

def bfs(estado_inicial, objetivo, tamanho_lado, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = deque([estado_inicial_obj])
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while fronteira:
        estado_atual = fronteira.popleft()
        nos_expandidos += 1
        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            tempo_exec = fim - inicio
            if gui_mode:
                return (caminho, tempo_exec, nos_expandidos, profundidade, "", arvore, tuple(estado_atual.estado))
            print("Objetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Profundidade da solução:", profundidade)
            print("Nós expandidos:", nos_expandidos)
            print(exibir_caminho_com_estados(estado_atual, tamanho_lado))
            return
        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            estado_tuple = tuple(filho.estado)
            if estado_tuple not in visitados:
                visitados.add(estado_tuple)
                fronteira.append(filho)
                arvore[estado_tuple] = tuple(estado_atual.estado)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")

def dfs(estado_inicial, objetivo, tamanho_lado, limite=50, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    pilha = [(estado_inicial_obj, 0)]
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while pilha:
        estado_atual, prof = pilha.pop()
        nos_expandidos += 1
        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            tempo_exec = fim - inicio
            if gui_mode:
                return (caminho, tempo_exec, nos_expandidos, profundidade, "", arvore, tuple(estado_atual.estado))
            print("Objetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Profundidade da solução:", profundidade)
            print("Nós expandidos:", nos_expandidos)
            print(exibir_caminho_com_estados(estado_atual, tamanho_lado))
            return
        if prof < limite:
            filhos = estado_atual.gerar_filhos(tamanho_lado)
            for filho in filhos:
                estado_tuple = tuple(filho.estado)
                if estado_tuple not in visitados:
                    visitados.add(estado_tuple)
                    pilha.append((filho, prof+1))
                    arvore[estado_tuple] = tuple(estado_atual.estado)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")

def ids(estado_inicial, objetivo, tamanho_lado, limite=50, gui_mode=False):
    inicio = time.time()
    for profundidade_max in range(limite+1):
        estado_inicial_obj = PuzzleState(estado_inicial)
        pilha = [(estado_inicial_obj, 0)]
        visitados = set()
        visitados.add(tuple(estado_inicial))
        nos_expandidos = 0
        arvore = {tuple(estado_inicial): None}
        while pilha:
            estado_atual, prof = pilha.pop()
            nos_expandidos += 1
            if estado_atual.is_objetivo(objetivo):
                fim = time.time()
                caminho = estado_atual.caminho()
                profundidade = estado_atual.profundidade
                tempo_exec = fim - inicio
                if gui_mode:
                    return (caminho, tempo_exec, nos_expandidos, profundidade, "", arvore, tuple(estado_atual.estado))
                print("Objetivo alcançado!")
                print("Sequência de movimentos:", caminho)
                print("Profundidade da solução:", profundidade)
                print("Nós expandidos:", nos_expandidos)
                print(exibir_caminho_com_estados(estado_atual, tamanho_lado))
                return
            if prof < profundidade_max:
                filhos = estado_atual.gerar_filhos(tamanho_lado)
                for filho in filhos:
                    estado_tuple = tuple(filho.estado)
                    if estado_tuple not in visitados:
                        visitados.add(estado_tuple)
                        pilha.append((filho, prof+1))
                        arvore[estado_tuple] = tuple(estado_atual.estado)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")
