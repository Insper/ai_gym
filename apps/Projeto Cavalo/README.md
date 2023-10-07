<h1> Projeto Cavalo e tabuleiro de xadrez </h1>

--------

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/sAi4kKq3)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12159149&assignment_repo_type=AssignmentRepo)

--------

## Como rodar
1. Certifique-se de que o Python3 ou superior está instalado em sua máquina.

2. Clone ou faça download do repositório no seu computador.

3. Acesse a pasta raiz do projeto em seu terminal.

4. Agora, temos que instalar as dependências desse projeto.

    4.1. Ainda no terminal, crie uma um ambiente virtual com o comando:
    - Caso seu sistema operacional seja Windows/Linux: 
    
            `python -m venv env`

    - Caso seu sistema operacional seja MacOS:

            `python3 -m venv env`

    4.2. Após criado o ambiente virtual, ative-o com o comando:
    - Caso seu sistema operacional seja Windows/Linux: 
    
            `env\Scripts\activate.bat`

    - Caso seu sistema operacional seja MacOS:
    
            `source env/bin/activate`

    4.3. Agora, instale as dependências do projeto com o comando:
        
            `pip install -r requirements.txt`

5. Agora, basta rodar o projeto!!!


## Como funciona o projeto:

- `main.py`: nesse arquivo, contém a resoluçâo do problema, sendo mais específico o algoritmo que foi utilizado para solucionar esse problema. Pode ser testado pelo comando:
    ```
    python main.py
    ```

- `knight_visualization.py`: nesse arquivo, contém a solução para o problema de maneira gráfica, ou seja, ele além de conter o algoritmo que irá solucionar o problema, é possível visualizar o mesmo de maneira visual, com o cavalo se movimentando para solcuionar o problema a partir do local que o usuário escolher.

    Para rodar esse arquivo:

    ```
    python knight_visualization.py
    ```

- `test.py`: nesse arquivo, contém os testes para o algoritmo proposto, para testar esse arquivo, você deve rodar os seguintes comandos no terminal:
    ```
    pytest -v test.py
    ```

## Questões que precisam ser respondidas na documentação do exercício:

### O que é relevante representar nos estados do mundo? Como os estados são estruturados (estrutura de dados) e qual o significado dela (dos campos)?
O estado deste problema gira principalmente em torno da configuração atual do tabuleiro (quais células foram visitadas) e da posição atual do cavalo. 

Nesse problema, é relevante representar:

- Posição atual do cavalo: A célula atual do tabuleiro em que o cavalo está posicionado.
- Movimentos já feitos: As posições do tabuleiro que o cavalo já visitou.
A estrutura de dados adotada para representar os estados é uma matriz 2D (board). Cada célula da matriz contém um número inteiro:

- -1: indica que a célula ainda não foi visitada pelo cavalo.
0 a n^2-1: indica a ordem em que a célula foi visitada, sendo n o tamanho do tabuleiro.

Assim, o tabuleiro board fornece uma visão completa do progresso atual do tour do cavalo e dos movimentos que ele já fez.


### Mostre como ficam representados os estados inicial e final segundo a representação adotada.

**Estado Inicial:**
Quando o programa começa e o objeto KnightBoard é criado, o estado inicial é definido:

- board:

    O tabuleiro é inicializado como uma lista 2D onde todas as células contêm o valor -1, indicando que nenhuma célula foi visitada ainda.

    $$\begin{bmatrix}
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    ...&...&...&...&...&...&...&...\\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    \end{bmatrix}$$

- Posição do cavalo:
    No momento da inicialização, a posição do cavalo não é explicitamente definida. No entanto, quando começamos a resolver o problema do Tour do Cavalo, definimos o ponto de partida, digamos (x, y). A célula correspondente no tabuleiro é então definida como 0, indicando o primeiro movimento. Por exemplo, se começarmos no topo esquerdo, o tabuleiro ficaria:

    $$\begin{bmatrix}
    0 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    ...&...&...&...&...&...&...&...\\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    -1 & -1 & -1 & -1 & -1 & -1 & -1 & -1 \\
    \end{bmatrix}$$


