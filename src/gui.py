import tkinter as tk
from tkinter import ttk, messagebox
import threading, time
from uninformed_searches import bfs, dfs, ids
from informed_searches import a_estrela, gulosa
from utils import validar_estado_inicial, gerar_estado_objetivo, gerar_estado_embaralhado_soluvel

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Solver IA")
        self.tamanho = tk.IntVar(value=3)
        self.tipo_busca = tk.StringVar(value="1")
        self.heuristica = tk.IntVar(value=1)
        self.algoritmo = tk.StringVar(value="1")
        self.cronometro = tk.StringVar(value="00:00.000")
        self.executando = False
        self.resultado = None
        self.entries = []

        self.cores_numeros = {
            0: "#e0e0e0",
            1: "#ff9999", 2: "#99ccff", 3: "#ccffcc", 4: "#ffff99", 5: "#ffccff",
            6: "#d9b3ff", 7: "#ffc299", 8: "#c0c0c0", 9: "#aaffff", 10: "#ffaaff",
            11: "#b3ffb3", 12: "#ffeb99", 13: "#b3b3ff", 14: "#ffb3b3", 15: "#a6e1fa",
            16: "#f5a9bc", 17: "#a9f5d0", 18: "#f2f5a9", 19: "#d0a9f5", 20: "#f5d0a9",
            21: "#a9c4f5", 22: "#c4a9f5", 23: "#a9f5f2", 24: "#e1f5a9"
        }

        self.build_interface()

    def build_interface(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Controles superiores
        top_frame = ttk.Frame(frame)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        ttk.Label(top_frame, text="Tamanho do Puzzle:").pack(side="left", padx=5)
        cb_tam = ttk.Combobox(top_frame, textvariable=self.tamanho, values=[3, 4, 5], state="readonly", width=5)
        cb_tam.pack(side="left", padx=5)
        cb_tam.bind("<<ComboboxSelected>>", self.criar_tabuleiro)
        
        self.btn_embaralhar = ttk.Button(top_frame, text="Embaralhar", command=self.embaralhar)
        self.btn_embaralhar.pack(side="right", padx=5)

        ttk.Label(frame, text="Tipo de Busca:").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(frame, text="Sem informação", variable=self.tipo_busca, value="1", command=self.atualizar_interface).grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Com informação", variable=self.tipo_busca, value="2", command=self.atualizar_interface).grid(row=1, column=2, sticky="w")

        self.frame_alg = ttk.Frame(frame)
        self.frame_alg.grid(row=2, column=0, columnspan=3, sticky="w")

        self.frame_heur = ttk.Frame(frame)
        self.frame_heur.grid(row=3, column=0, columnspan=3, sticky="w")

        self.frame_tabuleiros = ttk.Frame(frame)
        self.frame_tabuleiros.grid(row=4, column=0, columnspan=3, pady=10)

        self.frame_tabuleiro = ttk.LabelFrame(self.frame_tabuleiros, text="Estado Inicial")
        self.frame_tabuleiro.grid(row=0, column=0, padx=10)

        self.frame_tabuleiro_objetivo = ttk.LabelFrame(self.frame_tabuleiros, text="Estado Objetivo")
        self.frame_tabuleiro_objetivo.grid(row=0, column=1, padx=10)

        self.lbl_crono = ttk.Label(frame, textvariable=self.cronometro, font=("Arial", 12, "bold"))
        self.lbl_crono.grid(row=5, column=0, sticky="w")

        self.btn_buscar = ttk.Button(frame, text="Iniciar Busca", command=self.iniciar_busca)
        self.btn_buscar.grid(row=5, column=1, columnspan=2, pady=10)

        self.txt_resultado = tk.Text(frame, height=15, width=70, state="disabled")
        self.txt_resultado.grid(row=6, column=0, columnspan=3, pady=5)

        self.criar_tabuleiro()
        self.atualizar_interface()

    def criar_tabuleiro(self, event=None):
        for widget in self.frame_tabuleiro.winfo_children():
            widget.destroy()
        for widget in self.frame_tabuleiro_objetivo.winfo_children():
            widget.destroy()
        self.entries.clear()
        t = self.tamanho.get()
        estado_padrao = list(range(1, t*t)) + [0]

        for i in range(t):
            linha = []
            for j in range(t):
                val = estado_padrao[i*t + j]
                entry = tk.Entry(self.frame_tabuleiro, width=3, font=("Arial", 12, "bold"), justify="center", bg=self.cores_numeros.get(val, "white"))
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.insert(0, str(val))
                linha.append(entry)
            self.entries.append(linha)

        estado_objetivo = gerar_estado_objetivo(t)
        for i in range(t):
            for j in range(t):
                val = estado_objetivo[i*t + j]
                cor = self.cores_numeros.get(val, "white")
                lbl = tk.Label(self.frame_tabuleiro_objetivo, text=str(val) if val != 0 else "", width=3, height=1, relief="ridge", bg=cor, font=("Arial", 12, "bold"))
                lbl.grid(row=i, column=j, padx=1, pady=1)

    def embaralhar(self):
        """Gera um estado inicial válido e preenche o tabuleiro."""
        tamanho = self.tamanho.get()
        estado_embaralhado = gerar_estado_embaralhado_soluvel(tamanho)
        
        # Preencher as entries com o estado embaralhado
        for i in range(tamanho):
            for j in range(tamanho):
                idx = i * tamanho + j
                valor = estado_embaralhado[idx]
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(valor))
                # Atualizar cor de fundo
                self.entries[i][j].config(bg=self.cores_numeros.get(valor, "white"))

    def atualizar_interface(self):
        for widget in self.frame_alg.winfo_children():
            widget.destroy()
        for widget in self.frame_heur.winfo_children():
            widget.destroy()
        if self.tipo_busca.get() == "1":
            ttk.Radiobutton(self.frame_alg, text="BFS", variable=self.algoritmo, value="1").pack(side=tk.LEFT)
            ttk.Radiobutton(self.frame_alg, text="DFS", variable=self.algoritmo, value="2").pack(side=tk.LEFT)
            ttk.Radiobutton(self.frame_alg, text="IDS", variable=self.algoritmo, value="3").pack(side=tk.LEFT)
        else:
            ttk.Radiobutton(self.frame_alg, text="A*", variable=self.algoritmo, value="1").pack(side=tk.LEFT)
            ttk.Radiobutton(self.frame_alg, text="Gulosa", variable=self.algoritmo, value="2").pack(side=tk.LEFT)
            ttk.Radiobutton(self.frame_heur, text="Peças fora do lugar", variable=self.heuristica, value=1).pack(side=tk.LEFT)
            ttk.Radiobutton(self.frame_heur, text="Distância de Manhattan", variable=self.heuristica, value=2).pack(side=tk.LEFT)

    def obter_estado(self):
        estado = []
        for linha in self.entries:
            for entry in linha:
                try:
                    val = int(entry.get())
                except:
                    val = 0
                estado.append(val)
        return estado

    def iniciar_busca(self):
        if self.executando:
            return
        estado = self.obter_estado()
        tamanho = self.tamanho.get()
        valido, msg = validar_estado_inicial(estado, tamanho)
        if not valido:
            messagebox.showerror("Erro", msg)
            return
        self.executando = True
        self.cronometro.set("00:00.000")
        self.txt_resultado.config(state="normal")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.config(state="disabled")
        self.btn_buscar.config(state="disabled")
        threading.Thread(target=self.executar_busca, args=(estado, tamanho), daemon=True).start()
        self.root.after(10, self.atualizar_cronometro, time.perf_counter())

    def atualizar_cronometro(self, inicio):
        if not self.executando:
            return
        tempo = time.perf_counter() - inicio
        minutos = int(tempo // 60)
        segundos = int(tempo % 60)
        milesimos = int((tempo - int(tempo)) * 1000)
        self.cronometro.set(f"{minutos:02d}:{segundos:02d}.{milesimos:03d}")
        self.root.after(10, self.atualizar_cronometro, inicio)

    def executar_busca(self, estado, tamanho):
        objetivo = gerar_estado_objetivo(tamanho)
        tipo = self.tipo_busca.get()
        alg = self.algoritmo.get()
        heur = self.heuristica.get()
        resultado = None
        try:
            if tipo == "1":
                if alg == "1":
                    resultado = bfs(estado, objetivo, tamanho)
                elif alg == "2":
                    resultado = dfs(estado, objetivo, tamanho)
                elif alg == "3":
                    resultado = ids(estado, objetivo, tamanho)
            else:
                if alg == "1":
                    resultado = a_estrela(estado, objetivo, tamanho, heur)
                elif alg == "2":
                    resultado = gulosa(estado, objetivo, tamanho, heur)
        except Exception as e:
            self.mostrar_resultado(f"Erro durante a busca: {e}")
            self.executando = False
            self.btn_buscar.config(state="normal")
            return

        self.executando = False
        self.btn_buscar.config(state="normal")
        if resultado is None or resultado[0] is None:
            self.mostrar_resultado("Busca não encontrou solução ou limite de nós atingido.")
            return

        caminho, tempo, nos, prof, caminho_estados, arvore, estado_tuple = resultado
        msg = caminho_estados
        msg += "\n\n--- Resultado Detalhado ---\n"
        msg += f"Tempo de execução: {tempo:.9f} segundos\n"
        msg += f"Tempo de execução (ms): {tempo*1000:.6f}\n"
        msg += f"Tempo de execução (ns): {tempo*1e9:.0f}\n"
        msg += f"Nós expandidos: {nos}\n"
        msg += f"Profundidade da solução: {prof}\n"
        msg += f"Número de movimentos: {len(caminho)}\n"
        msg += f"Caminho da solução: {caminho}\n"
        self.mostrar_resultado(msg)

    def mostrar_resultado(self, texto):
        self.txt_resultado.config(state="normal")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, texto)
        self.txt_resultado.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()