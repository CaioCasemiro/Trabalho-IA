def pecas_fora_do_lugar(estado_atual, estado_objetivo):
    return sum(1 for i in range(len(estado_atual)) if estado_atual[i] != 0 and estado_atual[i] != estado_objetivo[i])

def distancia_manhattan(estado_atual, estado_objetivo):
    
    tamanho = int(len(estado_atual) ** 0.5)
    distancia_total = 0

    for i in range(len(estado_atual)):
        if estado_atual[i] != 0:
            valor = estado_atual[i]

            # Posição atual da peça
            linha_atual, coluna_atual = divmod(i, tamanho)

            # Posição correta da peça no estado objetivo
            posicao_correta = estado_objetivo.index(valor)
            linha_correta, coluna_correta = divmod(posicao_correta, tamanho)

            # Distância de Manhattan
            distancia_total += abs(linha_atual - linha_correta) + abs(coluna_atual - coluna_correta)

    return distancia_total