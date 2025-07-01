import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from uninformed_searches import bfs, dfs, ids
from informed_searches import a_estrela, gulosa
from utils import validar_estado_inicial, gerar_estado_objetivo, gerar_estado_embaralhado_soluvel, reconstruir_caminho, plotar_arvore_networkx_limitada

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
        frame_tipo = ttk.Frame(self)
        frame_tipo.pack(pady=5)

        ttk.Label(frame_tipo, text="Tipo de Busca:").pack(side=tk.LEFT)
        self.tipo_busca_var = tk.StringVar(value="Sem Informação")

        ttk.Radiobutton(frame_tipo, text="Sem Informação", variable=self.tipo_busca_var, value="Sem Informação", command=self.atualizar_interface_algoritmos).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_tipo, text="Com Informação", variable=self.tipo_busca_var, value="Com Informação", command=self.atualizar_interface_algoritmos).pack(side=tk.LEFT, padx=5)

        frame_top = ttk.Frame(self)
        frame_top.pack(pady=10)

        ttk.Label(frame_top, text="Tamanho do Puzzle:").pack(side=tk.LEFT)
        self.combo_tamanho = ttk.Combobox(frame_top, state="readonly")
        self.combo_tamanho.pack(side=tk.LEFT, padx=5)
        self.combo_tamanho.bind("<<ComboboxSelected>>", self.atualizar_grid)

        self.frame_grid = ttk.Frame(self)
        self.frame_grid.pack(pady=10)
        self.entries_grid = []

        self.frame_alg = ttk.Frame(self)
        self.frame_alg.pack(pady=5)

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

        frame_nos = ttk.Frame(self)
        frame_nos.pack(pady=5)
        ttk.Label(frame_nos, text="Limite de nós exibidos na árvore:").pack(side=tk.LEFT)
        self.entry_limite_nos = ttk.Entry(frame_nos, width=6)
        self.entry_limite_nos.insert(0, "100")
        self.entry_limite_nos.pack(side=tk.LEFT, padx=5)

        self.btn_embaralhar = ttk.Button(self, text="Embaralhar", command=self.embaralhar_estado)
        self.btn_embaralhar.pack(pady=2)

        self.btn_executar = ttk.Button(self, text="Executar", command=self.executar_busca)
        self.btn_executar.pack(pady=10)

        self.tabs = ttk.Notebook(self)
        self.tab_resultados = ttk.Frame(self.tabs)
        self.tab_caminho = ttk.Frame(self.tabs)
        self.tab_comparativo = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_resultados, text="Resultados")
        self.tabs.add(self.tab_caminho, text="Caminho até a solução")
        self.tabs.add(self.tab_comparativo, text="Comparativo")
        self.tabs.pack(expand=True, fill="both")

        self.txt_resultados = scrolledtext.ScrolledText(self.tab_resultados, width=110, height=15, font=("Consolas", 10))
        self.txt_resultados.pack(padx=5, pady=5)

        self.btn_arvore = ttk.Button(self.tab_resultados, text="Visualizar Árvore", command=self.visualizar_arvore)
        self.btn_arvore.pack(pady=5)

        self.txt_caminho = scrolledtext.ScrolledText(self.tab_caminho, width=110, height=30, font=("Consolas", 10))
        self.txt_caminho.pack(padx=5, pady=5, fill="both", expand=True)

        self.tree_comp = ttk.Treeview(self.tab_comparativo, columns=("Algoritmo", "Heurística", "Tempo", "Nós", "Profundidade"), show="headings")
        for col in self.tree_comp["columns"]:
            self.tree_comp.heading(col, text=col)
            self.tree_comp.column(col, width=120)
        self.tree_comp.pack(expand=True, fill="both", padx=5, pady=5)

        self.alg_vars = {}
        self.atualizar_tamanhos()
        self.atualizar_interface_algoritmos()

    def atualizar_tamanhos(self):
        tipo = self.tipo_busca_var.get()
        if tipo == "Sem Informação":
            self.combo_tamanho["values"] = ["8-puzzle (3x3)", "15-puzzle (4x4)"]
        else:
            self.combo_tamanho["values"] = ["8-puzzle (3x3)", "15-puzzle (4x4)", "24-puzzle (5x5)"]
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
        estado_padrao = list(range(1, tamanho * tamanho)) + [0]
        for idx, val in enumerate(estado_padrao):
            i, j = divmod(idx, tamanho)
            self.entries_grid[i][j].delete(0, tk.END)
            self.entries_grid[i][j].insert(0, str(val))

    def atualizar_interface_algoritmos(self):
        for widget in self.frame_alg.winfo_children():
            widget.destroy()
        self.alg_vars.clear()
        tipo = self.tipo_busca_var.get()
        if tipo == "Sem Informação":
            visiveis = ["BFS", "DFS", "IDS"]
            self.combo_heur.config(state="disabled")
        else:
            visiveis = ["A*", "Gulosa"]
            self.combo_heur.config(state="readonly")
        for nome in visiveis:
            var = tk.BooleanVar()
            ttk.Checkbutton(self.frame_alg, text=nome, variable=var).pack(side=tk.LEFT, padx=5)
            self.alg_vars[nome] = var
        self.atualizar_tamanhos()

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
        self.txt_caminho.delete("1.0", tk.END)
        tamanho = int(self.combo_tamanho.get().split("(")[1][0])
        estado_inicial = self.ler_estado_inicial()
        if estado_inicial is None:
            messagebox.showerror("Erro", "Preencha todos os campos com números.")
            return
        valido, msg = validar_estado_inicial(estado_inicial, tamanho)
        if not valido:
            messagebox.showerror("Estado inválido", msg)
            return

        objetivo = gerar_estado_objetivo(tamanho)
        heuristica = self.heuristicas.get(self.combo_heur.get(), 1)
        try:
            limite = int(self.entry_limite.get())
        except:
            limite = 50

        selecionados = [alg for alg, var in self.alg_vars.items() if var.get()]
        if not selecionados:
            messagebox.showwarning("Selecione", "Selecione pelo menos um algoritmo.")
            return

        resultados_comp = []

        for alg_nome in selecionados:
            self.txt_resultados.insert(tk.END, f"\n==== {alg_nome} ====\n")
            func = self.algoritmos[alg_nome]
            if alg_nome in ["A*", "Gulosa"]:
                resultado = func(estado_inicial, objetivo, tamanho, heuristica, gui_mode=True)
            elif alg_nome in ["DFS", "IDS"]:
                resultado = func(estado_inicial, objetivo, tamanho, limite, gui_mode=True)
            else:
                resultado = func(estado_inicial, objetivo, tamanho, gui_mode=True)

            if resultado is None:
                self.txt_resultados.insert(tk.END, "Nenhuma solução encontrada.\n")
                self.txt_caminho.insert(tk.END, f"==== {alg_nome} ====\nSem solução encontrada.\n")
                continue

            caminho_mov, tempo, nos_exp, prof, _, arvore, estado_objetivo_tuple = resultado
            self.txt_resultados.insert(tk.END, f"Tempo de execução: {tempo:.4f} s\n")
            self.txt_resultados.insert(tk.END, f"Nós expandidos: {nos_exp}\n")
            self.txt_resultados.insert(tk.END, f"Profundidade da solução: {prof}\n")
            self.txt_resultados.insert(tk.END, f"Sequência de movimentos: {caminho_mov}\n")
            self.txt_resultados.insert(tk.END, "-"*60 + "\n")
            resultados_comp.append((alg_nome, self.combo_heur.get() if alg_nome in ["A*", "Gulosa"] else "-", f"{tempo:.4f}", nos_exp, prof))

            self.txt_caminho.insert(tk.END, f"\n==== {alg_nome} ====\n")
            for i, estado in enumerate(reconstruir_caminho(arvore, estado_objetivo_tuple)):
                self.txt_caminho.insert(tk.END, f"*** Passo {i} ***\n")
                for j in range(tamanho):
                    linha = estado[j * tamanho:(j + 1) * tamanho]
                    self.txt_caminho.insert(tk.END, " ".join(f"{n:2}" if n != 0 else "  " for n in linha) + "\n")
                self.txt_caminho.insert(tk.END, "-" * 30 + "\n")

            self.arvore_atual = arvore
            self.estado_objetivo_atual = estado_objetivo_tuple
            self.tamanho_atual = tamanho

        for i in self.tree_comp.get_children():
            self.tree_comp.delete(i)
        for r in resultados_comp:
            self.tree_comp.insert("", tk.END, values=r)

    def visualizar_arvore(self):
        try:
            limite = int(self.entry_limite_nos.get())
        except:
            limite = 100
        if hasattr(self, 'arvore_atual'):
            plotar_arvore_networkx_limitada(self.arvore_atual, self.estado_objetivo_atual, self.tamanho_atual, limite=limite)

def main():
    app = NPuzzleGUI()
    app.mainloop()
