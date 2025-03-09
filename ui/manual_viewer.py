import pygame

class ManualViewer:
    """
    Provides functionality for displaying a manual image with scrolling support in a Pygame window.
    """
    def __init__(self, image_path, screen_size):
        """
        Initializes the ManualViewer by loading the manual image and setting up the background.

        Args:
            image_path (str): The file path to the manual image.
            screen_size (tuple): A tuple (width, height) representing the dimensions of the screen.
        
        The image is loaded and its dimensions are determined. A semi-transparent background is created,
        and the maximum scroll value is computed based on the image height and screen height.
        """
        self.screen_width, self.screen_height = screen_size
        self.scroll_y = 0 
        
        try:
            self.image = pygame.image.load(image_path)
            
            # Create a background surface with transparency
            self.background = pygame.Surface(screen_size, pygame.SRCALPHA)
            self.background.fill((0, 0, 0, 40))  # Semi-transparent black

            self.image_width, self.image_height = self.image.get_size()
            self.max_scroll = max(0, self.image_height - self.screen_height)
            
        except Exception as e:
            self.image = None
            self.image_width = self.image_height = 0
            self.max_scroll = 0
        
    def handle_event(self, event):
        """
        Processes input events to handle vertical scrolling of the manual.

        The method handles mouse wheel events (scroll up and down) as well as keyboard events
        (UP, DOWN, PAGEUP, PAGEDOWN) to adjust the scroll position accordingly.

        Args:
            event (pygame.event.Event): The event to be processed.
        """    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # # Scroll up
                self.scroll_y = max(0, self.scroll_y - 30)
                return True
            elif event.button == 5:  # Scroll down
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

    def draw(self, screen):
        """
        Draws the manual image on the screen with scrolling support and a scrollbar if needed.

        The method first blits the semi-transparent background overlay, then centers the image horizontally.
        If the image height is less than or equal to the screen height, it is vertically centered.
        Otherwise, a portion of the image determined by the current scroll position is displayed.
        A scrollbar is drawn if the image is taller than the screen.

        Args:
            screen (pygame.Surface): The surface on which to draw the manual.
        """
        screen.blit(self.background, (0, 0))
        
        # Center the image horizontally
        x_pos = (self.screen_width - self.image_width) // 2
        
        if self.image_height <= self.screen_height:
            y_pos = (self.screen_height - self.image_height) // 2
            screen.blit(self.image, (x_pos, y_pos))
        else:
            view_height = min(self.screen_height, self.image_height - self.scroll_y)
            
            try:
                view_rect = pygame.Rect(0, self.scroll_y, self.image_width, view_height)
                visible_portion = self.image.subsurface(view_rect)
                screen.blit(visible_portion, (x_pos, 0))
            except ValueError:
                screen.blit(self.image, (x_pos, -self.scroll_y))
        
        # Draw the scrollbar if the image height exceeds the screen height
        if self.image_height > self.screen_height:
            self._draw_scrollbar(screen)

    def _draw_scrollbar(self, screen):
        """
        Draws a vertical scrollbar to indicate the current scroll position of the manual image.

        The scrollbar is drawn on the right side of the screen. Its handle size and position
        are determined by the ratio of the screen height to the image height and the current scroll offset.

        Args:
            screen (pygame.Surface): The surface on which to draw the scrollbar.
        """
        scrollbar_width = 10
        scrollbar_height = self.screen_height - 40
        scrollbar_x = self.screen_width - 20
        scrollbar_y = 20
        
        pygame.draw.rect(screen, (80, 80, 80), 
                        (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
        
        visible_ratio = min(1.0, self.screen_height / self.image_height)
        handle_height = max(30, scrollbar_height * visible_ratio)
        
        if self.max_scroll > 0:
            handle_position = scrollbar_y + (self.scroll_y / self.max_scroll) * (scrollbar_height - handle_height)
        else:
            handle_position = scrollbar_y
        
        # Draw the scrollbar handle
        pygame.draw.rect(screen, (200, 200, 200), 
                        (scrollbar_x, handle_position, scrollbar_width, handle_height))