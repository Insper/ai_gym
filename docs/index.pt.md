# AI Gym

AI Gym é uma biblioteca educacional para aprender os fundamentos de
Inteligência Artificial por meio de problemas de busca e agentes.

## Algoritmos disponíveis

1. Busca em largura
2. Busca em profundidade
3. Busca em aprofundamento iterativo
4. Busca de custo uniforme
5. Busca gananciosa
6. Busca A*
7. Busca adversarial MinMax
8. Subida da montanha
9. Subida da montanha estocástica

Todos os algoritmos de busca compartilham uma interface comum de estado, o que
permite reutilizar a mesma representação de problema com estratégias
compatíveis.

## Instalação

```bash
pip install aigyminsper
```

## Rastreamento gráfico

O recurso de rastreamento exibe a árvore de busca enquanto o algoritmo avalia
os estados. Ele requer o executável Graphviz e um backend gráfico do
Matplotlib.

### Instalar o Graphviz

=== "Windows"

    ```powershell
    winget install graphviz
    where.exe dot
    ```

=== "Debian / Ubuntu / Linux Mint"

    ```bash
    sudo apt update
    sudo apt install graphviz
    which dot
    ```

### Configurar o backend gráfico

Verifique o backend atual do Matplotlib:

```bash
python -c "import matplotlib; print(matplotlib.get_backend())"
```

Se o resultado for `Agg`, instale o PyQt6 e selecione o backend Qt:

```bash
python -m pip install PyQt6
python -c "from PyQt6 import QtWidgets; print('PyQt6 OK')"
```

=== "Windows PowerShell"

    ```powershell
    $env:MPLBACKEND="QtAgg"
    ```

=== "Linux"

    ```bash
    export MPLBACKEND=QtAgg
    ```

### Ativar o rastreamento

```python
algorithm = BuscaLargura()
result = algorithm.search(state, trace=True)
```

As opções úteis incluem `trace_live=True`, `trace_fullscreen=True`,
`trace_hold_graph=False` e `trace_delay=0.02`. O MinMax também aceita
`trace_max_depth` para manter árvores de jogos grandes legíveis.
