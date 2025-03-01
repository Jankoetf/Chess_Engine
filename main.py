import pygame as p

import chess_engine.game_state as game_state
from chess_engine.constants import *
from ui.load_images import LoadImages
from ui.ui_state import UiState
from ui.button import Button
from ui.view import ViewClass

#initialize pygame
p.init()

#load all images
Images, Menu = LoadImages().get_all_images()

#components
ui_instance = UiState()

#View
view_instance = ViewClass(ui_instance)

# meni_icons_button = Button(0, 1, 1, 1, "", Menu["menu1"], ui_instance.toggle_menu_icons)
meni_button = Button(0, 4, 1, 1, "", Menu["menu2"], ui_instance.toggle_menu)
meni_button_in_meni = Button(0, 9, 1, 1, "", Menu["menu2"], ui_instance.toggle_menu)
background_style_button = Button(1, 9, 2, 1, "", Menu["N3"], ui_instance.switch_background)

def main():    
    table_color = False
    ai_black, ai_white, ai_ai = False, False, False
    sound = False
    show_control = False

    important_squares = [(1, -1), (2, -1), (3, -1), (4, -1), (5, -1), (6, -1)]
    
    screen = p.display.set_mode((WIDTH_TOTAL, HEIGHT_TOTAL))
    background = p.Surface((WIDTH, HEIGHT))
    background.fill(p.Color("black"))
    skeleton = p.Surface((WIDTH_TOTAL, HEIGHT_TOTAL))
    skeleton.fill(p.Color("white"))
    skeleton_icons = p.Surface((WIDTH_TOTAL, HEIGHT_TOTAL)) 
    skeleton_icons.fill(p.Color("white"))
    menu = p.Surface((WIDTH_TOTAL, HEIGHT_TOTAL))
    
    clock = p.time.Clock()

    gs = game_state.GameState()
    
    gs.BlackOrWhiteMove()
    validMoves = gs.get_all_legit_moves(gs.board)
    
    SquaresList = []
    SquareSelected = ()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:#Left == 1, Right ==3            
                location = p.mouse.get_pos()
                detectMouseprint(gs, location)#Checking square
                help_square = detectMouse_board_iterator(gs, location)
                
                if not ui_instance.show_menu:
                    view_instance.buttons["meni_icons_button"].handle_event(e)

                if ui_instance.show_menu_icons:
                    meni_button.handle_event(e)
                
                if ui_instance.show_menu:
                    background_style_button.handle_event(e)
                    meni_button_in_meni.handle_event(e)
                
                if help_square == (3, -1) and ui_instance.show_menu_icons and not ui_instance.show_menu:

                    ui_instance.show_menu = True
                    
                if help_square == (4, -1) and ui_instance.show_menu_icons and not ui_instance.show_menu:
                    sound = True if not sound else False
                   
                if help_square == (2, -1) and ui_instance.show_menu_icons and not ui_instance.show_menu:
                    table_color = True if not table_color else False
                
                if help_square == (5, -1) and ui_instance.show_menu_icons and not ui_instance.show_menu:
                    show_control = True if not show_control else False
                    
                if help_square == (6, -1) and ui_instance.show_menu_icons and not ui_instance.show_menu:
                    for i in range(len(gs.ListOfStupidMoves)):
                        gs.undoStupidMove(gs.board)
                
                if (help_square in important_squares and ui_instance.show_menu_icons) and not ui_instance.show_menu:
                    pass
                   
                if ui_instance.show_menu: 
                    if help_square == (8, -1):
                        ui_instance.show_menu = False
                    elif help_square == (8, 2):
                        if len(gs.ListOfStupidMoves) == 0:
                            ai_black, ai_white, ai_ai = True, False, False
                    elif help_square == (8, 3) or help_square == (8, 4):
                        if len(gs.ListOfStupidMoves) == 0:
                            ai_black, ai_white, ai_ai = False, False, False
                    elif help_square == (8, 5):
                        if len(gs.ListOfStupidMoves) == 0:
                            ai_black, ai_white, ai_ai = False, True, False
                            print(gs.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))
                    elif help_square == (8, 6) or help_square == (8,7):
                        if len(gs.ListOfStupidMoves) == 0:
                            ai_black, ai_white, ai_ai = False, False, True
                        
                        
                # if ((-1 in help_square) or (8 in help_square)) and (not help_square in important_squares or not show_menu_icon): 
                #     show_menu_icon = False if show_menu_icon else True
                    
                if not ai_ai:
                    if (SquareSelected != help_square) and not ((-1 in help_square) or (8 in help_square)) and not ui_instance.show_menu:
                        SquareSelected = help_square
                        SquaresList.append(SquareSelected)
                        print(help_square)
                        
                    else:
                        SquareSelected = ()
                        SquaresList = []
                    
                    if len(SquaresList) == 2:
                        move = game_state.Move(SquaresList[0], SquaresList[1], gs.board)
                        validMoves = gs.get_all_legit_moves(gs.board)
                        
                        if move in validMoves:
                            gs.MakeStupidMove(move, gs.board)
                            print(f"White king position is: {gs.WhiteKingPosition}")
                            print(f"Black king position is: {gs.BlackKingPosition}")
                            
                            if ai_white:
                                print(gs.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))
                            elif ai_black:
                                print(gs.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "b"))
                            
                            gs.Check()
                            validMoves = gs.get_all_legit_moves(gs.board)
                            
                            SquaresList = []
                            SquareSelected = ()
                            gs.BlackOrWhiteMove()
                        else:   
                            print("Move is invalid")
                            SquaresList = []
                            SquareSelected = ()
            
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 3:
                SquareSelected = ()
                SquaresList = []
                gs.undoStupidMove(gs.board)
                gs.BlackOrWhiteMove()
                validMoves = gs.get_all_legit_moves(gs.board)
                print(f"White king position is: {gs.WhiteKingPosition}")
                print(f"Black king position is: {gs.BlackKingPosition}")
                
                
        if not ui_instance.show_menu:
            ViewClass.draw_notation_rank_file(gs, background, show_control, table_color)
            ViewClass.draw_pieces(gs, background)           
            if ui_instance.show_menu_icons:
                ViewClass.draw_menu_icons(skeleton_icons, sound, "b" if not gs.whiteToMove else "w")
                screen.blit(skeleton_icons, (0,0))
                meni_button.draw(screen)
            else:     
                screen.blit(skeleton, (0,0))    
            screen.blit(background,(ADDITIONAL_WIDTH, ADDITIONAL_HEIGHT))

            view_instance.buttons["meni_icons_button"].draw(screen)

        else:
            ViewClass.draw_menu(menu, ui_instance.board_style)
            screen.blit(menu,(0, 0))
            meni_button_in_meni.draw(screen)
            background_style_button.draw(screen)
            
        clock.tick(MAX_FPS)
        p.display.flip()
    
    print(gs.mc)
    print(gs.uc)
    p.quit()
    
            
def detectMouseprint(gs, location):
    if location[1]//64 - 1 in range(8) and location[0]//64 - 1 in range(8):
        print(gs.board_notation[location[1]//64 - 1][location[0]//64 - 1])

def detectMouse(gs, location):
    return gs.board_notation[location[1]//64 - 1][location[0]//64 - 1]
    
def detectMouse_board_iterator_print(gs, location):
    return print(f"{location[1]//64 - 1}, {location[0]//64 - 1}")

def detectMouse_board_iterator(gs, location):
    return (location[1]//64 - 1, location[0]//64 - 1)


    
    
if __name__ == "__main__":    
    main()
