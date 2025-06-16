from uninformed_searches import bfs, dfs, ids
from informed_searches import a_estrela, gulosa

def main():
    print("=== RESOLUÇÃO DO N-PUZZLE ===")

    print("\nQual tipo de busca deseja utilizar?")
    print("1 - Busca sem informação")
    print("2 - Busca com informação")
    tipo_busca = int(input(">>> "))

    if tipo_busca == 1:
        print("\nEscolha o tamanho do puzzle:")
        print("3 - 8-puzzle (3x3)")
        print("4 - 15-puzzle (4x4)")
        tamanho = int(input(">>> "))

        if tamanho not in [3, 4]:
            print("Tamanho inválido para busca sem informação.")
            return

        if tamanho == 3:
            estado_inicial = [1, 2, 3, 4, 0, 5, 6, 7, 8]
            objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 0]
        else:
            estado_inicial = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
            objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

        print("\nEscolha o algoritmo:")
        print("1 - Busca em largura")
        print("2 - Busca em profundidade")
        print("3 - Aprofundamento iterativo")
        algoritmo = int(input(">>> "))

        if algoritmo == 1:
            bfs(estado_inicial, objetivo, tamanho)
        elif algoritmo == 2:
            dfs(estado_inicial, objetivo, tamanho)
        elif algoritmo == 3:
            ids(estado_inicial, objetivo, tamanho)
        else:
            print("Opção inválida.")

    elif tipo_busca == 2:
        print("\nEscolha o tamanho do puzzle:")
        print("3 - 8-puzzle (3x3)")
        print("4 - 15-puzzle (4x4)")
        print("5 - 24-puzzle (5x5)")
        tamanho = int(input(">>> "))

        if tamanho == 3:
            estado_inicial = [1, 2, 3, 4, 0, 5, 6, 7, 8]
            objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 0]
        elif tamanho == 4:
            estado_inicial = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15, 12]
            objetivo =       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        elif tamanho == 5:
            estado_inicial = [1, 2, 3, 4, 5,
                              6, 7, 8, 9, 10,
                              11, 12, 13, 14, 15,
                              16, 17, 18, 19, 0,
                              21, 22, 23, 24, 20]
            objetivo =       [1, 2, 3, 4, 5,
                              6, 7, 8, 9, 10,
                              11, 12, 13, 14, 15,
                              16, 17, 18, 19, 20,
                              21, 22, 23, 24, 0]
        else:
            print("Tamanho inválido.")
            return

        print("\nEscolha a heurística:")
        print("1 - Peças fora do lugar")
        print("2 - Distância de Manhattan")
        heuristica_escolhida = int(input(">>> "))

        if heuristica_escolhida not in [1, 2]:
            print("Heurística inválida.")
            return

        print("\nEscolha o algoritmo:")
        print("4 - A*")
        print("5 - Busca Gulosa")
        algoritmo = int(input(">>> "))

        if algoritmo == 4:
            a_estrela(estado_inicial, objetivo, tamanho, heuristica_escolhida)
        elif algoritmo == 5:
            gulosa(estado_inicial, objetivo, tamanho, heuristica_escolhida)
        else:
            print("Opção inválida.")

    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
