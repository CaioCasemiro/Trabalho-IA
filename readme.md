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
- [Recursos Adicionais](#recursos-adicionais)
- [Licença](#licença)

---

## Visão Geral

O objetivo principal é encontrar a sequência de movimentos que transforma uma configuração inicial do tabuleiro em uma configuração objetivo predefinida. O sistema permite comparar diferentes algoritmos de busca quanto à eficiência (tempo, nós expandidos, profundidade da solução) e visualizar o **caminho da solução** de forma textual estruturada, mostrando os estados intermediários.

---

## Funcionalidades

- **Suporte a múltiplos tamanhos de puzzle:**
  - 8-Puzzle (3x3)
  - 15-Puzzle (4x4)
  - 24-Puzzle (5x5) *(para buscas informadas e algumas desinformadas com limites)*

- **Algoritmos de busca implementados:**
  - **Sem informação (Cegos):**
    - Busca em Largura (BFS)
    - Busca em Profundidade (DFS)
    - Busca com Aprofundamento Iterativo (IDS)
  - **Com informação (Heurísticos):**
    - A* (A Estrela)
    - Busca Gulosa (Greedy Best-First Search)

- **Heurísticas admissíveis para buscas informadas:**
  - Número de peças fora do lugar
  - Soma das distâncias de Manhattan das peças até suas posições corretas

- **Interface gráfica (Tkinter):**
  - Seleção do tamanho do puzzle.
  - Inserção manual ou embaralhamento automático de estados iniciais solúveis.
  - Escolha de algoritmo(s) e heurística(s).
  - Limites de nós expandidos e tempo de execução configurados para evitar travamentos em buscas mais complexas.
  - Exibição de métricas detalhadas de desempenho (tempo, nós expandidos, profundidade da solução).
  - Visualização textual do caminho completo da solução (sequência de estados e movimentos).
  - Tabela comparativa dos algoritmos executados para o mesmo estado inicial.

---

## Como Executar o Sistema

### Pré-requisitos

- **Python 3.8 ou superior** (Testado e recomendado com Python 3.12.0) [cite: 96]
- **Tkinter** (geralmente já incluso na instalação padrão do Python)
- Não são necessárias bibliotecas externas além das padrão do Python. [cite: 98, 99]

### Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/CaioCasemiro/Trabalho-IA.git
    cd SeuRepositorioPuzzleSolver # ou o nome da pasta do seu projeto
    ```

2.  **(Opcional) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/Mac:
    source venv/bin/activate
    ```

3.  **Execute a aplicação:**
    ```bash
    python gui.py
    ```

    > **Dica:** Se você encontrar problemas com o Tkinter (por exemplo, "ModuleNotFoundError: No module named 'tkinter'"), pode ser necessário instalá-lo separadamente, dependendo do seu sistema operacional e como o Python foi instalado. Por exemplo, em sistemas baseados em Debian/Ubuntu, use `sudo apt-get install python3-tk`.

### Estrutura dos Arquivos

SeuRepositorioPuzzleSolver/
│
├── gui.py                  # Interface gráfica principal e lógica de interação do usuário.
├── uninformed_searches.py  # Implementações dos algoritmos de busca sem informação (BFS, DFS, IDS).
├── informed_searches.py    # Implementações dos algoritmos de busca com informação (A*, Busca Gulosa).
├── puzzle.py               # Definição da classe PuzzleState, que representa um estado do tabuleiro.
├── heuristics.py           # Funções para cálculo das heurísticas (peças fora do lugar, distância de Manhattan).
├── utils.py                # Funções auxiliares (validação de estado, geração de estados, exibição do caminho).
└── readme.md               # Este arquivo.


---

## Como Utilizar a Interface

### Seleção do Puzzle

- Escolha o tamanho do puzzle (3x3 para 8-Puzzle, 4x4 para 15-Puzzle, 5x5 para 24-Puzzle) no menu suspenso "Tamanho do Puzzle". A grade de entrada será ajustada automaticamente.

### Inserção do Estado Inicial

- Preencha manualmente cada célula da grade de "Estado Inicial" com os números do estado desejado (0 representa o espaço vazio).
- Alternativamente, clique no botão **"Embaralhar"** para gerar um estado inicial solúvel aleatoriamente.

### Escolha do Algoritmo e Heurística

- Selecione o "Tipo de Busca":
    - **"Sem informação"**: Ativa as opções BFS, DFS, IDS.
    - **"Com informação"**: Ativa as opções A* e Busca Gulosa, e permite a escolha da heurística (Peças Fora do Lugar ou Distância de Manhattan).
- Escolha o algoritmo desejado entre as opções disponíveis para o tipo de busca selecionado.

### Execução e Visualização dos Resultados

- Clique em **"Iniciar Busca"** para executar o algoritmo selecionado.
- Durante a execução, um cronômetro será exibido.
- Ao finalizar, os resultados aparecerão na área de texto, incluindo:
  - O caminho da solução, mostrando cada passo e o estado do tabuleiro correspondente.
  - Tempo de execução em segundos, milissegundos e nanossegundos. 
  - Número de nós expandidos durante a busca. 
  - Profundidade da solução (número de movimentos). 
  - A sequência de movimentos (e.g., 'cima', 'baixo', 'esquerda', 'direita').

### Comparação de Algoritmos

- Para comparar algoritmos, você pode executar diferentes buscas para o mesmo estado inicial.
- As métricas de desempenho serão exibidas na área de resultado, permitindo a comparação manual ou a coleta de dados para tabelas externas, como as apresentadas no relatório. 

---

## Detalhes Técnicos

- **Representação dos Estados:** Cada estado do tabuleiro é representado internamente como uma tupla unidimensional de inteiros, com 0 representando o espaço vazio.
- **Custo da Ação:** Cada movimento da peça vazia é considerado um custo uniforme de 1.
- **Condição de Objetivo:** A busca termina quando o estado atual do tabuleiro é idêntico ao estado objetivo predefinido (números em ordem crescente com 0 na última posição).
- **Validação de Solubilidade:** O sistema inclui lógica para validar se um estado inicial é solúvel, impedindo a execução de puzzles insolúveis.
- **Limites de Busca:** Para gerenciar a complexidade e evitar execuções excessivamente longas, os algoritmos têm limites definidos para o número máximo de nós a expandir (1.000.000) e um tempo limite (30 segundos).
- **Otimização de Memória (A* e Gulosa):** Para as buscas informadas, foi implementado um cache para os valores heurísticos, evitando recálculos desnecessários e melhorando o desempenho.

---

## Autores

- Kaio Mourato de Moura 
- Caio Casemiro de Matos Moura

---

## Recursos Adicionais

- **Repositório GitHub:** Para acessar o código-fonte completo e contribuir para o projeto, visite: **[https://github.com/CaioCasemiro/Trabalho-IA]**
- **Vídeo Explicativo no YouTube:** Para uma demonstração e explicação detalhada do sistema, assista ao vídeo em: **[https://www.youtube.com/watch?v=b2caOAh1N5c]**

