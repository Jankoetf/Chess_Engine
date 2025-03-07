import pygame

class ManualViewer:
    def __init__(self, image_path, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.scroll_y = 0 
        
        # Učitavanje slike
        try:
            self.image = pygame.image.load(image_path)
            
            # Kreiranje pozadine sa transparencijom
            self.background = pygame.Surface(screen_size, pygame.SRCALPHA)
            self.background.fill((0, 0, 0, 180))  # Crna sa transparencijom

            self.image_width, self.image_height = self.image.get_size()
            self.max_scroll = max(0, self.image_height - self.screen_height)
            
        except Exception as e:
            self.image = None
            self.image_width = self.image_height = 0
            self.max_scroll = 0
        
    def handle_event(self, event):        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Skrol miša nagore
                self.scroll_y = max(0, self.scroll_y - 30)
                return True
            elif event.button == 5:  # Skrol miša nadole
                self.scroll_y = min(self.max_scroll, self.scroll_y + 30)
                return True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_y = max(0, self.scroll_y - 30)
                return True
            elif event.key == pygame.K_DOWN:
                self.scroll_y = min(self.max_scroll, self.scroll_y + 30)
                return True
            elif event.key == pygame.K_PAGEUP:
                self.scroll_y = max(0, self.scroll_y - 200)
                return True
            elif event.key == pygame.K_PAGEDOWN:
                self.scroll_y = min(self.max_scroll, self.scroll_y + 200)
                return True
            
        return False
    
    def draw_1(self, screen):
        screen.blit(self.background, (0, 0))
        
        # Centriranje slike na ekranu
        img_width, img_height = self.image.get_size()
        x_pos = (self.screen_width - img_width) // 2
        y_pos = (self.screen_height - img_height) // 2
        
        # Crtanje slike
        screen.blit(self.image, (x_pos, y_pos))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        # Centriranje slike horizontalno
        x_pos = (self.screen_width - self.image_width) // 2
        
        # Ako je slika manja od ekrana, prikaži je celu centriranu
        if self.image_height <= self.screen_height:
            y_pos = (self.screen_height - self.image_height) // 2
            screen.blit(self.image, (x_pos, y_pos))
        else:
            # Prikazivanje dela slike prema skrolu
            view_height = min(self.screen_height, self.image_height - self.scroll_y)
            
            try:
                # Kreiranje podrektangla za vidljivi deo slike
                view_rect = pygame.Rect(0, self.scroll_y, self.image_width, view_height)
                visible_portion = self.image.subsurface(view_rect)
                screen.blit(visible_portion, (x_pos, 0))
            except ValueError:
                # Sigurnosna alternativa ako subsurface ne uspe
                screen.blit(self.image, (x_pos, -self.scroll_y))
        
        # Crtanje skrol trake ako je slika veća od ekrana
        if self.image_height > self.screen_height:
            self._draw_scrollbar(screen)

    def _draw_scrollbar(self, screen):
        scrollbar_width = 10
        scrollbar_height = self.screen_height - 40
        scrollbar_x = self.screen_width - 20
        scrollbar_y = 20
        
        # Pozadina skrol trake
        pygame.draw.rect(screen, (80, 80, 80), 
                        (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
        
        # Indikator pozicije
        visible_ratio = min(1.0, self.screen_height / self.image_height)
        handle_height = max(30, scrollbar_height * visible_ratio)
        
        if self.max_scroll > 0:
            handle_position = scrollbar_y + (self.scroll_y / self.max_scroll) * (scrollbar_height - handle_height)
        else:
            handle_position = scrollbar_y
        
        # Crtanje indikatora
        pygame.draw.rect(screen, (200, 200, 200), 
                        (scrollbar_x, handle_position, scrollbar_width, handle_height))