""" class that encapsulates the user interface state of a chess application """
class UiState:
    def __init__(self):
        """
        Initializes the main application UI state and global configuration options.

        This constructor sets up all necessary variables that control the behavior and appearance of the UI as well as game logic. 
        It encapsulates:

        - Application state: Flags for displaying menus, icons, manual, temporary board state, and game evaluation score.
        - Game options: Settings for board style, table color, control display, and sound.
        - AI state: Flags to determine if AI is playing as white or black, or if it's a human vs. human game, and the corresponding game mode.

        These attributes ensure that the GUI and underlying game mechanisms can be managed globally and updated as needed
        """
        
        #app state
        self.show_menu = False #if menu than not table!
        self.show_menu_icons = False
        self.show_manual = False
        self.temp_board = None
        self.game_evaluation = 0
        
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
        self.game_mode = "Human VS Human"
        
        # square selection
        self.square_selected = ()
        self.squares_list = []
        
        # Istorija poteza za prikaz
        self.move_history = []
    
    #callbacks
    def reset_selection(self):
        """Resets the board selection by clearing the selected square and the selection list."""
        self.square_selected = ()
        self.squares_list = []
    
    def toggle_menu(self):
        """Toggles the visibility of the main menu."""
        self.show_menu = not self.show_menu
    
    def toggle_menu_icons(self):
        """Toggles the visibility of the menu icons."""
        self.show_menu_icons = not self.show_menu_icons
    
    def toggle_manual(self):
        """Toggles the display of the manual."""
        self.show_manual = not self.show_manual
    
    def toggle_sound(self):
        """toggles visibility of the labels"""
        self.sound = not self.sound

    def set_ai_white(self):
        """Sets the game mode for AI playing as white against a human opponent."""
        self.ai_white = True
        self.ai_black = False
        self.human_vs_human = False
        self.game_mode = "White AI VS Human"
    
    def set_ai_black(self):
        """Sets the game mode for AI playing as black against a human opponent."""
        self.ai_white = False
        self.ai_black = True
        self.human_vs_human = False
        self.game_mode = "Black AI VS Human"

    def set_human_vs_human(self):
        """Sets the game mode to human vs human."""
        self.ai_white = False
        self.ai_black = False
        self.human_vs_human = True
        self.game_mode = "Human VS Human"

    def switch_background(self):
        """Cycles through the available board background styles."""
        self.board_style += 1
        self.board_style %= self.n_styles
    
    def toggle_table_color(self):
        """Toggles the table color setting."""
        self.table_color = not self.table_color
    
    def toggle_control(self):
        """Toggles the display of control squares on the board."""
        self.show_control = not self.show_control

    def toggle_ai_thinking(self):
        """Toggles the AI thinking state, while AI is thinking player select new move"""
        self.ai_thinking = not self.ai_thinking

    def __str__(self):
        """For printing"""
        return f"ai_white:  {self.ai_white}, ai_black: {self.ai_black}, human: {self.human_vs_human}"