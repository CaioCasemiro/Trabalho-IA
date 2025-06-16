class PuzzleState:
    def __init__ (self, estado, pai=None, movimento=None, profundidade=0):
        self.estado = estado
        self.pai = pai
        self.movimento = movimento
        self.profundidade = profundidade

    def get_posicao_vazia(self):
        return self.estado.index(0)
    
    def gerar_filhos(self, tamanho_lado):
        filhos = []
        idx = self.get_posicao_vazia()
        linha, col = divmod(idx, tamanho_lado)

        movimentos = {
            'cima': (linha -1, col),
            'baixo': (linha +1, col),
            'esquerda': (linha, col -1),
            'direita': (linha, col +1),
        }
        
        for move, (l, c) in movimentos.items():
            if 0 <= l < tamanho_lado and 0 <= c < tamanho_lado:
                novo_idx = l * tamanho_lado + c
                novo_estado = self.estado[:]
                novo_estado[idx], novo_estado[novo_idx] = novo_estado[novo_idx], novo_estado[idx]
                filho = PuzzleState(novo_estado, self, move, self.profundidade + 1)
                filhos.append(filho)

        return filhos
        
    def is_objetivo(self, objetivo):
        return self.estado == objetivo
    
    def caminho(self):
        no = self
        caminho = []
        while no.pai:
            caminho.append(no.movimento)
            no = no.pai
        return caminho[::-1]
    
    def __eq__(self, other):
        return self.estado == other.estado
    
    def __hash__(self):
        return hash(tuple(self.estado))
    
    def __lt__(self, outro):
        return True