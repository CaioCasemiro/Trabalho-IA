# Resolvedor n-Puzzle com Algoritmos de Busca

Este projeto implementa um resolvedor para o clássico problema do n-Puzzle (também conhecido como "quebra-cabeça deslizante") utilizando diversos algoritmos de busca, tanto sem informação quanto com informação. O sistema contará com uma interface gráfica intuitiva desenvolvida em Tkinter para facilitar a interação e a visualização dos resultados.

## Visão Geral do Projeto

O objetivo principal é encontrar a sequência de movimentos que transforma uma configuração inicial do tabuleiro em uma configuração objetivo predefinida. Serão implementados e comparados diferentes algoritmos de busca para analisar sua eficiência em termos de tempo de execução, número de nós expandidos e profundidade da solução.

## Funcionalidades Planejadas

O Resolvedor n-Puzzle oferecerá as seguintes funcionalidades:

### Tipos de Puzzle Suportados
* [cite_start]**8-Puzzle (3x3)** 
* [cite_start]**15-Puzzle (4x4)** 
* [cite_start]**24-Puzzle (5x5)** (Disponível apenas para buscas com informação) 

### Algoritmos de Busca Implementados
O sistema incluirá as seguintes estratégias de busca:

* **Buscas Sem Informação:**
    * [cite_start]Busca em Largura (Breadth-First Search - BFS) 
    * [cite_start]Busca em Profundidade (Depth-First Search - DFS) 
    * [cite_start]Busca com Aprofundamento Iterativo (Iterative Deepening Search - IDS) 

* **Buscas Com Informação:**
    * [cite_start]A* (A Estrela) 
    * [cite_start]Busca Gulosa (Greedy Best-First Search) 

### Heurísticas (para Buscas Com Informação)
[cite_start]As buscas informadas utilizarão as seguintes heurísticas admissíveis: 

* [cite_start]Número de peças fora do lugar 
* [cite_start]Soma das distâncias de Manhattan das peças até suas posições corretas 

### Interface Gráfica do Usuário (GUI)
A interface será desenvolvida utilizando Tkinter e permitirá ao usuário:

* Selecionar o tipo de puzzle (8, 15 ou 24 peças).
* Inserir o estado inicial do tabuleiro de forma interativa ou textual.
* Escolher o tipo de busca (sem informação ou com informação).
* Selecionar o algoritmo de busca específico (BFS, DFS, IDS, A*, Gulosa).
* Selecionar a heurística desejada (para A* e Busca Gulosa).
* Visualizar o progresso da busca (opcional).
* Exibir os resultados da solução de forma clara.

### Saída de Resultados e Análise Comparativa
[cite_start]Para cada execução de um algoritmo, o programa apresentará: 

* [cite_start]A sequência de movimentos realizados para alcançar o objetivo. 
* [cite_start]O número total de passos (profundidade da solução). 
* [cite_start]O tempo de execução do algoritmo. 
* [cite_start]O número de nós/estados expandidos durante a busca. 
* [cite_start]O caminho de busca percorrido, mostrando os estados do tabuleiro a cada passo. 
* [cite_start]Uma representação da árvore de busca gerada, evidenciando o caminho correto (pode ser via estrutura textual ou visual). 

Adicionalmente, o sistema permitirá a comparação das métricas (tempo, nós expandidos, profundidade) entre diferentes algoritmos e heurísticas para o mesmo estado inicial, facilitando a coleta de dados para o relatório.

## Estrutura do Projeto

A organização dos arquivos e diretórios será a seguinte:
n_puzzle_solver/
├── src/
│   ├── init.py               # Pacote Python
│   ├── main.py                   # Ponto de entrada da aplicação GUI
│   ├── gui.py                    # Classes e lógica da interface gráfica (Tkinter)
│   ├── puzzle_logic.py           # Definição da classe PuzzleState e lógica do tabuleiro
│   ├── search_algorithms.py      # Implementação de todos os algoritmos de busca
│   ├── heuristics.py             # Funções de heurística (Manhattan, Peças fora do lugar)
│   └── utils.py                  # Funções utilitárias (validação, exibição de caminhos)
├── tests/                        # (Opcional) Testes unitários para a lógica do puzzle e algoritmos
│   ├── init.py
│   ├── test_puzzle_logic.py
│   └── test_search_algorithms.py
├── assets/                       # (Opcional) Recursos visuais como ícones
│   └── icon.png
├── README.md                     # Este arquivo
├── requirements.txt              # Lista de dependências Python (se houver além do Tkinter)
└── .gitignore                    # Arquivo para o Git, ignorando pastas e arquivos desnecessários

## Como Executar

Para executar o Resolvedor n-Puzzle, siga os passos abaixo:

1.  **Pré-requisitos:**
    * Python 3.x instalado.
    * Tkinter (geralmente já vem com a instalação padrão do Python).

2.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/n_puzzle_solver.git](https://github.com/seu-usuario/n_puzzle_solver.git)
    cd n_puzzle_solver
    ```

3.  **Execute a Aplicação:**
    ```bash
    python src/main.py
    ```

Uma janela da aplicação será aberta, permitindo a interação com o resolvedor do n-Puzzle.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Autor

Kaio Mourato e Caio Casemiro

## Licença

Este projeto está sob a licença [Escolha uma licença, por exemplo, MIT ou GNU GPL].