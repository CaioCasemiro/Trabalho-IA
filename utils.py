def exibir_caminho_com_estados(estado_final, tamanho_lado):
    caminho = []
    atual = estado_final
    while atual:
        caminho.append(atual)
        atual = atual.pai

    caminho.reverse()

    print("\n--- Caminho de estados (do inicial ao objetivo) ---")
    for idx, estado in enumerate(caminho):
        print(f"\nPasso {idx}: Movimento = {estado.movimento}")
        for i in range(tamanho_lado):
            linha = estado.estado[i*tamanho_lado:(i+1)*tamanho_lado]
            print(" ".join(str(n).rjust(2) if n != 0 else "  " for n in linha))

