import pygame
from chess_engine.constants import *

class Label:
    def __init__(self, x, y, text=''):
        """
        Inicijalizuje Label objekat.
        
        :param x: X koordinata (gornji levi ugao)
        :param y: Y koordinata (gornji levi ugao)
        :param font: Font za prikazivanje teksta (pygame.font.Font objekat)
        :param text: Tekst koji će biti prikazan
        """
        self.x = x*SQUARE_SIZE
        self.y = y*SQUARE_SIZE
        self.font = pygame.font.SysFont("Palatino", 32)
        # self.text = text
        self.color = (139, 69, 19)  # Podrazumevana crna boja

        self.set_text(text)
    
    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (self.x, self.y)
    
    def set_color(self, color):
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (self.x, self.y)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.text_rect.topleft = (self.x, self.y)
    
    def draw(self, surface):    
        surface.blit(self.text_surface, self.text_rect)