from aigyminsper.search.Graph import State
from aigyminsper.search.SearchAlgorithms import BuscaCustoUniforme

class U2(State):

    def __init__(self, bono, adam, larry, edge, lanterna, operator):
        self.bono = bono
        self.adam = adam
        self.larry = larry
        self.edge = edge
        self.lanterna = lanterna
        self.operator = operator
    
    def successors(self):
        successors = []
        
        #edge vai
        if (self.edge == self.lanterna) and (self.edge == False):
            successors.append(U2(self.bono, self.adam, self.larry, True, True, 'Edge vai'))
        if (self.edge == self.lanterna) and (self.edge == True):
            successors.append(U2(self.bono, self.adam, self.larry, False, False, 'Edge volta'))
        
        #bono vai
        if (self.bono == self.lanterna) and (self.bono == False):
            successors.append(U2(True, self.adam, self.larry, self.edge, True, 'Bono vai'))
        if (self.bono == self.lanterna) and (self.bono == True):
            successors.append(U2(False, self.adam, self.larry, self.edge, False, 'Bono volta'))
        
        #adam vai
        if (self.adam == self.lanterna) and (self.adam == False):
            successors.append(U2(self.bono, True, self.larry, self.edge, True, 'Adam vai'))
        if (self.adam == self.lanterna) and (self.adam == True):
            successors.append(U2(self.bono, False, self.larry, self.edge, False, 'Adam volta'))
        
        #larry vai
        if (self.larry == self.lanterna) and (self.larry == False):
            successors.append(U2(self.bono, self.adam, True, self.edge, True, 'Larry vai'))
        if (self.larry == self.lanterna) and (self.larry == True):
            successors.append(U2(self.bono, self.adam, False, self.edge, False, 'Larry volta'))

        #bono, larry vai
        if (self.bono == self.lanterna) and (self.larry == self.lanterna) and (self.bono == False) and (self.larry == False):
            successors.append(U2(True, self.adam, True, self.edge, True, 'Bono, Larry vai'))
        if (self.bono == self.lanterna) and (self.larry == self.lanterna) and (self.bono == True) and (self.larry == True):
            successors.append(U2(False, self.adam, False, self.edge, False, 'Bono, Larry volta'))
        
        #bono, adam vai
        if (self.bono == self.lanterna) and (self.adam == self.lanterna) and (self.bono == False) and (self.adam == False):
            successors.append(U2(True, True, self.larry, self.edge, True, 'Bono, Adam vai'))
        if (self.bono == self.lanterna) and (self.adam == self.lanterna) and (self.bono == True) and (self.adam == True):
            successors.append(U2(False, False, self.larry, self.edge, False, 'Bono, Adam volta'))

        #bono, edge vai
        if (self.bono == self.lanterna) and (self.edge == self.lanterna) and (self.bono == False) and (self.edge == False):
            successors.append(U2(True, self.adam, self.larry, True, True, 'Bono, Edge vai'))
        if (self.bono == self.lanterna) and (self.edge == self.lanterna) and (self.bono == True) and (self.edge == True):
            successors.append(U2(False, self.adam, self.larry, False, False, 'Bono, Edge volta'))

        #edge, larry vai
        if (self.edge == self.lanterna) and (self.larry == self.lanterna) and (self.edge == False) and (self.larry == False):
            successors.append(U2(self.bono, self.adam, True, True, True, 'Edge, Larry vai'))
        if (self.edge == self.lanterna) and (self.larry == self.lanterna) and (self.edge == True) and (self.larry == True):
            successors.append(U2(self.bono, self.adam, False, False, False, 'Edge, Larry volta'))

        #edge, adam vai
        if (self.edge == self.lanterna) and (self.adam == self.lanterna) and (self.edge == False) and (self.adam == False):
            successors.append(U2(self.bono, True, self.larry, True, True, 'Edge, Adam vai'))
        if (self.edge == self.lanterna) and (self.adam == self.lanterna) and (self.edge == True) and (self.adam == True):
            successors.append(U2(self.bono, False, self.larry, False, False, 'Edge, Adam volta'))

        #larry, adam vai
        if (self.larry == self.lanterna) and (self.adam == self.lanterna) and (self.larry == False) and (self.adam == False):
            successors.append(U2(self.bono, True, True, self.edge, True, 'Larry, Adam vai'))
        if (self.larry == self.lanterna) and (self.adam == self.lanterna) and (self.larry == True) and (self.adam == True):
            successors.append(U2(self.bono, False, False, self.edge, False, 'Larry, Adam volta'))
        
        
        
        return successors

    
    def is_goal(self):
        if all([self.bono, self.adam, self.larry, self.edge, self.lanterna]):
            return True
        else:
            return False
    
    
    def description(self):
        return 'U2 implementation'
    
    def cost(self):
        if self.operator == 'Bono vai':
            return 1
        if self.operator == 'Edge vai':
            return 2
        if self.operator == 'Adam vai':
            return 5
        if self.operator == 'Larry vai':
            return 10
        
        if self.operator == 'Bono volta':
            return 1
        if self.operator == 'Edge volta':
            return 2
        if self.operator == 'Adam volta':
            return 5
        if self.operator == 'Larry volta':
            return 10
        
        if self.operator == 'Bono, Edge vai':
            return 2
        if self.operator == 'Bono, Larry vai':
            return 10
        if self.operator == 'Bono, Adam vai':
            return 5
        if self.operator == 'Edge, Larry vai':
            return 10
        if self.operator == 'Edge, Adam vai':
            return 5
        if self.operator == 'Larry, Adam vai':
            return 10
        
        if self.operator == 'Bono, Edge volta':
            return 2
        if self.operator == 'Bono, Larry volta':
            return 10
        if self.operator == 'Bono, Adam volta':
            return 5
        if self.operator == 'Edge, Larry volta':
            return 10
        if self.operator == 'Edge, Adam volta':
            return 5
        if self.operator == 'Larry, Adam volta':
            return 10

    
    def print(self):
        return str(self.operator)
    
    def env(self):
        return self.operator