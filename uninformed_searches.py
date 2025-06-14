from puzzle import PuzzleState
from collections import deque
import time

def bfs (estado_inicial, objetivo, tamanho_lado): #busca em largura
    print("\nExecutando Busca em Largura (BFS)...")

    inicio = time.time()

    estado_inicial_obj = PuzzleState(estado_inicial)

    fronteira = deque([estado_inicial_obj])

    visitados = set()
    visitados.add(tuple(estado_inicial))

    while fronteira:
        estado_atual = fronteira.popleft()

        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            print("\nObjetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Quantidade de passos:", len(caminho))
            print(f"Tempo de execução: {fim - inicio:.4f} segundos")
            print("Profundidade da solução:", estado_atual.profundidade)
            return
        
        filhos = estado_atual.gerar_filhos(tamanho_lado)
        for filho in filhos:
            estado_tuple = tuple(filho.estado)
            if estado_tuple not in visitados:
                visitados.add(estado_tuple)
                fronteira.append(filho)

    print("Nenhuma solução encontrada.")