def pecas_fora_do_lugar(estado, objetivo):
    return sum(1 for i, v in enumerate(estado) if v != 0 and v != objetivo[i])

def distancia_manhattan(estado, objetivo):
    tamanho = int(len(estado) ** 0.5)
    pos_obj = {v: (i//tamanho, i%tamanho) for i, v in enumerate(objetivo)}
    soma = 0
    for idx, val in enumerate(estado):
        if val == 0: continue
        linha, col = divmod(idx, tamanho)
        linha_obj, col_obj = pos_obj[val]
        soma += abs(linha - linha_obj) + abs(col - col_obj)
    return soma