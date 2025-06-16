from uninformed_searches import *

def main():
    print("=== RESOLUÇÃO DO N-PUZZLE ===")

    tamanho = int(input("Escolha o tipo de puzzle:\n3 para 8-puzzle (3x3)\n4 para 15-puzzle (4x4)\n>>> "))
    n = tamanho * tamanho

    if tamanho == 3:
        estado_inicial = [1, 2, 3, 4, 0, 5, 6, 7, 8]
        objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 0]
    elif tamanho == 4:
        estado_inicial = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
        objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    else:
        print("Tamanho inválido.")
        return

    # Mostra os estados escolhidos
    print("\nEstado inicial:")
    for i in range(tamanho):
        print(estado_inicial[i*tamanho:(i+1)*tamanho])

    print("\nEstado objetivo:")
    for i in range(tamanho):
        print(objetivo[i*tamanho:(i+1)*tamanho])

    print("\nEscolha o algoritmo de busca:")
    print("1 - BFS")
    print("2 - DFS")
    print("3 - IDS")
    escolha = int(input(">>> "))

    if escolha == 1:
        bfs(estado_inicial, objetivo, tamanho)
    elif escolha == 2:
        dfs(estado_inicial, objetivo, tamanho)
    elif escolha == 3:
        ids(estado_inicial, objetivo, tamanho)
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