**Estado Final:**
O estado final é alcançado quando o cavalo visitou todas as células do tabuleiro uma vez.

- board:

    Cada célula do tabuleiro contém um número inteiro único de 0 a 63 (para um tabuleiro 8x8), indicando a ordem dos movimentos do cavalo. Por exemplo, o tabuleiro após um tour completo do cavalo (começando da célula superior esquerda) pode parecer algo assim (os números exatos podem variar dependendo da solução encontrada):

    $$\begin{bmatrix}
    0 & 33 & 2 & \dots \\
    3 & 18 & \dots & \dots \\
    \vdots & \vdots & \vdots & \vdots \\
    \dots & \dots & 62 & 63 \\
    \end{bmatrix}

- Posição do cavalo:
    No final do tour, a posição do cavalo não é crucial porque ele já visitou todas as células. No entanto, seu último movimento seria em algum lugar no tabuleiro onde o valor da célula é 63 (para um tabuleiro 8x8).


### Quais as operações sobre os estados? (detalhe como cada operação irá alterar os estados e quais as condições para cada operação ser executada)

As operações sobre os estados no problema do "Knight's Tour" são basicamente os movimentos do cavalo no tabuleiro de xadrez. A cada passo, o cavalo tem até 8 possíveis movimentos, mas nem todos são válidos dependendo do estado atual do tabuleiro e da posição do cavalo. Aqui está um resumo das operações e suas condições:

- Operações:

    - Mova o cavalo 2 células na direção horizontal e 1 célula na direção vertical.
    - Mova o cavalo 1 célula na direção horizontal e 2 células na direção vertical.
    - As variações dos dois movimentos acima nas direções opostas também são consideradas (para cobrir todos os 8 possíveis movimentos do cavalo).

<br>

- Condições para as operações:

    - A célula de destino deve estar dentro dos limites do tabuleiro.
    - A célula de destino não deve ter sido visitada anteriormente pelo cavalo (ou seja, a célula deve ter o valor -1).
    - A movimentação deve seguir as regras padrão de movimentação do cavalo no xadrez.

<br>

- Como as operações alteram o estado:

    - A posição atual do cavalo no tabuleiro é atualizada para a nova célula de destino.
    -  A célula de destino é marcada com o número do movimento atual, indicando a ordem dos movimentos do cavalo.
    - A estratégia geral do algoritmo é tentar todos os possíveis movimentos a partir da posição atual do cavalo e, se um movimento levar a uma solução, ele é aceito. Se nenhum movimento levar a uma solução, o algoritmo faz um "backtrack" para tentar outros caminhos.

### Que algoritmo de busca foi utilizado para resolver este problema?

O algoritmo utilizado para resolver o problema do "Knight's Tour" no código fornecido é uma forma de busca em profundidade (Depth-First Search, ou DFS) com "backtracking". Além disso, ele utiliza a Regra de Warnsdorff para priorizar os movimentos, o que torna a busca mais eficiente.

A Regra de Warnsdorff é uma heurística que diz para escolher o próximo movimento do cavalo com base no número de movimentos subsequentes disponíveis. Em outras palavras, o cavalo sempre tenta mover-se para a posição que tem o menor número de movimentos subsequentes possíveis. Essa heurística ajuda a resolver o problema mais rapidamente, pois direciona a busca para os cantos e bordas do tabuleiro mais cedo, que são as posições mais difíceis de serem alcançadas.

Em resumo, o algoritmo é uma combinação de DFS com backtracking e a Regra de Warnsdorff para otimizar a busca.

### A equipe fez uso de heurísticas? Se sim, explique as heurísticas utilizadas.

Sim, A Regra de Warnsdorff! Explicada na questão anterior.

### Uma explicação de como deve ser usada a implementação com exemplos.
Respondido em **"Como funciona o projeto"**.

