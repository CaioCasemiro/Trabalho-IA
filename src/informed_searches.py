from puzzle import PuzzleState
from heuristics import pecas_fora_do_lugar, distancia_manhattan
from utils import exibir_caminho_com_estados
import heapq, time

def a_estrela(estado_inicial, objetivo, tamanho_lado, heuristica_escolhida, gui_mode=False):
    def escolher_heuristica(estado, objetivo, heuristica_escolhida):
        if heuristica_escolhida == 1:
            return pecas_fora_do_lugar(estado, objetivo)
        else:
            return distancia_manhattan(estado, objetivo)
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial_obj))
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while fronteira:
        _, estado_atual = heapq.heappop(fronteira)
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
                custo_real = filho.profundidade
                heuristica = escolher_heuristica(filho.estado, objetivo, heuristica_escolhida)
                prioridade = custo_real + heuristica
                heapq.heappush(fronteira, (prioridade, filho))
                arvore[estado_tuple] = tuple(estado_atual.estado)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")

def gulosa(estado_inicial, objetivo, tamanho_lado, heuristica_escolhida, gui_mode=False):
    def escolher_heuristica(estado, objetivo, heuristica_escolhida):
        if heuristica_escolhida == 1:
            return pecas_fora_do_lugar(estado, objetivo)
        else:
            return distancia_manhattan(estado, objetivo)
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial_obj))
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while fronteira:
        _, estado_atual = heapq.heappop(fronteira)
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
                heuristica = escolher_heuristica(filho.estado, objetivo, heuristica_escolhida)
                heapq.heappush(fronteira, (heuristica, filho))
                arvore[estado_tuple] = tuple(estado_atual.estado)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")