import pygame
from chess_engine.constants import *

class Label:
    def __init__(self, x, y, text=''):
        """
        Initializes a Label object

        Args:
            x (int): The x-coordinate of the label's top-left corner in grid units.
            y (int): The y-coordinate of the label's top-left corner in grid units.
            text (str, optional): The text to be displayed on the label. Defaults to an empty string.
        
        The coordinates are scaled by SQUARE_SIZE, for easier use.
        """

        self.x = x*SQUARE_SIZE
        self.y = y*SQUARE_SIZE
        self.font = pygame.font.SysFont("Palatino", 32)
        self.color = (139, 69, 19)

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
        """
        Draws the label on the specified Pygame surface

        Args:
            surface (pygame.Surface): The surface on which the label will be rendered
        """
        surface.blit(self.text_surface, self.text_rect)