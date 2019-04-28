#Donald Quick
#Cptr 215 - Lab13
from unoCard import UnoCard

class UnoPlayer:
    def __init__(self):
        self.hand = []
        
    def __str__(self):
        return f'{self.hand}'
    
    def __repr__(self):
        return 'UnoPlayer()'

    def __add__(self, card):
        self.hand.append(card)
    
    def remove(self, card, index):
        del self.hand[index]

    def calledUno(self):
        if len(self.hand) == 1:
            return True
        return False

    
