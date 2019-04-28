#Donald Quick
#Cptr 215 - Lab13
from unoCard import UnoCard
from unoPlayer import UnoPlayer
import random
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as messagebox

class gameWindow(tk.Frame):
    def __init__(self, parent, players):
        #A setup to use images for buttons - create class of imageCards
        #from PIL import Image, ImageTk
        #self.image = Image.open("redCard.gif")
        #self.photo1 = ImageTk.PhotoImage(self.image)
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.buttons = []
        self.column = 0
        self.readyCheckFrame = ttk.Frame(self)
        self.turnLabel = ttk.Label(self, text=f"Player 1 turn")
        self.turnLabel.grid(row=1, column=1)

        self.currentCardLabel = ttk.Label(self, text='Current card')
        self.currentCardFrame = ttk.Frame(self)
        self.currentCardLabel.grid(row=2, column=1)
        self.currentCardFrame.grid(row=3, column=1)

        self.cardLabel = ttk.Label(self, text="Cards in your hand")
        self.cardLabel.grid(row=4, column=1)
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.grid(row=5, column=1)
        self.wildcolorFrame = ttk.Frame(self)
        self.generateWildcolorButtons()

        self.players = players
        self.deck = create_deck()
        self.discardPile = []
        self.currentCard = self.drawCard(self.deck)
        self.currentPlayer = self.players[0]
        self.reversed = False
        self.skipped = False
        self.drawn = False
        self.drawn4 = False

        self.passButton = tk.Button(self, text='Skip your turn', command=lambda: self.passTurn())
        self.passButton.grid(row=6, column=1)

        #TODO: add frame to show total amount of cards in each players hands
        # This allows for the functionality of calling uno
        self.allHandsFrame = ttk.Frame(self)

        self.changeCurrentCard(self.currentCard)
        for i in range(len(self.players)):
            self.initHands(players[i])
        self.generateCardButtons(self.currentPlayer.hand)

    def initHands(self, player):
        for i in range(7):
            player + (self.drawCard(self.deck))

    def generateCardButtons(self, range):
        if self.buttons != []:
            self.clearButtons(range)
        else:
            for card in range:
                cardButton = tk.Button(self.buttonFrame, text=str(card), fg=card.color, bg='White', width=10,
                                       command=lambda currentCard=card: self.buttonAction(currentCard))
                self.buttons.append(cardButton)
                cardButton.grid(row=0, column=self.column, sticky='ew')
                self.column += 1

    def clearButtons(self, passthrough):
        for i in self.buttons:
                i.destroy()
                self.buttons.remove(i)
        self.generateCardButtons(passthrough)

    def generateWildcolorButtons(self):
        colorLabel = tk.Label(self.wildcolorFrame, text='Choose wild card color:')
        colorLabel.grid(row=0, column=0)
        colors = ['Gold', 'Green', 'Red', 'Blue'] 
        currentCol = 1
        for color in colors:
            colorButton = tk.Button(self.wildcolorFrame, text=color, fg=f"{color}", width=10,
                                      command=lambda wildColor=color: self.determineWildcolor(wildColor))
            colorButton.grid(row=0, column=currentCol)
            currentCol += 1

    def determineWildcolor(self, color):
        self.currentCard.changeWild(color)
        self.wildcolorFrame.grid_remove()
        self.changeCurrentCard(self.currentCard)
        self.buttonFrame.grid(row=5, column=1)
        self.cardLabel.grid(row=4, column=1)
        self.passButton.grid(row=6, column=1)
        self.nextTurn()

    def buttonAction(self, card):
        if 'Black' in card:
            if 'Draw4' in card:
                self.drawn4 = True
            self.currentPlayer.remove(card, self.currentPlayer.hand.index(card))
            self.changeCurrentCard(card)
            button = self.getButton(card)
            button.destroy()
            self.wildcolorFrame.grid(row=7, column=1)
            self.buttonFrame.grid_remove()
            self.cardLabel.grid_remove()
            self.passButton.grid_remove()
        elif card.playedOn(self.currentCard):
            if 'Reverse' in card:
                self.reversed = not(self.reversed)
            self.currentPlayer.remove(card, self.currentPlayer.hand.index(card))
            self.changeCurrentCard(card)
            button = self.getButton(card)
            button.destroy()
            self.buttons.remove(button)
            if 'Skip' in card:
                self.skipped = True
            if 'Draw' in card:
                self.drawn = True
            self.nextTurn()
        else:
            messagebox.showinfo("Incorrect match", "Incorrect card match! Please match by card type or color. "
                                    + "If you can't, skip your turn")

    def changeCurrentCard(self, card):
        if len(self.deck) == 0:
            for i in range(len(self.discardPile)):
                self.deck.append(self.discardPile[i])
            self.discardPile = []
        if 'Wild' in card: #To make sure you add the true wild cards and not fake - ex: (Green, Wild)
            self.discardPile.append(UnoCard('Black', 'Wild'))
        elif 'Draw4' in card:
            self.discardPile.append(UnoCard('Black', 'Draw4'))
        else:
            self.discardPile.append(card)
        cardButton = tk.Button(self.currentCardFrame, text=str(card), fg=card.color)
        cardButton.grid(row=0, column=0, sticky='ew')
        self.currentCard = card

    def addCard(self):
        self.currentPlayer + self.drawCard(self.deck)
        self.generateCardButtons(self.currentPlayer.hand)

    def getButton(self, card):
        for button in self.buttons:
            if button['text'] == str(card) and button['fg'].startswith(card.color):
                return button

    def nextTurn(self):
        if len(self.currentPlayer.hand) == 0:
            self.playerWon()
        else: 
            #TODO: Clean this up
            if self.reversed == False:
                if self.players.index(self.currentPlayer) + 1 == len(self.players):
                    self.currentPlayer = self.players[0]
                    self.turnLabel.config(text = f"Player 1 turn")
                else:
                    self.currentPlayer = self.players[self.players.index(self.currentPlayer) + 1]
                    self.turnLabel.config(text = f"Player {self.players.index(self.currentPlayer) + 1} turn")
                self.generateCardButtons(self.currentPlayer.hand)
            else: #Going in reverse
                if self.players.index(self.currentPlayer) == 0:
                    self.currentPlayer = self.players[len(self.players) - 1]
                    self.turnLabel.config(text = f"Player {self.players.index(self.currentPlayer) + 1} turn")
                else:
                    self.currentPlayer = self.players[self.players.index(self.currentPlayer) - 1]
                    self.turnLabel.config(text = f"Player {self.players.index(self.currentPlayer) + 1} turn")
                self.generateCardButtons(self.currentPlayer.hand)
            #checks for the advance cards
            if self.skipped:
                self.skipped = False
                self.nextTurn()
            if self.drawn:
                self.addCard()
                self.addCard()
                self.drawn = False
            if self.drawn4:
                for i in range(4):
                    self.addCard()
                self.drawn4 = False
            self.waitReady() 
    
    def passTurn(self):
        self.addCard()
        self.nextTurn()

    def drawCard(self, deck):
        card = deck[0]
        deck.pop(0)
        return card

    def callUno(self):
        #TODO:functionality when a player pressed the uno button
        pass
    
    def drawOppenentHand(self):
        #TODO: Frame for showing opponents total cards
        pass
    
    def removeScreen(self):
        self.wildcolorFrame.grid_remove()
        self.buttonFrame.grid_remove()
        self.currentCardFrame.grid_remove()
        self.cardLabel.grid_remove()
        self.currentCardLabel.grid_remove()
        self.passButton.grid_remove()
        self.turnLabel.grid_remove()
        

    def returnScreen(self):
        self.buttonFrame.grid(row=5, column=1)
        self.currentCardFrame.grid(row=3, column=1)
        self.cardLabel.grid(row=4, column=1)
        self.currentCardLabel.grid(row=2, column=1)
        self.passButton.grid(row=6, column=1)
        self.turnLabel.grid(row=1, column=1)
        self.readyCheckFrame.grid_remove()
        
    def playerWon(self):
        self.removeScreen()
        self.turnLabel.grid(row=1, column=1)
        self.turnLabel.config(text=f"Player {self.players.index(self.currentPlayer) + 1} won")
        #TODO: Add a replay or quit functionality
        #Mabye a context bar at top able to create new game at anytime

    def waitReady(self):
        self.removeScreen()
        readyButton = tk.Button(self.readyCheckFrame, text=f"Player {self.players.index(self.currentPlayer) + 1} Ready?", 
                                width=50, height=10,command=lambda: self.returnScreen())
        readyButton.grid(row=0, column=0)
        self.readyCheckFrame.grid(row=8, column=1)

class playerInputWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.buttons = []
        self.parent = parent
        self.prompt = ttk.Label(self, text="How many Player?")
        self.prompt.grid(row=0,column=0)
        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.grid(row=1,column=0)
        self.createButtons()

    def createButtons(self):
        column = 0
        for i in range(2, 5):
            choiceButton = tk.Button(self.buttonFrame, text=i, width=10,
                                       command=lambda playerAmount = i: self.startGame(playerAmount))
            self.buttons.append(choiceButton)
            choiceButton.grid(row=0, column=column, sticky='ew')
            column += 1

    def startGame(self, players):
        player1 = UnoPlayer()
        player2 = UnoPlayer()
        player3 = UnoPlayer()
        player4 = UnoPlayer()
        if players == 2:
            players = [player1, player2]
        elif players == 3:
            players = [player1, player2, player3]
        else:
            players = [player1, player2, player3, player4]     
        self.parent.destroy()
        root = tk.Tk()
        gameWindow(root, players).pack(side="top", fill="both", expand=True)
        root.mainloop()

def create_deck():
    deck = []
    for c in ['Red', 'Green', 'Blue', 'Gold']:
        for r in ['0','1','2','3','4','5','6','7','8','9', 'Skip', 'Reverse', 'Draw']:
            if r == '0':
                deck.append(UnoCard(c, r))
            else:
                for i in range(2):
                    deck.append(UnoCard(c, r))
        deck.append(UnoCard('Black', 'Wild'))
        deck.append(UnoCard('Black', 'Draw4'))
    random.shuffle(deck)
    return deck

if __name__ == "__main__":
    playerInput = tk.Tk()
    playerInputWindow(playerInput).pack()
    playerInput.mainloop()
