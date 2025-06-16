from puzzle import PuzzleState
from heuristics import *
from utils import *
import heapq
import time

def escolher_heuristica(estado, objetivo, heuristica_escolhida):
    if heuristica_escolhida == 1:
        return pecas_fora_do_lugar(estado, objetivo)
    else:
        return distancia_manhattan(estado, objetivo)

def a_estrela(estado_inicial, estado_objetivo, tamanho_lado, heuristica_escolhida):
    print("\nExecutando Busca A* (A Estrela)...")
    inicio = time.time()

    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial_obj))
    visitados = set()
    visitados.add(tuple(estado_inicial))

    while fronteira:
        _, estado_atual = heapq.heappop(fronteira)

        if estado_atual.is_objetivo(estado_objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            print("\nObjetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Quantidade de passos:", len(caminho))
            print(f"Tempo de execução: {fim - inicio:.4f} segundos")
            print("Profundidade da solução:", estado_atual.profundidade)
            exibir_caminho_com_estados(estado_atual, tamanho_lado)
            return

        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            estado_tuple = tuple(filho.estado)
            if estado_tuple not in visitados:
                visitados.add(estado_tuple)
                custo_real = filho.profundidade
                heuristica = escolher_heuristica(filho.estado, estado_objetivo, heuristica_escolhida)
                prioridade = custo_real + heuristica
                heapq.heappush(fronteira, (prioridade, filho))

    print("Nenhuma solução encontrada.")


def gulosa(estado_inicial, estado_objetivo, tamanho_lado, heuristica_escolhida):
    
    print("\nExecutando Busca Gulosa...")
    inicio = time.time()

    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heuristica = escolher_heuristica(estado_inicial, estado_objetivo, heuristica_escolhida)
    heapq.heappush(fronteira, (heuristica, estado_inicial_obj))
    visitados = set()
    visitados.add(tuple(estado_inicial))

    while fronteira:
        _, estado_atual = heapq.heappop(fronteira)

        if estado_atual.is_objetivo(estado_objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            print("\nObjetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Quantidade de passos:", len(caminho))
            print(f"Tempo de execução: {fim - inicio:.4f} segundos")
            print("Profundidade da solução:", estado_atual.profundidade)
            exibir_caminho_com_estados(estado_atual, tamanho_lado)
            return

        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            estado_tuple = tuple(filho.estado)
            if estado_tuple not in visitados:
                visitados.add(estado_tuple)
                heuristica = escolher_heuristica(filho.estado, estado_objetivo, heuristica_escolhida)
                heapq.heappush(fronteira, (heuristica, filho))

    print("Nenhuma solução encontrada.")