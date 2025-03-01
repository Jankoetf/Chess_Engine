import pygame
from chess_engine.constants import *

class Button:
    def __init__(self, x, y, width, height, text="", image=None, action=None):
        self.rect = pygame.Rect(x*SQUARE_SIZE, y*SQUARE_SIZE, width*SQUARE_SIZE, height*SQUARE_SIZE)
        self.pos = (x, y)
        self.text = text
        self.image = image
        self.action = action
        self.hovered = False
    
    def is_clicked(self, pos):
        """Proverava da li je pozicija unutar dugmeta."""
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        """Obrađuje događaje koji se odnose na dugme."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_clicked(event.pos) and self.action:
                self.action()
                return True
        return False
    
    def update(self, mouse_pos):
        """Ažurira stanje dugmeta (npr. efekat prelaska)."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        """Crta dugme na zadatoj površini."""
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            color = (100, 100, 200) if self.hovered else (70, 70, 150)
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Ivica
            
            if self.text:
                font = pygame.font.SysFont("Arial", 20)
                text_surf = font.render(self.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.rect.center)
                surface.blit(text_surf, text_rect)