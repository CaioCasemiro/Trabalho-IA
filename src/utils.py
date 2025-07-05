import random
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from collections import deque
import numpy as np
import tkinter as tk


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
            linha = estado.estado[i * tamanho_lado: (i + 1) * tamanho_lado]
            saida += "\n" + " ".join(str(n).rjust(2) if n != 0 else "  " for n in linha)
    return saida


def reconstruir_caminho(arvore_map, estado_objetivo_tuple):
    caminho = []
    atual = estado_objetivo_tuple
    while atual is not None:
        caminho.append(atual)
        atual = arvore_map.get(atual)
    return caminho[::-1]


def formatar_estado(estado, tamanho):
    linhas = []
    for i in range(tamanho):
        linha = estado[i * tamanho: (i + 1) * tamanho]
        linhas.append(" ".join(str(x) if x != 0 else " " for x in linha))
    return " | ".join(linhas)


def gerar_arvore_busca(arvore_map, estado_objetivo_tuple, tamanho, movimentos=None):
    caminho_solucao = set(reconstruir_caminho(arvore_map, estado_objetivo_tuple))
    filhos_por_pai = {}
    for filho, pai in arvore_map.items():
        if pai not in filhos_por_pai:
            filhos_por_pai[pai] = []
        filhos_por_pai[pai].append(filho)

    def imprimir(no, profundidade=0, prefixo="", visitados=None):
        if visitados is None:
            visitados = set()
        visitados.add(no)
        linhas = []
        is_caminho = no in caminho_solucao
        estado_str = formatar_estado(no, tamanho)
        mov = ""
        if movimentos and no in movimentos:
            mov = f"[{movimentos[no]}]"
        if is_caminho:
            linha = f"{prefixo}*** Prof {profundidade} {mov}: {estado_str} ***"
        else:
            linha = f"{prefixo}Prof {profundidade} {mov}: {estado_str}"
        linhas.append(linha)

        filhos = filhos_por_pai.get(no, [])
        for i, filho in enumerate(filhos):
            if filho in visitados:
                continue
            if i == len(filhos) - 1:
                novo_prefixo = prefixo + "    "
            else:
                novo_prefixo = prefixo + "│   "
            linhas.extend(imprimir(filho, profundidade + 1, novo_prefixo, visitados))
        return linhas

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
    objetivo = list(range(1, tamanho * tamanho))
    objetivo.append(0)
    return objetivo


def validar_estado_inicial(estado, tamanho):
    esperado = set(range(tamanho * tamanho))
    if len(estado) != tamanho * tamanho:
        return False, "Quantidade de peças incorreta."
    if set(estado) != esperado:
        return False, f"Os números devem ser de 0 a {tamanho * tamanho - 1} sem repetições."

    def contar_inversoes(seq):
        seq = [x for x in seq if x != 0]
        inv = 0
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                if seq[i] > seq[j]:
                    inv += 1
        return inv

    inversoes = contar_inversoes(estado)

    if tamanho % 2 == 1:
        # Se o tamanho for ímpar, número de inversões deve ser par
        if inversoes % 2 != 0:
            return False, "Este puzzle não é solúvel (inversões ímpar)."
    else:
        # Se o tamanho for par, (inversões + linha do 0, contando de baixo) deve ser ímpar
        linha_vazia = tamanho - (estado.index(0) // tamanho)
        if (inversoes + linha_vazia) % 2 == 0:
            return False, "Este puzzle não é solúvel (paridade incorreta para tabuleiro par)."

    return True, ""



def gerar_estado_embaralhado_soluvel(tamanho):
    objetivo = gerar_estado_objetivo(tamanho)
    while True:
        estado = objetivo[:]
        random.shuffle(estado)
        valido, _ = validar_estado_inicial(estado, tamanho)
        if valido:
            return estado


def plotar_arvore_networkx_limitada(arvore_map, estado_objetivo_tuple, tamanho, limite=50, root=None):
    G = nx.DiGraph()
    visitados = set()
    fila = deque()
    contador_nos = 0

    caminho_solucao = set()
    atual = estado_objetivo_tuple
    while atual:
        caminho_solucao.add(atual)
        atual = arvore_map.get(atual)

    raiz = next((n for n, p in arvore_map.items() if p is None), None)
    if raiz is None:
        print("Árvore vazia.")
        return

    fila.append(raiz)
    visitados.add(raiz)

    while fila and contador_nos < limite:
        no = fila.popleft()
        contador_nos += 1
        G.add_node(no)
        for filho, pai in arvore_map.items():
            if pai == no and filho not in visitados:
                G.add_edge(no, filho)
                fila.append(filho)
                visitados.add(filho)
                if contador_nos >= limite:
                    break

    labels = {
        node: "\n".join(
            " ".join(f"{n:2}" if n != 0 else "  " for n in node[i * tamanho:(i + 1) * tamanho])
            for i in range(tamanho)
        ) for node in G.nodes
    }

    pos = hierarchy_pos(G, raiz)

    color_map = ['lightgreen' if node in caminho_solucao else 'lightgray' for node in G.nodes]

    # Criar nova janela Tkinter para exibir o gráfico
    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=1500, ax=ax)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=15, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_family='monospace', ax=ax)
    ax.set_title("Árvore de Busca (limitada)")
    ax.axis('off')
    plt.tight_layout()

    # Exibir gráfico dentro do Tkinter
    window = tk.Toplevel(root)
    window.title("Visualização da Árvore")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    plt.close()


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
    """
    Calcula posição dos nós para visualização hierárquica.
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)

    children = list(G.successors(root))
    if children:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2
        for child in children:
            nextx += dx
            pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap,
                                xcenter=nextx, pos=pos, parent=root)
    return pos