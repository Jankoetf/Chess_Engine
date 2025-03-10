import pygame
from chess_engine.constants import *

class Button:
    def __init__(self, x, y, width, height, first_image=None, second_image = None, action=None):

        """
        Represents a clickable button in a Pygame application

        Args:
            x (int): The x-coordinate (in grid units) for the button's position.
            y (int): The y-coordinate (in grid units) for the button's position.
            width (int): The width (in grid units) of the button.
            height (int): The height (in grid units) of the button.
            first_image (Surface, optional): The primary image to display on the button.
            second_image (Surface, optional): The secondary image used for toggling button state.
            action (callable, optional): The callback function to be executed when the button is clicked, communicating with state of UI
        """

        self.rect = pygame.Rect(x*SQUARE_SIZE, y*SQUARE_SIZE, width*SQUARE_SIZE, height*SQUARE_SIZE)
        self.pos = (x, y)
        self.image = first_image
        self.first_image = first_image
        self.second_image = second_image
        self.action = action
        self.hovered = False
        self.toggle_button = second_image!=None
    
    def is_clicked(self, pos):
        """Checks if a given position is within the button's boundaries"""
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        """Processes a Pygame event for the button"""
        if self.is_clicked(event.pos) and self.action:
            self.action()

            if self.toggle_button:
                self.image = self.second_image if self.image == self.first_image else self.first_image

            return True
            
        return False
    
    def get_position(self, pos):
        return (pos[1]+1, pos[0]+1)
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        """
        Draws the button's current image onto the specified surface

        Args:
            surface (pygame.Surface): The surface on which to draw the button
        """
        if self.image:
            surface.blit(self.image, self.rect)