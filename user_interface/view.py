"""drawing logic"""
import pygame as p

from chess_engine.constants import *
from user_interface.button import Button
from user_interface.label import Label
from user_interface.load_images import LoadImages
from user_interface.manual_viewer import ManualViewer

class ViewClass:
    Images, Menu = LoadImages().get_all_images()

    def __init__(self, ui_instance):
        """
        Initializes the ViewClass with UI elements, buttons, manual viewer, and labels.

        Args:
            ui_instance: An instance providing callback methods to update the UI state.
        
        The constructor creates a collection of buttons with their corresponding positions, images, and callback functions.
        It also initializes a ManualViewer for displaying game instructions and sets up labels for game evaluation,
        AI status, and game mode.
        """

        self.buttons = {
            "meni_icons_button":Button(0, 1, 1, 1, self.Menu["menu1"],None, ui_instance.toggle_menu_icons),
            "meni_button": Button(0, 4, 1, 1, self.Menu["menu2"],None,  ui_instance.toggle_menu),
            "meni_button_in_meni": Button(0, 9, 1, 1, self.Menu["menu2"],None,  ui_instance.toggle_menu),
            "meni_button_in_meni_2": Button(9, 9, 1, 1, self.Menu["menu2"],None,  ui_instance.toggle_menu),
            "background_style_button": Button(1, 9, 2, 1, self.Menu["N3"],None,  ui_instance.switch_background),
            "table_color_button": Button(0, 3, 1, 1, self.Menu["color"], None,  ui_instance.toggle_table_color),
            "sound_button": Button(0, 5, 1, 1, self.Menu["sound2"], self.Menu["sound1"], ui_instance.toggle_sound),
            "control_button": Button(0, 6, 1, 1, self.Menu["Robots3"], None, ui_instance.toggle_control),
            "reset_button": Button(0, 7, 1, 1, self.Menu["N2"], None, None),
            "ai_black_button": Button(3, 9, 1, 1, self.Menu["blackAI"], None, ui_instance.set_ai_black),
            "human_vs_human_button": Button(4, 9, 2, 1, self.Menu["N1"], None, ui_instance.set_human_vs_human),
            "ai_white_button": Button(6, 9, 1, 1, self.Menu["whiteAI"], None, ui_instance.set_ai_white),
            "manual_button": Button(7, 9, 2, 1, self.Menu["manual"], None, ui_instance.toggle_manual),
        }

        manual_path = "Resources/ImgsMenu/game_instructions.png"
        self.manual = ManualViewer(manual_path, (WIDTH_TOTAL, HEIGHT))

        self.labels = {
            "game_evaluation_label":Label(0.2, 9, ""),
            "ai_label": Label(0.2, 9.5, "AI is thinking"),
            "game_mode_label": Label(0.2, 0.5, "game mode: Black AI VS Human"),
        }

    @staticmethod
    def draw_board(board):
        colors = [p.Color("white"), p.Color("grey")]
        for rank in range(BASE_DIMENSION):
            for file in range(BASE_DIMENSION):
                color = colors[((rank+file)%2)]
                p.draw.rect(board, color,
                p.Rect(rank*SQUARE_SIZE, file*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def draw_notation_rank_file(gs, board, showControl, c):
        color = "b" if gs.whiteToMove else "w"
        op_color = "w" if gs.whiteToMove else "b"
        controled = gs.Control(color, gs.board)
        controled2  = gs.Control(op_color, gs.board)
        Font = p.font.SysFont(None, 24)
        colors = [p.Color((224, 224, 224)), p.Color((128, 128, 128)), p.Color((120, 80, 40)), p.Color((80, 40, 120)),p.Color((120, 120, 20))]
        if c:
            colors = [p.Color("white"), p.Color("green"), p.Color((120, 80, 40)), p.Color((80, 40, 120)), p.Color((120, 120, 20))]
            
        
        for rank in range(BASE_DIMENSION):
            for file in range(BASE_DIMENSION):
                color = colors[((rank + file)%2)]
                p.draw.rect(board, color, p.Rect(file*64, rank*64, 64,64))
                if showControl:
                    if (rank, file) in controled:
                        p.draw.rect(board, colors[2], p.Rect(file*64, rank*64, 64,64))
                    elif (rank, file) in controled2:
                        p.draw.rect(board, colors[3], p.Rect(file*64, rank*64, 64,64))
                    if (rank, file) in controled2 and (rank, file) in controled:
                        p.draw.rect(board, colors[4], p.Rect(file*64, rank*64, 64,64))
                    
                img = Font.render(gs.board_notation[rank][file], True, (0, 0, 0))
                board.blit(img, (file*SQUARE_SIZE,rank*SQUARE_SIZE))

    @staticmethod
    def draw_pieces(gs, board, background):
        
        for rank in range(BASE_DIMENSION):
            for file in range(BASE_DIMENSION):
                piece = board[rank][file]
                if piece != "--":
                    background.blit(ViewClass.Images[piece], p.Rect(file*SQUARE_SIZE,
                                rank*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if gs.black_is_mated:
            background.blit(ViewClass.Images["wK_w"], p.Rect(gs.WhiteKingPosition[1]*SQUARE_SIZE, gs.WhiteKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            background.blit(ViewClass.Images["bK_l"], p.Rect(gs.BlackKingPosition[1]*SQUARE_SIZE, gs.BlackKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif gs.white_is_mated:
            background.blit(ViewClass.Images["wK_l"], p.Rect(gs.WhiteKingPosition[1]*SQUARE_SIZE, gs.WhiteKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            background.blit(ViewClass.Images["bK_w"], p.Rect(gs.BlackKingPosition[1]*SQUARE_SIZE, gs.BlackKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    @staticmethod
    def draw_menu_icons(board, sound, turn = "b"):
        # board.blit(ViewClass.Menu["Robots3"], (0*SQUARE_SIZE, 6*SQUARE_SIZE))
        #board.blit(Menu["N1"], (0*SQUARE_SIZE, 3*SQUARE_SIZE))
        if turn == "b":
            board.blit(ViewClass.Menu["blackK"], (0*SQUARE_SIZE, 2*SQUARE_SIZE))
        else:
            board.blit(ViewClass.Menu["whiteK"], (0*SQUARE_SIZE, 2*SQUARE_SIZE))
        #board.blit(ViewClass.Menu["N2"], (0*SQUARE_SIZE, 7*SQUARE_SIZE))

    @staticmethod
    def draw_menu(menu, view_instance, background, show_manual):
        #Font = p.font.SysFont(None, 28)

        if show_manual:
            view_instance.manual.draw(menu)
        else:
            menu.blit(ViewClass.Menu[f"background{background+1}"], (0,0))

