import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from uninformed_searches import bfs, dfs, ids
from utils import validar_estado_inicial, gerar_estado_objetivo

class NPuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resolvedor n-Puzzle - IA")
        self.geometry("950x700")
        self.resizable(False, False)
        self.algoritmos = {
            "BFS": bfs,
            "DFS": dfs,
            "IDS": ids,
            "A*": a_estrela,
            "Gulosa": gulosa
        }
        self.heuristicas = {
            "Peças fora do lugar": 1,
            "Distância de Manhattan": 2
        }
        self.tamanhos = {
            "8-puzzle (3x3)": 3,
            "15-puzzle (4x4)": 4,
            "24-puzzle (5x5)": 5
        }
        self.build_interface()

    def build_interface(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(pady=10)
        ttk.Label(frame_top, text="Tamanho do Puzzle:").pack(side=tk.LEFT)
        self.combo_tamanho = ttk.Combobox(frame_top, values=list(self.tamanhos.keys()), state="readonly")
        self.combo_tamanho.current(0)
        self.combo_tamanho.pack(side=tk.LEFT, padx=5)
        self.combo_tamanho.bind("<<ComboboxSelected>>", self.atualizar_grid)

        frame_alg = ttk.Frame(self)
        frame_alg.pack(pady=5)
        ttk.Label(frame_alg, text="Algoritmo(s):").pack(side=tk.LEFT)
        self.alg_vars = {}
        for nome in self.algoritmos:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(frame_alg, text=nome, variable=var)
            cb.pack(side=tk.LEFT, padx=2)
            self.alg_vars[nome] = var

        frame_heur = ttk.Frame(self)
        frame_heur.pack(pady=5)
        ttk.Label(frame_heur, text="Heurística:").pack(side=tk.LEFT)
        self.combo_heur = ttk.Combobox(frame_heur, values=list(self.heuristicas.keys()), state="readonly")
        self.combo_heur.current(0)
        self.combo_heur.pack(side=tk.LEFT, padx=5)

        frame_limite = ttk.Frame(self)
        frame_limite.pack(pady=5)
        ttk.Label(frame_limite, text="Limite de Profundidade (DFS/IDS):").pack(side=tk.LEFT)
        self.entry_limite = ttk.Entry(frame_limite, width=5)
        self.entry_limite.insert(0, "50")
        self.entry_limite.pack(side=tk.LEFT, padx=5)

        self.frame_grid = ttk.Frame(self)
        self.frame_grid.pack(pady=10)
        self.entries_grid = []
        self.atualizar_grid()

        self.btn_executar = ttk.Button(self, text="Executar", command=self.executar_busca)
        self.btn_executar.pack(pady=10)

        self.tabs = ttk.Notebook(self)
        self.tab_resultados = ttk.Frame(self.tabs)
        self.tab_arvore = ttk.Frame(self.tabs)
        self.tab_comparativo = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_resultados, text="Resultados")
        self.tabs.add(self.tab_arvore, text="Árvore de Busca")
        self.tabs.add(self.tab_comparativo, text="Comparativo")
        self.tabs.pack(expand=True, fill="both")

        self.txt_resultados = scrolledtext.ScrolledText(self.tab_resultados, width=110, height=15, font=("Consolas", 10))
        self.txt_resultados.pack(padx=5, pady=5)

        self.txt_arvore = scrolledtext.ScrolledText(self.tab_arvore, width=110, height=15, font=("Consolas", 10))
        self.txt_arvore.pack(padx=5, pady=5)

        self.tree_comp = ttk.Treeview(self.tab_comparativo, columns=("Algoritmo", "Heurística", "Tempo", "Nós", "Profundidade"), show="headings")
        for col in self.tree_comp["columns"]:
            self.tree_comp.heading(col, text=col)
            self.tree_comp.column(col, width=120)
        self.tree_comp.pack(expand=True, fill="both", padx=5, pady=5)

    def atualizar_grid(self, event=None):
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        self.entries_grid.clear()
        tamanho = self.tamanhos[self.combo_tamanho.get()]
        for i in range(tamanho):
            linha = []
            for j in range(tamanho):
                e = ttk.Entry(self.frame_grid, width=3, font=("Consolas", 14), justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                linha.append(e)
            self.entries_grid.append(linha)
        estado_padrao = list(range(1, tamanho*tamanho))
        estado_padrao.append(0)
        for idx, val in enumerate(estado_padrao):
            i, j = divmod(idx, tamanho)
            self.entries_grid[i][j].delete(0, tk.END)
            self.entries_grid[i][j].insert(0, str(val))

    def ler_estado_inicial(self):
        tamanho = self.tamanhos[self.combo_tamanho.get()]
        estado = []
        for i in range(tamanho):
            for j in range(tamanho):
                val = self.entries_grid[i][j].get()
                if not val.isdigit():
                    return None
                estado.append(int(val))
        return estado

    def executar_busca(self):
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_arvore.delete("1.0", tk.END)
        tamanho = self.tamanhos[self.combo_tamanho.get()]
        estado_inicial = self.ler_estado_inicial()
        if estado_inicial is None:
            messagebox.showerror("Erro", "Preencha todos os campos do estado inicial com números.")
            return
        valido, msg = validar_estado_inicial(estado_inicial, tamanho)
        if not valido:
            messagebox.showerror("Estado inválido", msg)
            return
        objetivo = gerar_estado_objetivo(tamanho)
        heuristica_nome = self.combo_heur.get()
        heuristica = self.heuristicas[heuristica_nome]
        limite = self.entry_limite.get()
        try:
            limite = int(limite)
        except:
            limite = 50

        selecionados = [alg for alg, var in self.alg_vars.items() if var.get()]
        if not selecionados:
            messagebox.showwarning("Selecione", "Selecione pelo menos um algoritmo.")
            return

        resultados_comp = []
        for alg_nome in selecionados:
            self.txt_resultados.insert(tk.END, f"\n=== {alg_nome} ===\n")
            if alg_nome in ["A*", "Gulosa"]:
                func = self.algoritmos[alg_nome]
                resultado = func(estado_inicial, objetivo, tamanho, heuristica, gui_mode=True)
            elif alg_nome == "DFS":
                func = self.algoritmos[alg_nome]
                resultado = func(estado_inicial, objetivo, tamanho, limite, gui_mode=True)
            elif alg_nome == "IDS":
                func = self.algoritmos[alg_nome]
                resultado = func(estado_inicial, objetivo, tamanho, limite, gui_mode=True)
            else:
                func = self.algoritmos[alg_nome]
                resultado = func(estado_inicial, objetivo, tamanho, gui_mode=True)
            if resultado is None:
                self.txt_resultados.insert(tk.END, "Nenhuma solução encontrada.\n")
                continue
            caminho, tempo, nos_expandidos, profundidade, arvore_txt = resultado
            self.txt_resultados.insert(tk.END, f"Tempo de execução: {tempo:.4f} s\n")
            self.txt_resultados.insert(tk.END, f"Nós expandidos: {nos_expandidos}\n")
            self.txt_resultados.insert(tk.END, f"Profundidade da solução: {profundidade}\n")
            self.txt_resultados.insert(tk.END, f"Sequência de movimentos: {caminho}\n")
            self.txt_resultados.insert(tk.END, "-"*60 + "\n")
            self.txt_arvore.insert(tk.END, f"\n=== {alg_nome} ===\n")
            self.txt_arvore.insert(tk.END, arvore_txt + "\n")
            resultados_comp.append((alg_nome, heuristica_nome if alg_nome in ["A*", "Gulosa"] else "-", f"{tempo:.4f}", nos_expandidos, profundidade))
        for i in self.tree_comp.get_children():
            self.tree_comp.delete(i)
        for r in resultados_comp:
            self.tree_comp.insert("", tk.END, values=r)

def main():
    app = NPuzzleGUI()
    app.mainloop()
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
from puzzle import PuzzleState
from utils import exibir_caminho_com_estados, gerar_arvore_busca
import time
from collections import deque

def bfs(estado_inicial, objetivo, tamanho_lado, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    fronteira = deque([estado_inicial_obj])
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0

    while fronteira:
        estado_atual = fronteira.popleft()
        nos_expandidos += 1
        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            tempo_exec = fim - inicio
            arvore_txt = gerar_arvore_busca(estado_atual, tamanho_lado)
            if gui_mode:
                return (caminho, tempo_exec, nos_expandidos, profundidade, arvore_txt)
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
                fronteira.append(filho)
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")

def dfs(estado_inicial, objetivo, tamanho_lado, limite=50, gui_mode=False):
    inicio = time.time()
    estado_inicial_obj = PuzzleState(estado_inicial)
    pilha = [(estado_inicial_obj, 0)]
    visitados = set()
    visitados.add(tuple(estado_inicial))
    nos_expandidos = 0

    while pilha:
        estado_atual, prof = pilha.pop()
        nos_expandidos += 1
        if estado_atual.is_objetivo(objetivo):
            fim = time.time()
            caminho = estado_atual.caminho()
            profundidade = estado_atual.profundidade
            tempo_exec = fim - inicio
            arvore_txt = gerar_arvore_busca(estado_atual, tamanho_lado)
            if gui_mode:
                return (caminho, tempo_exec, nos_expandidos, profundidade, arvore_txt)
            print("Objetivo alcançado!")
            print("Sequência de movimentos:", caminho)
            print("Profundidade da solução:", profundidade)
            print("Nós expandidos:", nos_expandidos)
            print(exibir_caminho_com_estados(estado_atual, tamanho_lado))
            return
        if prof < limite:
            filhos = estado_atual.gerar_filhos(tamanho_lado)
            for filho in filhos:
                estado_tuple = tuple(filho.estado)
                if estado_tuple not in visitados:
                    visitados.add(estado_tuple)
                    pilha.append((filho, prof+1))
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")

def ids(estado_inicial, objetivo, tamanho_lado, limite=50, gui_mode=False):
    inicio = time.time()
    for profundidade_max in range(limite+1):
        estado_inicial_obj = PuzzleState(estado_inicial)
        pilha = [(estado_inicial_obj, 0)]
        visitados = set()
        visitados.add(tuple(estado_inicial))
        nos_expandidos = 0
        while pilha:
            estado_atual, prof = pilha.pop()
            nos_expandidos += 1
            if estado_atual.is_objetivo(objetivo):
                fim = time.time()
                caminho = estado_atual.caminho()
                profundidade = estado_atual.profundidade
                tempo_exec = fim - inicio
                arvore_txt = gerar_arvore_busca(estado_atual, tamanho_lado)
                if gui_mode:
                    return (caminho, tempo_exec, nos_expandidos, profundidade, arvore_txt)
                print("Objetivo alcançado!")
                print("Sequência de movimentos:", caminho)
                print("Profundidade da solução:", profundidade)
                print("Nós expandidos:", nos_expandidos)
                print(exibir_caminho_com_estados(estado_atual, tamanho_lado))
                return
            if prof < profundidade_max:
                filhos = estado_atual.gerar_filhos(tamanho_lado)
                for filho in filhos:
                    estado_tuple = tuple(filho.estado)
                    if estado_tuple not in visitados:
                        visitados.add(estado_tuple)
                        pilha.append((filho, prof+1))
    if gui_mode:
        return None
    print("Nenhuma solução encontrada.")