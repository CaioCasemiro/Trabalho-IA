import random

def exibir_caminho_com_estados(estado_final, tamanho_lado):
    caminho = []
    atual = estado_final
    while atual:
        caminho.append(atual)
        atual = atual.pai
    caminho.reverse()
    saida = "\n--- Caminho de estados (do inicial ao objetivo) ---"
    for idx, estado in enumerate(caminho):
        saida += f"\nPasso {idx}: Movimento = {estado.movimento}"
        for i in range(tamanho_lado):
            linha = estado.estado[i*tamanho_lado:(i+1)*tamanho_lado]
            saida += "\n" + " ".join(str(n).rjust(2) if n != 0 else "  " for n in linha)
    return saida

def reconstruir_caminho(arvore_map, estado_objetivo_tuple):
    """
    Retorna a lista de estados (tuples) do caminho solução do inicial ao objetivo.
    """
    caminho = []
    atual = estado_objetivo_tuple
    while atual is not None:
        caminho.append(atual)
        atual = arvore_map.get(atual)
    return caminho[::-1]

def formatar_estado(estado, tamanho):
    """
    Retorna uma string formatada do tabuleiro em linhas.
    """
    linhas = []
    for i in range(tamanho):
        linha = estado[i*tamanho:(i+1)*tamanho]
        linhas.append(" ".join(str(x) if x != 0 else " " for x in linha))
    return " | ".join(linhas)

def gerar_arvore_busca(arvore_map, estado_objetivo_tuple, tamanho, movimentos=None):
    """
    Gera uma representação textual estruturada da árvore de busca.
    - arvore_map: dict filho_tuple -> pai_tuple
    - estado_objetivo_tuple: tuple do objetivo
    - tamanho: lado do puzzle (3, 4, 5)
    - movimentos: dict filho_tuple -> movimento (opcional, para mostrar o movimento que levou ao nó)
    """
    # Reconstrói o caminho solução para destacar
    caminho_solucao = set(reconstruir_caminho(arvore_map, estado_objetivo_tuple))

    # Constrói a árvore reversa: pai -> [filhos]
    filhos_por_pai = {}
    for filho, pai in arvore_map.items():
        if pai not in filhos_por_pai:
            filhos_por_pai[pai] = []
        filhos_por_pai[pai].append(filho)

    # Função recursiva para imprimir a árvore
    def imprimir(no, profundidade=0, prefixo="", visitados=None):
        if visitados is None:
            visitados = set()
        visitados.add(no)
        linhas = []
        is_caminho = no in caminho_solucao
        estado_str = formatar_estado(no, tamanho)
        mov = ""
        if movimentos and no in movimentos:
            mov = f" [{movimentos[no]}]"
        destaque = "*** " if is_caminho else ""
        linha = f"{prefixo}{destaque}Prof {profundidade}{mov}: {estado_str}{' ***' if is_caminho else ''}"
        linhas.append(linha)
        filhos = filhos_por_pai.get(no, [])
        for i, filho in enumerate(filhos):
            if filho in visitados:
                continue
            if i == len(filhos) - 1:
                novo_prefixo = prefixo + "└── "
            else:
                novo_prefixo = prefixo + "├── "
            linhas.extend(imprimir(filho, profundidade+1, novo_prefixo, visitados))
        return linhas

    # Raiz é o nó cujo pai é None
    raiz = None
    for filho, pai in arvore_map.items():
        if pai is None:
            raiz = filho
            break
    if raiz is None:
        return "Árvore vazia ou não encontrada."

    linhas = imprimir(raiz)
    return "\n".join(linhas)

def gerar_estado_objetivo(tamanho):
    objetivo = list(range(1, tamanho*tamanho))
    objetivo.append(0)
    return objetivo

def validar_estado_inicial(estado, tamanho):
    esperado = set(range(tamanho*tamanho))
    if len(estado) != tamanho*tamanho:
        return False, "Quantidade de peças incorreta."
    if set(estado) != esperado:
        return False, f"Os números devem ser de 0 a {tamanho*tamanho-1} sem repetições."
    # Checagem de solubilidade
    def contar_inversoes(seq):
        seq = [x for x in seq if x != 0]
        inv = 0
        for i in range(len(seq)):
            for j in range(i+1, len(seq)):
                if seq[i] > seq[j]:
                    inv += 1
        return inv
    inversoes = contar_inversoes(estado)
    if tamanho % 2 == 1:
        if inversoes % 2 != 0:
            return False, "Este puzzle não é solúvel (paridade de inversões)."
    else:
        linha_vazia = tamanho - (estado.index(0) // tamanho)
        if (linha_vazia % 2 == 0) == (inversoes % 2 == 1):
            return False, "Este puzzle não é solúvel (paridade de inversões e linha do zero)."
    return True, ""

def gerar_estado_embaralhado_soluvel(tamanho):
    objetivo = gerar_estado_objetivo(tamanho)
    while True:
        estado = objetivo[:]
        random.shuffle(estado)
        valido, _ = validar_estado_inicial(estado, tamanho)
        if valido:
            return estado

