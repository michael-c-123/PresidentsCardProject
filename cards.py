import random
import pygame
import display

rank_dict = {1:"A", 11:"J", 12: "Q", 13:"K", 20: "X"}
rank_words = {1:"ace", 11:"jack", 12:"queen", 13:"king", 20:"joker"}
suit_words = {"S":"spades","C":"clubs","D":"diamonds","H":"hearts","+":"red","-":"black"}

w_img = None 
h_img = None

def init_dimensions(gameDisplay):
    global w_img, h_img
    w_screen = gameDisplay.get_size()[0]
    h_screen = gameDisplay.get_size()[1]

    w_img = int(500*341/w_screen)
    h_img = int(726.0*240.0/h_screen)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        path = "cards/"
        if self.rank > 1 and self.rank <11:
            path += str(self.rank)
        else:
            path += rank_words[self.rank]
        path += "_of_"
        path += suit_words[self.suit] + ".png"
        img = pygame.image.load(path)
        img = pygame.transform.smoothscale(img, (w_img,h_img)) #TODO scale to screen size
        self.img = img
        self.img_button = display.ImageButton(img, (0,0))
    def __str__(self):
        rank_char = self.rank
        if rank_char == 1 or rank_char > 10:
            rank_char = rank_dict[rank_char]
        return str(rank_char) + self.suit
    def correct(val):
        if val == 2:
            return 20
        if val == 1:
            return 14
        return val
    def __lt__(self, other):
        a = Card.correct(self.rank)
        b = Card.correct(other.rank)
        return a < b
    def __gt__(self, other):
        a = Card.correct(self.rank)
        b = Card.correct(other.rank)
        return a > b
    def __eq__(self, other):
        return self.rank == other.rank
    def __ne__(self, other):
        return not self.__eq__(other)
    def __ge__(self,other):
        return self.__eq__(other) or self.__gt__(other)
    def __le__(self,other):
        return self.__eq__(other) or self.__lt__(other)
    def strictly_equals(self,other):
        return self.rank == other.rank and self.suit == other.suit

class Deck:
    def __init__(self):
        self.cards = []
        self.win = None
    def fill(self):
        for rank in range(1,14):
            self.cards.append(Card(rank,"S")) #spades
            self.cards.append(Card(rank,"C")) #clubs
            self.cards.append(Card(rank,"D")) #diamonds
            self.cards.append(Card(rank,"H")) #hearts
        #self.cards.append(Card(20,"-")) #black joker
        #self.cards.append(Card(20,"+")) #red joker
    def shuffle(self):
        random.shuffle(self.cards)
    def push(self, card):
        self.cards.append(card)
    def pop(self):
        return self.cards.pop()
    def peek(self):
        return self.cards[-1]
    def has_card(self,target):
        for card in self.cards:
            if card.strictly_equals(target):
                return True
        return False
    def __str__(self):
        string = ""
        for card in self.cards:
            string+= str(card) + "\n"
        return string
 