# Rastreamento gráfico

O recurso de rastreamento exibe a árvore de busca enquanto um algoritmo avalia
e expande estados. Ele requer o executável Graphviz e um backend gráfico do
Matplotlib.

## Instalar o Graphviz

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

## Configurar o backend gráfico

Verifique o backend atual do Matplotlib:

```bash
python -c "import matplotlib; print(matplotlib.get_backend())"
```

Se o comando retornar `Agg`, instale o PyQt6 dentro do ambiente virtual e
selecione o backend Qt:

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

## Ativar o rastreamento

Passe `trace=True` ao chamar o método `search` de um algoritmo:

```python
algorithm = BuscaLargura()
result = algorithm.search(state, trace=True)
```

As opções mais úteis são:

| Opção | Descrição |
| --- | --- |
| `trace_live=True` | Atualiza o grafo durante a busca em vez de reproduzi-lo ao final. |
| `trace_fullscreen=True` | Abre a visualização em tela cheia. |
| `trace_hold_graph=False` | Fecha a visualização quando o rastreamento termina. |
| `trace_delay=0.02` | Define o intervalo, em segundos, entre os quadros da reprodução. |
| `trace_max_depth=2` | Limita a profundidade exibida para algoritmos como o MinMax. |

Por exemplo, a chamada abaixo reproduz um rastreamento com profundidade
limitada e fecha a janela ao final:

```python
result = algorithm.search(
    state,
    trace=True,
    trace_live=False,
    trace_hold_graph=False,
    trace_delay=0.02,
    trace_max_depth=2,
)
```
