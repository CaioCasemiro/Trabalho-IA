class PuzzleState:
    __slots__ = ('estado', 'pai', 'movimento', 'profundidade', '_filhos')

    def __init__(self, estado, pai=None, movimento=None, profundidade=0):
        self.estado = tuple(estado)  
        self.pai = pai
        self.movimento = movimento
        self.profundidade = profundidade
        self._filhos = None  # Cache para filhos

    def get_posicao_vazia(self):
        return self.estado.index(0)

    def gerar_filhos(self, tamanho_lado):
        if self._filhos is None:
            self._filhos = self._calcular_filhos(tamanho_lado)
        return self._filhos

    def _calcular_filhos(self, tamanho_lado):
        filhos = []
        idx = self.get_posicao_vazia()
        linha, col = divmod(idx, tamanho_lado)

        movimentos = {
            'cima': (linha - 1, col),
            'baixo': (linha + 1, col),
            'esquerda': (linha, col - 1),
            'direita': (linha, col + 1),
        }

        for move, (l, c) in movimentos.items():
            if 0 <= l < tamanho_lado and 0 <= c < tamanho_lado:
                novo_idx = l * tamanho_lado + c
                novo_estado = list(self.estado)
                novo_estado[idx], novo_estado[novo_idx] = novo_estado[novo_idx], novo_estado[idx]
                filhos.append(PuzzleState(novo_estado, self, move, self.profundidade + 1))
        return filhos

    def is_objetivo(self, objetivo):
        return self.estado == tuple(objetivo)

    def caminho(self):
        movimentos = []
        atual = self
        while atual.pai:
            movimentos.append(atual.movimento)
            atual = atual.pai
        return movimentos[::-1]

    def __eq__(self, other):
        return self.estado == other.estado

    def __hash__(self):
        return hash(self.estado)

    def __lt__(self, other):
        return False  # necessário para PriorityQueue