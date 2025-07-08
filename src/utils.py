import random

def exibir_caminho_com_estados(estado_final, tamanho_lado):
    caminho = []
    atual = estado_final
    while atual:
        caminho.append(atual)
        atual = atual.pai
    caminho.reverse()
    saida = "\n--- Caminho de estados (do inicial ao objetivo) ---"
    # Limitar a exibição a 50 passos
    if len(caminho) > 50:
        saida += f"\n[Caminho truncado: {len(caminho)} passos, exibindo os primeiros e últimos 25]"
        # Exibir primeiros 25
        for idx, estado in enumerate(caminho[:25]):
            saida += f"\nPasso {idx}: Movimento = {estado.movimento}"
            for i in range(tamanho_lado):
                linha = estado.estado[i * tamanho_lado: (i + 1) * tamanho_lado]
                saida += "\n" + " ".join(str(n).rjust(2) if n != 0 else "  " for n in linha)
        # Exibir ... para indicar truncamento
        saida += "\n... [caminho intermediário omitido] ..."
        # Exibir últimos 25
        for idx, estado in enumerate(caminho[-25:], start=len(caminho)-25):
            saida += f"\nPasso {idx}: Movimento = {estado.movimento}"
            for i in range(tamanho_lado):
                linha = estado.estado[i * tamanho_lado: (i + 1) * tamanho_lado]
                saida += "\n" + " ".join(str(n).rjust(2) if n != 0 else "  " for n in linha)
    else:
        for idx, estado in enumerate(caminho):
            saida += f"\nPasso {idx}: Movimento = {estado.movimento}"
            for i in range(tamanho_lado):
                linha = estado.estado[i * tamanho_lado: (i + 1) * tamanho_lado]
                saida += "\n" + " ".join(str(n).rjust(2) if n != 0 else "  " for n in linha)
    return saida

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
    """Gera um estado inicial solucionável para o puzzle de tamanho NxN."""
    objetivo = gerar_estado_objetivo(tamanho)
    while True:
        estado = objetivo[:]
        random.shuffle(estado)
        valido, _ = validar_estado_inicial(estado, tamanho)
        if valido:
            return estado


