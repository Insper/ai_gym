from aigyminsper.search.search_algorithms import BuscaCustoUniforme
from aigyminsper.search.graph import State

class U2(State):

    def __init__(self, bono, edge, adam, larry, lanterna, op):
        """
        In the init method, we set the initial variables:
        `bono`, `edge`, `adam`, `larry` and `latern` are booleans where
        False means it is on the left side of the river and
        True means it is on the right side of the river
        op: the operation that led to the current state
            ex: If the state has just started, op = ' '; if a band member moved to other side, op = 'bono'
            if two members moved to the other side op = 'bono:edge' and so on...
        """
        super().__init__(op)
        #
        # para bono, edge, adam, larry e lanterna FALSE significa lado esquerdo do rio
        # TRUE significa lado direito do rio
        #
        self.bono = bono
        self.edge = edge
        self.adam = adam
        self.larry = larry
        self.lanterna = lanterna

    def successors(self):
        """
        When generating the successors, we follow the flow below:
        1 - We create an empty list of successors `sucessors = []`
        2 - We list the possible actions and ask: what conditions must be met to execute an action?
        3 - We create conditional statements for each action
        4 - When a condition is satisfied, we create a new state with the new characteristics resulting from the action and add it to the successors
        5 - We return the successors

        In U2, the flow would be
        1 - `sucessors = []`
        2 - possible action: cross the river, two can cross the river if one is carrying the latern
        3 - for crossing the river verify if the band member is on the same side of the lattern, for each other member on the same side, create a sucessor
            avoiding creating duplicates
        4 - when a band member move alone we set the operation to its name, then we append to the sucessors the next state as the previous,
            but the lattern and the band member that moved negated
            ex: bono moves, append `U2(not self.bono, self.edge, self.adam, self.larry, not self.lanterna, 'bono')
            when a band member move together we set the operation to the name of both with ';' separator, then we append to the sucessors the next state as the previous
            but the lantern and the band members that moved negated
            ex: bone and edge moves, append `U2(not self.bono, not self.edge, self.adam, self.larry, not self.lanterna, 'bono;edge')
        5 - `return sucessors`
        """
        sucessors = []
        if self.bono == self.lanterna:
            sucessors.append(U2(not self.bono, self.edge, self.adam, self.larry, not self.lanterna, 'bono'))
            if self.edge == self.lanterna:
                sucessors.append(U2(not self.bono, not self.edge, self.adam, self.larry, not self.lanterna, 'bono;edge'))
            if self.adam == self.lanterna:
                sucessors.append(U2(not self.bono, self.edge, not self.adam, self.larry, not self.lanterna, 'bono;adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(not self.bono, self.edge, self.adam, not self.larry, not self.lanterna, 'bono;larry'))
        if self.edge == self.lanterna:
            sucessors.append(U2(self.bono, not self.edge, self.adam, self.larry, not self.lanterna, 'edge'))
            if self.adam == self.lanterna:
                sucessors.append(U2(self.bono, not self.edge, not self.adam, self.larry, not self.lanterna, 'edge;adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(self.bono, not self.edge, self.adam, not self.larry, not self.lanterna, 'edge;larry'))
        if self.adam == self.lanterna:
            sucessors.append(U2(self.bono, self.edge, not self.adam, self.larry, not self.lanterna, 'adam'))
            if self.larry == self.lanterna:
                sucessors.append(U2(self.bono, self.edge, not self.adam, not self.larry, not self.lanterna, 'adam;larry'))
        if self.larry == self.lanterna:
            sucessors.append(U2(self.bono, self.edge, self.adam, not self.larry, not self.lanterna, 'larry'))
        return sucessors
    
    def is_goal(self):
        """
        Is goal method checks if a State is the goal state,
        so it returns True if it is the goal state and False otherwise

        In the U2, the goal is that each member and the lanterna is on the right side of the river
        """
        return self.bono & self.edge & self.adam & self.larry & self.lanterna
    
    def description(self):
        """
        Descriptions helps undestand the enviroment the State are basing from,
        In the Vacuum World Generic, the agent is trying to maitain clean all times
        from the world
        """
        return "Problema de custo minimo usando os integrantes da banda U2"
    
    def cost(self):
        """
        The cost() function is the function that dictitate how much resources the agent will use
        to reach this State given an specific action

        In the U2
        bono, edge, adam and larry takes diferent minutes to cross the river
        the quantity of time to cross the river alone is equal to the quantity of time it takes to travel
        the quantity of time to cross the river with two persons is equal to the time taken by the slowest member

        bono takes 1 minute to cross
        edge takes 2 minutes to cross
        adam takes 5 minutes to cross
        larry takes 10 minutes to cross

        The minutes taken to cross is the actual cost to reach this state
        """
        if self.operator == 'bono':
            return 1
        elif self.operator == 'edge':
            return 2
        elif self.operator == 'adam':
            return 5
        elif self.operator == 'larry':
            return 10
        elif self.operator == 'bono;edge':
            return 2
        elif self.operator == 'bono;adam':
            return 5
        elif self.operator == 'bono;larry':
            return 10
        elif self.operator == 'edge;adam':
            return 5
        elif self.operator == 'edge;larry':
            return 10
        elif self.operator == 'adam;larry':
            return 10
    
    def env(self):
        """
        env stands for Enviroment, it is a function that describes the actual
        state using it's variables.

        In the U2, the enviroment is where each of the member is on the river the the cost taken to reach it
        """
        return str(self.bono)+";"+str(self.edge)+";"+str(self.adam)+";"+str(self.larry)+str(self.cost)

def main():
    print('Busca de Custo Uniforme')
    state = U2(False, False, False, False, False, ' ')
    algorithm = BuscaCustoUniforme()
    result = algorithm.search(state)
    if result != None:
        if result.g <= 17:
            print('Achou uma solucao que satisfaz o enunciado')
            print(result.show_path())
            print(result.g)
        else:
            print('Achou uma solucao que NAO satisfaz a restricao de custo')
            print(result.show_path())
            print(result.g)
    else:
        print('Nao achou solucao')

if __name__ == '__main__':
    main()