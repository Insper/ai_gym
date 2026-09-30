# Guia do usuário

## Escolhendo uma classe de estado

Um estado representa uma configuração do problema. O método `successors()`
descreve as configurações que podem ser alcançadas a partir dele.

| Classe de estado | Finalidade | Algoritmos típicos |
| --- | --- | --- |
| `State` | Representação básica de espaço de estados ou jogo | BL, BP, aprofundamento iterativo, custo uniforme, MinMax |
| `HeuristicState` | Estado com estimativa de distância ou qualidade | Gananciosa, A*, subida da montanha |
| `CspState` | Estado para satisfação de restrições e problemas estocásticos | Subida da montanha estocástica |

### Estado básico

Implemente a interface `State` para problemas comuns de busca:

```python
from aigyminsper.search.graph import State


class MeuAgente(State):
    def __init__(self, operador, valor):
        super().__init__(operador)
        self.valor = valor

    def successors(self):
        return []  # Retorne estados MeuAgente alcançáveis.

    def is_goal(self):
        return False

    def description(self):
        return "Descrição do problema"

    def cost(self):
        return 1

    def env(self):
        # Este valor deve representar o estado relevante de forma única.
        return str(self.valor)
```

O método `env()` é utilizado pelas estratégias de poda. Dois estados que
devem ser tratados como equivalentes precisam retornar o mesmo valor.

### Estado heurístico

Algoritmos heurísticos também utilizam `h()`:

```python
from aigyminsper.search.graph import HeuristicState


class MeuAgenteHeuristico(HeuristicState):
    # Implemente successors(), is_goal(), description(), cost() e env().

    def h(self):
        return 0  # Estime a distância restante ou a qualidade do estado.
```

`CspState` estende essa interface com `random_state()` quando um algoritmo
local estocástico precisa gerar outro candidato.

## Escolhendo um algoritmo de busca

```python
from aigyminsper.search.search_algorithms import BuscaLargura


state = MeuAgente("", valor_inicial)
result = BuscaLargura().search(state)

if result is not None:
    print(result.show_path())
else:
    print("Sem solução")
```

| Algoritmo | Classe | Tipo de estado | Custo | Heurística | Principal consideração |
| --- | --- | --- | ---: | ---: | --- |
| Busca em largura | `BuscaLargura` | `State` | Não | Não | Pode consumir muita memória |
| Busca em profundidade | `BuscaProfundidade` | `State` | Não | Não | Requer limite de profundidade |
| Aprofundamento iterativo | `BuscaProfundidadeIterativa` | `State` | Não | Não | Repete buscas limitadas por profundidade |
| Custo uniforme | `BuscaCustoUniforme` | `State` | Sim | Não | Aceita custos de ação variados |
| Gananciosa | `BuscaGananciosa` | `HeuristicState` | Não | Sim | Em geral não é ótima |
| A* | `AEstrela` | `HeuristicState` | Sim | Sim | A otimalidade depende da heurística |
| MinMax | `MinMax` | `State` | Utilidade | Opcional | Alterna turnos de maximização e minimização |
| Subida da montanha | `SubidaMontanha` | `HeuristicState` | — | Sim | Pode parar em um ótimo local |
| Subida da montanha estocástica | `SubidaMontanhaEstocastico` | `CspState` | — | Sim | Utiliza busca local aleatória |

## Estratégias de poda

Os algoritmos de busca em grafo aceitam o argumento `pruning`:

```python
result = algorithm.search(state, pruning="general")
```

- `without`: não impede estados repetidos.
- `father-son`: impede o retorno imediato ao estado pai.
- `general`: registra ambientes que já foram gerados.

O comportamento depende de `env()` representar cada estado de forma única.

## MinMax

O MinMax utiliza `start=0` para o jogador maximizador e `start=1` para o
jogador minimizador. O argumento opcional `m` limita a profundidade explorada.

```python
from aigyminsper.search.search_algorithms import MinMax


result = MinMax().search(state, start=0, m=4)
```

Consulte o [exemplo de Jogo da Velha](examples.md#jogo-da-velha) para uma
implementação completa.
