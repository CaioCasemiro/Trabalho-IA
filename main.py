from puzzle import PuzzleState
from uninformed_searches import *

def main():
    print("=== RESOLUÇÃO DO N-PUZZLE ===")

    tamanho = int(input("Escolha o tamanho do puzzle:\n3 para 8-puzzle\n4 para 15-puzzle\nn>>> "))
    n = tamanho * tamanho

    print(f"\nDigite os {n} números do estado inicial separados por espaço (use 0 para o espaço vazio):")
    entrada = input("Exemplo (3x3): 1 2 3 4 5 6 7 8 0\n>>> ")
    estado_inicial = [int(x) for x in entrada.strip().split()]

    if len(estado_inicial) != n:
        print(f"Erro: você digitou {len(estado_inicial)} números, mas o puzzle precisa de {n}.")
        return

    objetivo = list(range(1, n)) + [0]

    print("\nEscolha o algoritmo de busca:")
    print("1 - Busca em Largura (BFS)")
    print("2 - Busca em Profundidade (DFS)")
    print("3 - Aprofundamento Iterativo (IDS)")
    print("4 - A* (com heurística)")
    print("5 - Busca Gulosa")
    escolha = int(input(">>> "))

#Terminar a parte que vai executar as buscas

    if escolha == 1:
        bfs(estado_inicial, objetivo, tamanho)
    elif escolha == 2:
        dfs(estado_inicial, objetivo, tamanho)
    elif escolha == 3:
        ids(estado_inicial, objetivo, tamanho)
    else:
        print("Essa opção ainda não está implementada.")

if __name__ == "__main__":
    main()