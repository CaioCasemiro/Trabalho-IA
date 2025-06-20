import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from uninformed_searches import bfs, dfs, ids
from informed_searches import a_estrela, gulosa
from utils import validar_estado_inicial, gerar_estado_objetivo, gerar_estado_embaralhado_soluvel, gerar_arvore_busca

class NPuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Resolvedor n-Puzzle - IA")
        self.geometry("1050x750")
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

        self.build_interface()

    def build_interface(self):
        # Frame Tipo de Busca
        frame_tipo = ttk.Frame(self)
        frame_tipo.pack(pady=5)

        ttk.Label(frame_tipo, text="Tipo de Busca:").pack(side=tk.LEFT)

        self.tipo_busca_var = tk.StringVar(value="Sem Informação")

        rb_sem_info = ttk.Radiobutton(frame_tipo, text="Sem Informação", variable=self.tipo_busca_var, value="Sem Informação", command=self.atualizar_tamanhos)
        rb_com_info = ttk.Radiobutton(frame_tipo, text="Com Informação", variable=self.tipo_busca_var, value="Com Informação", command=self.atualizar_tamanhos)

        rb_sem_info.pack(side=tk.LEFT, padx=5)
        rb_com_info.pack(side=tk.LEFT, padx=5)

        frame_top = ttk.Frame(self)
        frame_top.pack(pady=10)

        ttk.Label(frame_top, text="Tamanho do Puzzle:").pack(side=tk.LEFT)

        self.combo_tamanho = ttk.Combobox(frame_top, state="readonly")
        self.combo_tamanho.pack(side=tk.LEFT, padx=5)
        self.combo_tamanho.bind("<<ComboboxSelected>>", self.atualizar_grid)

        # CRIAR self.frame_grid ANTES de chamar atualizar_tamanhos
        frame_grid = ttk.Frame(self)
        frame_grid.pack(pady=10)
        self.frame_grid = frame_grid
        self.entries_grid = []

        self.atualizar_tamanhos()

        frame_alg = ttk.Frame(self)
        frame_alg.pack(pady=5)

        ttk.Label(frame_alg, text="Algoritmo(s):").pack(side=tk.LEFT)

        self.alg_vars = {}
        for nome in self.algoritmos:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(frame_alg, text=nome, variable=var, command=self.atualizar_heuristica_state)
            cb.pack(side=tk.LEFT, padx=2)
            self.alg_vars[nome] = var

        frame_heur = ttk.Frame(self)
        frame_heur.pack(pady=5)

        ttk.Label(frame_heur, text="Heurística:").pack(side=tk.LEFT)

        self.combo_heur = ttk.Combobox(frame_heur, values=list(self.heuristicas.keys()), state="disabled")
        self.combo_heur.current(0)
        self.combo_heur.pack(side=tk.LEFT, padx=5)

        frame_limite = ttk.Frame(self)
        frame_limite.pack(pady=5)

        ttk.Label(frame_limite, text="Limite de Profundidade (DFS/IDS):").pack(side=tk.LEFT)

        self.entry_limite = ttk.Entry(frame_limite, width=5)
        self.entry_limite.insert(0, "50")
        self.entry_limite.pack(side=tk.LEFT, padx=5)

        self.btn_embaralhar = ttk.Button(self, text="Embaralhar", command=self.embaralhar_estado)
        self.btn_embaralhar.pack(pady=2)

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

        self.txt_arvore = scrolledtext.ScrolledText(self.tab_arvore, width=110, height=30, font=("Consolas", 10))
        self.txt_arvore.pack(padx=5, pady=5, fill="both", expand=True)

        self.tree_comp = ttk.Treeview(self.tab_comparativo, columns=("Algoritmo", "Heurística", "Tempo", "Nós", "Profundidade"), show="headings")
        for col in self.tree_comp["columns"]:
            self.tree_comp.heading(col, text=col)
            self.tree_comp.column(col, width=120)
        self.tree_comp.pack(expand=True, fill="both", padx=5, pady=5)

    def atualizar_heuristica_state(self):
        if self.alg_vars["A*"].get() or self.alg_vars["Gulosa"].get():
            self.combo_heur.config(state="readonly")
        else:
            self.combo_heur.config(state="disabled")

    def atualizar_tamanhos(self):
        if self.tipo_busca_var.get() == "Sem Informação":
            tamanhos_disponiveis = ["8-puzzle (3x3)", "15-puzzle (4x4)"]
        else:
            tamanhos_disponiveis = ["8-puzzle (3x3)", "15-puzzle (4x4)", "24-puzzle (5x5)"]

        self.combo_tamanho["values"] = tamanhos_disponiveis
        self.combo_tamanho.current(0)
        self.atualizar_grid()

    def atualizar_grid(self, event=None):
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        self.entries_grid.clear()

        tamanho = int(self.combo_tamanho.get().split("(")[1][0])

        for i in range(tamanho):
            linha = []
            for j in range(tamanho):
                e = ttk.Entry(self.frame_grid, width=3, font=("Consolas", 14), justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                linha.append(e)
            self.entries_grid.append(linha)

        estado_padrao = list(range(1, tamanho * tamanho))
        estado_padrao.append(0)

        for idx, val in enumerate(estado_padrao):
            i, j = divmod(idx, tamanho)
            self.entries_grid[i][j].delete(0, tk.END)
            self.entries_grid[i][j].insert(0, str(val))

    def ler_estado_inicial(self):
        tamanho = int(self.combo_tamanho.get().split("(")[1][0])
        estado = []
        for i in range(tamanho):
            for j in range(tamanho):
                val = self.entries_grid[i][j].get()
                if not val.isdigit():
                    return None
                estado.append(int(val))
        return estado

    def embaralhar_estado(self):
        tamanho = int(self.combo_tamanho.get().split("(")[1][0])
        estado = gerar_estado_embaralhado_soluvel(tamanho)
        for idx, val in enumerate(estado):
            i, j = divmod(idx, tamanho)
            self.entries_grid[i][j].delete(0, tk.END)
            self.entries_grid[i][j].insert(0, str(val))

    def executar_busca(self):
        self.txt_resultados.delete("1.0", tk.END)
        self.txt_arvore.delete("1.0", tk.END)

        tamanho = int(self.combo_tamanho.get().split("(")[1][0])
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
        heuristica = self.heuristicas.get(heuristica_nome, 1)
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
                self.txt_arvore.delete("1.0", tk.END)
                self.txt_arvore.insert(tk.END, "Árvore não gerada (sem solução).\n")
                continue

            caminho, tempo, nos_expandidos, profundidade, arvore_txt, arvore, estado_objetivo_tuple = resultado

            self.txt_resultados.insert(tk.END, f"Tempo de execução: {tempo:.4f} s\n")
            self.txt_resultados.insert(tk.END, f"Nós expandidos: {nos_expandidos}\n")
            self.txt_resultados.insert(tk.END, f"Profundidade da solução: {profundidade}\n")
            self.txt_resultados.insert(tk.END, f"Sequência de movimentos: {caminho}\n")
            self.txt_resultados.insert(tk.END, "-"*60 + "\n")

            resultados_comp.append((alg_nome, heuristica_nome if alg_nome in ["A*", "Gulosa"] else "-", f"{tempo:.4f}", nos_expandidos, profundidade))

            self.txt_arvore.delete("1.0", tk.END)
            arvore_str = gerar_arvore_busca(arvore, estado_objetivo_tuple, tamanho)
            self.txt_arvore.insert(tk.END, arvore_str)

        for i in self.tree_comp.get_children():
            self.tree_comp.delete(i)
        for r in resultados_comp:
            self.tree_comp.insert("", tk.END, values=r)

def main():
    app = NPuzzleGUI()
    app.mainloop()
