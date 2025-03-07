""" class that encapsulates the user interface state of a chess application """
class UiState:
    def __init__(self):
        #app state
        self.show_menu = False #if menu than not table!
        self.show_menu_icons = False
        self.show_manual = False
        
        # game options
        self.board_style, self.n_styles = 0, 3
        self.table_color = False
        self.show_control = False
        self.sound = False
        
        # AI state
        self.ai_black = False
        self.ai_white = False
        self.human_vs_human = True
        self.ai_thinking = False
        
        # square selection
        self.square_selected = ()
        self.squares_list = []
        
        # Istorija poteza za prikaz
        self.move_history = []
    
    #callbacks
    def reset_selection(self):
        """Resetuje selekciju na šahovskoj tabli."""
        self.square_selected = ()
        self.squares_list = []
    
    def add_to_selection(self, square):
        """Dodaje kliknuto polje u selekciju."""
        self.square_selected = square
        self.squares_list.append(square)
    
    def toggle_menu(self):
        """Prikazuje ili sakriva glavni meni."""
        self.show_menu = not self.show_menu
    
    def toggle_menu_icons(self):
        """Prikazuje ili sakriva ikone menija."""
        self.show_menu_icons = not self.show_menu_icons
    
    def toggle_manual(self):
        self.show_manual = not self.show_manual
    
    def toggle_sound(self):
        """Uključuje ili isključuje zvuk."""
        self.sound = not self.sound
    
    # def toggle_table(self):
    #     """Uključuje ili isključuje prikaz tabele."""
    #     self.show_table = not self.show_table

    def set_ai_white(self):
        self.ai_white = True
        self.ai_black = False
        self.human_vs_human = False
    
    def set_ai_black(self):
        self.ai_white = False
        self.ai_black = True
        self.human_vs_human = False

    def set_human_vs_human(self):
        self.ai_white = False
        self.ai_black = False
        self.human_vs_human = True

    def switch_background(self):
        self.board_style += 1
        self.board_style %= self.n_styles
    
    def toggle_table_color(self):
        self.table_color = not self.table_color
    
    def toggle_control(self):
        """Uključuje ili isključuje prikaz kontrola."""
        self.show_control = not self.show_control
    
    def start_ai_thinking(self):
        """Označava da AI razmišlja o potezu."""
        self.ai_thinking = True
    
    def stop_ai_thinking(self):
        """Označava da je AI završio razmišljanje."""
        self.ai_thinking = False

    def __str__(self):
        return f"ai_white:  {self.ai_white}, ai_black: {self.ai_black}, human: {self.human_vs_human}"