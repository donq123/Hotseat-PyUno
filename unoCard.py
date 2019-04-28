#Donald Quick
#Cptr 215 - Lab13

class UnoCard:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank

    def playedOn(self, other):
        if self.color == 'Black' or other.color == 'Black':
            return True
        if self.color == other.color:
            return True
        elif self.rank == other.rank:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.color} {self.rank}"
    
    def __repr__(self):
        return f"UnoCard('{self.color}', '{self.rank}')"
    
    def __contains__(self, search):
        if self.color == search or self.rank == search:
            return True
        else:
            return False
    
    def changeWild(self, color):
        self.color = color
