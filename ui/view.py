"""drawing logic"""
import pygame as p

from chess_engine.constants import *
from ui.button import Button
from ui.load_images import LoadImages

Images, Menu = LoadImages().get_all_images()

class ViewClass:
    def __init__(self, ui_instance): #/????????????????????????
        self.buttons = {
            "meni_icons_button":Button(0, 1, 1, 1, "", Menu["menu1"], ui_instance.toggle_menu_icons)
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
    def draw_pieces(gs, board1):
        for rank in range(BASE_DIMENSION):
            for file in range(BASE_DIMENSION):
                piece = gs.board[rank][file];
                if piece != "--":
                    board1.blit(Images[piece], p.Rect(file*SQUARE_SIZE,
                                rank*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if gs.black_is_mated:
            board1.blit(Images["wK_w"], p.Rect(gs.WhiteKingPosition[1]*SQUARE_SIZE, gs.WhiteKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            board1.blit(Images["bK_l"], p.Rect(gs.BlackKingPosition[1]*SQUARE_SIZE, gs.BlackKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif gs.white_is_mated:
            board1.blit(Images["wK_l"], p.Rect(gs.WhiteKingPosition[1]*SQUARE_SIZE, gs.WhiteKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            board1.blit(Images["bK_w"], p.Rect(gs.BlackKingPosition[1]*SQUARE_SIZE, gs.BlackKingPosition[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    @staticmethod
    def draw_menu_icons(board, sound, turn = "b"):
        #board.blit(Menu["menu2"], (0*SQUARE_SIZE, 4*SQUARE_SIZE))
        if sound:
            board.blit(Menu["sound1"], (0*SQUARE_SIZE, 5*SQUARE_SIZE))
        else:
            board.blit(Menu["sound2"], (0*SQUARE_SIZE, 5*SQUARE_SIZE))
        Font = p.font.SysFont(None, 38)
        board.blit(Menu["Robots3"], (0*SQUARE_SIZE, 6*SQUARE_SIZE))
        board.blit(Menu["N1"], (0*SQUARE_SIZE, 3*SQUARE_SIZE))
        if turn == "b":
            board.blit(Menu["blackK"], (0*SQUARE_SIZE, 2*SQUARE_SIZE))
        else:
            board.blit(Menu["whiteK"], (0*SQUARE_SIZE, 2*SQUARE_SIZE))
        board.blit(Menu["N2"], (0*SQUARE_SIZE, 7*SQUARE_SIZE))

    @staticmethod
    def draw_menu(menu, background = 0, ai = False):
        Font = p.font.SysFont(None, 28)
        menu.blit(Menu[f"background{background+1}"], (0,0))
        
        menu.blit(Menu["N1"], (SQUARE_SIZE*4, SQUARE_SIZE*9))
        img = Font.render("Normal game", True, (0, 0, 0))
        menu.blit(img, (SQUARE_SIZE*4, SQUARE_SIZE*9 + 40))
        
        menu.blit(Menu["whiteK2"], (SQUARE_SIZE*3, SQUARE_SIZE*9))
        img = Font.render("AI", True, (0, 0, 0))
        menu.blit(img, (SQUARE_SIZE*3, SQUARE_SIZE*9 + 10))
        
        menu.blit(Menu["blackK2"], (SQUARE_SIZE*6, SQUARE_SIZE*9))
        img = Font.render("AI", True, (0, 0, 0))
        menu.blit(img, (SQUARE_SIZE*6, SQUARE_SIZE*9 + 10))
        
        menu.blit(Menu["Robots"], (SQUARE_SIZE*7, SQUARE_SIZE*9))
        #menu.blit(Menu["menu2"], (SQUARE_SIZE*0, SQUARE_SIZE*9))
        #menu.blit(Menu["N3"], (SQUARE_SIZE*1, SQUARE_SIZE*9))