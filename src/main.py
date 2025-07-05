from uninformed_searches import bfs, dfs, ids
from informed_searches import a_estrela, gulosa
from utils import validar_estado_inicial, gerar_estado_objetivo
import sys

def escolher_estado_inicial(tamanho):
    if tamanho == 3:
        return [1, 2, 3, 4, 0, 5, 6, 7, 8]
    elif tamanho == 4:
        return [1, 2, 3, 4,
                5, 6, 7, 8,
                9, 10, 11, 12,
                0, 13, 14, 15]
    elif tamanho == 5:
        return [1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15,
                16, 17, 18, 19, 20,
                21, 22, 0, 23, 24]
    else:
        print("Tamanho inválido.")
        sys.exit()

def main():
    print("Escolha o tamanho do puzzle:")
    print("1 - 8-puzzle (3x3)")
    print("2 - 15-puzzle (4x4)")
    print("3 - 24-puzzle (5x5)")
    op_tam = input("Opção: ")

    tamanho = {'1': 3, '2': 4, '3': 5}.get(op_tam)
    if not tamanho:
        print("Tamanho inválido.")
        return

    estado_inicial = escolher_estado_inicial(tamanho)
    objetivo = gerar_estado_objetivo(tamanho)

    valido, msg = validar_estado_inicial(estado_inicial, tamanho)
    if not valido:
        print("Estado inválido:", msg)
        return

    print("\nTipo de busca:")
    print("1 - Sem informação (BFS, DFS, IDS)")
    print("2 - Com informação (A*, Gulosa)")
    tipo_busca = input("Opção: ")

    heuristica = None
    if tipo_busca == "2":
        print("\nEscolha a heurística:")
        print("1 - Peças fora do lugar")
        print("2 - Distância de Manhattan")
        heuristica = input("Opção: ")
        heuristica = int(heuristica) if heuristica in ["1", "2"] else 2

    if tipo_busca == "1":
        print("\nEscolha o algoritmo:")
        print("1 - BFS")
        print("2 - DFS")
        print("3 - IDS")
        alg = input("Opção: ")
    else:
        print("\nEscolha o algoritmo:")
        print("1 - A*")
        print("2 - Gulosa")
        alg = input("Opção: ")

    print("\nExecutando busca...")
    resultado = None

    if tipo_busca == "1":
        if alg == "1":
            print("Iniciando BFS...")
            resultado = bfs(estado_inicial, objetivo, tamanho, gui_mode=False)
        elif alg == "2":
            print("Iniciando DFS...")
            resultado = dfs(estado_inicial, objetivo, tamanho, limite=50, gui_mode=False)
        elif alg == "3":
            print("Iniciando IDS...")
            resultado = ids(estado_inicial, objetivo, tamanho, limite=50, gui_mode=False)
        else:
            print("Algoritmo inválido.")
            return
    else:
        if alg == "1":
            print("Iniciando A*...")
            resultado = a_estrela(estado_inicial, objetivo, tamanho, heuristica, gui_mode=False)
        elif alg == "2":
            print("Iniciando Gulosa...")
            resultado = gulosa(estado_inicial, objetivo, tamanho, heuristica, gui_mode=False)
        else:
            print("Algoritmo inválido.")
            return

    # Se a busca falhou (ou atingiu limite de nós)
    if resultado is None or resultado[0] is None:
        _, tempo, nos, _, _, _, _ = resultado
        print("\n--- Busca interrompida ---")
        print(f"Tempo: {tempo:.2f} segundos")
        print(f"Nós expandidos: {nos} (pode ter atingido o limite máximo)")
        return

    caminho, tempo, nos, prof, caminho_estados, _, _ = resultado

    print(caminho_estados)

    print("\n--- Resultado ---")
    print(f"Tempo de execução: {tempo:.4f} segundos")
    print(f"Nós expandidos: {nos} {'(atingiu o limite)' if nos >= 1_000_000 else ''}")
    print(f"Profundidade da solução: {prof}")
    print(f"Número de movimentos: {len(caminho)}")
    print(f"Caminho da solução: {caminho}")

if __name__ == "__main__":
    main()
