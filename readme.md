# Resolvedor n-Puzzle com Algoritmos de Busca

Este projeto implementa um resolvedor para o clássico problema do n-Puzzle (quebra-cabeça deslizante) utilizando diversos algoritmos de busca, tanto sem informação quanto com informação. O sistema possui uma interface gráfica intuitiva desenvolvida em Tkinter, permitindo fácil interação, análise e visualização dos resultados.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Como Executar o Sistema](#como-executar-o-sistema)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação e Execução](#instalação-e-execução)
  - [Estrutura dos Arquivos](#estrutura-dos-arquivos)
- [Como Utilizar a Interface](#como-utilizar-a-interface)
  - [Seleção do Puzzle](#seleção-do-puzzle)
  - [Inserção do Estado Inicial](#inserção-do-estado-inicial)
  - [Escolha do Algoritmo e Heurística](#escolha-do-algoritmo-e-heurística)
  - [Execução e Visualização dos Resultados](#execução-e-visualização-dos-resultados)
  - [Comparação de Algoritmos](#comparação-de-algoritmos)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Autores](#autores)
- [Licença](#licença)

---

## Visão Geral

O objetivo principal é encontrar a sequência de movimentos que transforma uma configuração inicial do tabuleiro em uma configuração objetivo predefinida. O sistema permite comparar diferentes algoritmos de busca quanto à eficiência (tempo, nós expandidos, profundidade da solução) e visualizar a árvore de busca de forma textual estruturada, destacando o caminho solução.

---

## Funcionalidades

- **Suporte a múltiplos tamanhos de puzzle:**
  - 8-Puzzle (3x3)
  - 15-Puzzle (4x4)
  - 24-Puzzle (5x5) *(apenas para buscas informadas)*

- **Algoritmos de busca implementados:**
  - **Sem informação:**
    - Busca em Largura (BFS)
    - Busca em Profundidade (DFS)
    - Busca com Aprofundamento Iterativo (IDS)
  - **Com informação:**
    - A* (A Estrela)
    - Busca Gulosa

- **Heurísticas para buscas informadas:**
  - Número de peças fora do lugar
  - Soma das distâncias de Manhattan das peças até suas posições corretas

- **Interface gráfica (Tkinter):**
  - Seleção do tipo de puzzle
  - Inserção manual ou embaralhamento automático do estado inicial
  - Escolha de algoritmo(s) e heurística
  - Definição do limite de profundidade para DFS/IDS
  - Execução de múltiplos algoritmos em sequência
  - Visualização dos resultados detalhados
  - Visualização textual estruturada da árvore de busca, com destaque do caminho solução
  - Comparação automática dos algoritmos executados

---

## Como Executar o Sistema

### Pré-requisitos

- **Python 3.8 ou superior** (recomendado Python 3.10, 3.11 ou 3.12)
- **Tkinter** (já incluso na maioria das instalações do Python)
- Não são necessárias bibliotecas externas além das padrão do Python

### Instalação e Execução

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/CaioCasemiro/Trabalho-IA.git
    cd n_puzzle_solver
    ```

2. **(Opcional) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3. **Execute a aplicação:**
    ```bash
    python src/main.py
    ```

    > **Dica:** Se aparecer erro de Tkinter, instale o pacote correspondente ao seu sistema operacional.

### Estrutura dos Arquivos

```
Trabalho-IA/
│
├── src/
│   ├── gui.py                  # Interface gráfica principal
│   ├── uninformed_searches.py  # Algoritmos BFS, DFS, IDS
│   ├── informed_searches.py    # Algoritmos A*, Gulosa
│   ├── puzzle.py               # Estrutura do estado do puzzle
│   ├── heuristics.py           # Funções de heurística
│   ├── utils.py                # Funções auxiliares (validação, embaralhamento, árvore textual)
│   ├── main.py                 # Ponto de entrada da aplicação
│
├── readme.md
└── ...
```

---

## Como Utilizar a Interface

### Seleção do Puzzle

- Escolha o tamanho do puzzle (8, 15 ou 24 peças) no topo da janela.
- O grid de entrada será ajustado automaticamente.

### Inserção do Estado Inicial

- Preencha manualmente cada célula do grid com os números do estado inicial desejado.
- Ou clique em **"Embaralhar"** para gerar automaticamente um estado inicial solúvel aleatório.

### Escolha do Algoritmo e Heurística

- Marque um ou mais algoritmos de busca para executar.
- Para A* ou Gulosa, selecione a heurística desejada (combobox será habilitado automaticamente).
- Para DFS/IDS, defina o limite de profundidade se desejar.

### Execução e Visualização dos Resultados

- Clique em **"Executar"** para iniciar a busca.
- Os resultados aparecerão na aba **"Resultados"**, incluindo:
  - Tempo de execução
  - Número de nós expandidos
  - Profundidade da solução
  - Sequência de movimentos
- A aba **"Árvore de Busca"** mostrará uma representação textual estruturada da árvore de busca, com o caminho solução destacado.
  - Cada nó exibe: profundidade, movimento (se aplicável) e o estado do tabuleiro.
  - O caminho correto é destacado com "***" antes e depois da linha.
- A aba **"Comparativo"** mostra uma tabela comparando os algoritmos executados.

### Comparação de Algoritmos

- Execute múltiplos algoritmos para o mesmo estado inicial.
- Compare tempo, nós expandidos e profundidade na aba "Comparativo".

---

## Detalhes Técnicos

- **Árvore de Busca Textual:**  
  A árvore é impressa com indentação e símbolos (├──, └──) para indicar hierarquia. O caminho solução é destacado.  
  Exemplo de nó:
  ```
  *** Prof 3 [CIMA]: 1 2 3 | 4 5 6 | 7 8   ***
  ```
- **Estados Solúveis:**  
  O sistema só permite execução para estados solúveis, validando automaticamente a entrada.
- **Limite de Nós:**  
  Para puzzles grandes, a árvore textual pode ser muito extensa. Use puzzles menores para melhor visualização.

---

## Autores

- Kaio Mourato
- Caio Casemiro

---

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---