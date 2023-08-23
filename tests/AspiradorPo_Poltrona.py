from aigyminsper.search.SearchAlgorithms import BuscaProfundidadeIterativa
from aigyminsper.search.Graph import State

class AspiradorPo(State):

    def __init__(self, op, posicao, s_esq, s_dir, s_cima, s_baixo, armchairs: dict):
        self.operator = op
        self.posicao_robo = posicao
        self.situacao_esq = s_esq
        self.situacao_dir = s_dir
        self.situacao_cima = s_cima
        self.situacao_baixo = s_baixo
        self.armchairs = armchairs
    
def successors(self):
    successors = []

    # Check if the room is dirty and not cleaned
    if self.posicao_robo == 'ESQ' and self.situacao_esq == 'SUJO':
        # Check if there is an armchair
        if self.armchairs[self.posicao_robo]:
            # Flip armchair
            flipped_armchairs = self.armchairs.copy()
            flipped_armchairs[self.posicao_robo] = False
            successors.append(AspiradorPo("virar_poltrona", self.posicao_robo, self.situacao_esq, self.situacao_dir, self.situacao_cima, self.situacao_baixo, flipped_armchairs))

            # Clean the room
            cleaned_armchairs = flipped_armchairs.copy()
            cleaned_armchairs[self.posicao_robo] = True
            successors.append(AspiradorPo("limpar", self.posicao_robo, 'LIMPO', self.situacao_dir, self.situacao_cima, self.situacao_baixo, cleaned_armchairs))
            
            # Turn armchair back
            successors.append(AspiradorPo("desvirar_poltrona", self.posicao_robo, 'LIMPO', self.situacao_dir, self.situacao_cima, self.situacao_baixo, self.armchairs))
        else:
            # Clean the room without armchair actions
            cleaned_armchairs = self.armchairs.copy()
            cleaned_armchairs[self.posicao_robo] = True
            successors.append(AspiradorPo("limpar", self.posicao_robo, 'LIMPO', self.situacao_dir, self.situacao_cima, self.situacao_baixo, cleaned_armchairs))

    # Check the other directions
    for direction in ['dir', 'cima', 'baixo']:
        if self.posicao_robo == direction.upper() and getattr(self, f'situacao_{direction}') == 'SUJO':
            successors.append(AspiradorPo("limpar", self.posicao_robo, getattr(self, f'situacao_{direction}'), self.situacao_dir, self.situacao_cima, self.situacao_baixo, self.armchairs))
        
    # Movement directions: esq, dir, cima, baixo
    for direction in ['esq', 'dir', 'cima', 'baixo']:
        if self.posicao_robo != direction.upper():
            successors.append(AspiradorPo(direction, direction.upper(), self.situacao_esq, self.situacao_dir, self.situacao_cima, self.situacao_baixo, self.armchairs))

    return successors

        
    
    def is_goal(self):
        if all(status == 'LIMPO' for status in [self.situacao_dir, self.situacao_esq, self.situacao_cima, self.situacao_baixo]) and self.posicao_robo == "ESQ":
            return True
        return False 

    def cost(self):
        return 1

    def description(self):
        return "Implementa um aspirador de po para 4 quartos"

    def env(self):
        return self.operator


def main():
    armchairs = {'ESQ': True, 'DIR': True, 'CIMA': True, 'BAIXO': True}
    state = AspiradorPo('', 'ESQ', 'SUJO', 'SUJO', 'SUJO', 'SUJO', armchairs)
    algorithm = BuscaProfundidadeIterativa()
    result = algorithm.search(state)
    if result is not None:
        print('Achou!')
        print(result.show_path())
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()
