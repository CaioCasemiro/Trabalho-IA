from puzzle import PuzzleState
from heuristics import pecas_fora_do_lugar, distancia_manhattan
from utils import exibir_caminho_com_estados
import heapq, time

MAX_NOS = 1_000_000  # Limite de nós expandidos
TIMEOUT = 30  # segundos

def a_estrela(estado_inicial, objetivo, tamanho_lado, heuristica_escolhida, gui_mode=False):
    def escolher_heuristica(estado, objetivo, heuristica_escolhida):
        return pecas_fora_do_lugar(estado, objetivo) if heuristica_escolhida == 1 else distancia_manhattan(estado, objetivo)

    inicio = time.time()
    cache_heuristica = {}
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial_obj))

    custo_estado = {tuple(estado_inicial): 0}
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while fronteira:
        if time.time() - inicio > TIMEOUT:
            return None, time.time() - inicio, nos_expandidos, 0, "Timeout excedido", arvore, None
        prioridade_atual, estado_atual = heapq.heappop(fronteira)
        estado_tuple = tuple(estado_atual.estado)
        custo_g_atual = custo_estado.get(estado_tuple, float('inf'))

        # Usar cache para heurística
        if estado_tuple in cache_heuristica:
            heuristica_atual = cache_heuristica[estado_tuple]
        else:
            heuristica_atual = escolher_heuristica(estado_atual.estado, objetivo, heuristica_escolhida)
            cache_heuristica[estado_tuple] = heuristica_atual

        if prioridade_atual > custo_g_atual + heuristica_atual:
            continue

        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            fim = time.time()
            return None, fim - inicio, nos_expandidos, 0, "Limite de nós excedido", arvore, None

        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            caminho_estados = exibir_caminho_com_estados(estado_atual, tamanho_lado)
            return caminho, fim - inicio, nos_expandidos, profundidade, caminho_estados, arvore, estado_tuple

        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            filho_tuple = tuple(filho.estado)
            custo_g_filho = filho.profundidade

            if custo_g_filho < custo_estado.get(filho_tuple, float('inf')):
                custo_estado[filho_tuple] = custo_g_filho
                # Calcular ou usar cache para heurística do filho
                if filho_tuple in cache_heuristica:
                    heuristica_filho = cache_heuristica[filho_tuple]
                else:
                    heuristica_filho = escolher_heuristica(filho.estado, objetivo, heuristica_escolhida)
                    cache_heuristica[filho_tuple] = heuristica_filho
                prioridade = custo_g_filho + heuristica_filho
                heapq.heappush(fronteira, (prioridade, filho))
                arvore[filho_tuple] = estado_tuple

    fim = time.time()
    return None, fim - inicio, nos_expandidos, 0, "Solução não encontrada", arvore, None

def gulosa(estado_inicial, objetivo, tamanho_lado, heuristica_escolhida, gui_mode=False):
    def escolher_heuristica(estado, objetivo, heuristica_escolhida):
        return pecas_fora_do_lugar(estado, objetivo) if heuristica_escolhida == 1 else distancia_manhattan(estado, objetivo)

    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = []
    heapq.heappush(fronteira, (0, estado_inicial_obj))

    visitados = set()
    custo_estado = {tuple(estado_inicial): 0}
    nos_expandidos = 0
    arvore = {tuple(estado_inicial): None}

    while fronteira:
        if time.time() - inicio > TIMEOUT:
            return None, time.time() - inicio, nos_expandidos, 0, "Timeout excedido", arvore, None
        prioridade_atual, estado_atual = heapq.heappop(fronteira)
        estado_tuple = tuple(estado_atual.estado)

        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)

        nos_expandidos += 1
        if nos_expandidos > MAX_NOS:
            fim = time.time()
            return None, fim - inicio, nos_expandidos, 0, "Limite de nós excedido", arvore, None

        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            caminho_estados = exibir_caminho_com_estados(estado_atual, tamanho_lado)
            return caminho, fim - inicio, nos_expandidos, profundidade, caminho_estados, arvore, estado_tuple

        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            filho_tuple = tuple(filho.estado)
            if filho_tuple not in visitados:
                custo_estado[filho_tuple] = filho.profundidade
                heuristica = escolher_heuristica(filho.estado, objetivo, heuristica_escolhida)
                heapq.heappush(fronteira, (heuristica, filho))
                arvore[filho_tuple] = estado_tuple

    fim = time.time()
    return None, fim - inicio, nos_expandidos, 0, "Solução não encontrada", arvore, None