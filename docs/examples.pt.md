# Exemplos

Estes exemplos demonstram como modelar diferentes problemas de busca com o AI
Gym.

## Mundo do aspirador

`VacuumWorldGeneric.py` recebe um arquivo de texto que descreve os cômodos
sujos e a posição inicial do robô. No mapa, `0` significa limpo e `1` significa
sujo.

```text
0;1;1;1
0;0;0;0
1;1;1;1
```

Execute o exemplo com o arquivo de configuração, a linha e a coluna:

```bash
python docs/src/VacuumWorldGeneric.py configuracao.txt 0 0
```

As ações disponíveis movem o robô para a esquerda, direita, cima ou baixo, ou
limpam o cômodo atual. Uma solução válida alcança um estado no qual todos os
cômodos estão limpos.

![Primeiro mapa do mundo do aspirador](img/mundo_ex_1.png)

Outra configuração pode iniciar o robô na linha 2 e coluna 3:

```text
0;1;1;1
0;0;1;1
1;1;1;1
```

```bash
python docs/src/VacuumWorldGeneric.py configuracao.txt 2 3
```

![Segundo mapa do mundo do aspirador](img/mundo_ex_2.png)

[Ver implementação](implementations/VacuumWorldGeneric.md)

## Problema da ponte do U2

Os quatro integrantes do U2 precisam atravessar uma ponte em 17 minutos. É
noite, eles possuem uma lanterna e no máximo duas pessoas podem atravessar
juntas. Bono, Edge, Adam e Larry levam, respectivamente, 1, 2, 5 e 10 minutos.
Uma dupla se move na velocidade da pessoa mais lenta.

O objetivo é levar todas as pessoas e a lanterna para o outro lado com o menor
custo total.

[Ver implementação](implementations/U2.md)

## Quebra-cabeça de 8 peças

O exemplo do quebra-cabeça de 8 peças utiliza A* para organizar as peças
numeradas no estado objetivo.

![Grafo de busca do quebra-cabeça](img/fig03-04.png){ width="400" }

[Ver implementação](implementations/Puzzle8.md)

## Jogo da Velha

O exemplo de Jogo da Velha modela uma partida 3×3 completa para o `MinMax`. O
X é representado por `1` e maximiza a utilidade; O é representado por `-1` e a
minimiza; casas vazias utilizam `0`.

Cada estado armazena um tabuleiro imutável e o próximo jogador. `successors()`
cria um estado para cada casa vazia. `cost()` retorna uma utilidade terminal
alta para uma vitória e uma estimativa baseada nas linhas no limite de
profundidade.

Execute o exemplo a partir da raiz do projeto:

```bash
python -m docs.src.NoughtsNCrosses
```

Para exibir a árvore de decisão, altere a chamada final para
`play(trace=True)`. O MinMax exibe dois níveis por padrão, preservando o
caminho selecionado completo. Aumente `trace_max_depth` apenas para árvores
pequenas.

[Ver implementação](implementations/NoughtsNCrosses.md)
