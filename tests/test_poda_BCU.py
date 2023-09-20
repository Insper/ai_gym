#
# Considerando as implementações: 
#
# - AspiradorPo.py
# - SumOne.py
# - poi.py
#
# Testar o algoritmo: 
#
# 4) Uniform cost search (CustoUniforme)
#
# Com as seguintes configurações de poda: 
#
# - without pruning
# - father-son pruning
# - general pruning
#
#

from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme
from SumOne import SumOne

def test_sumone_without_pruning():
    state = SumOne(1, '', 11)
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    print(f'\nEstado inicial = {state.env()}')
    print(f'Solução = {result.show_path()}')
    assert result.show_path() == " ; +2  ; +2  ; +2  ; +2  ; +2 "
