import pygame as p

import chess_engine.game_state as game_state
from chess_engine.constants import *
from chess_engine.ai_class import AiClass
from ui.ui_state import UiState
from ui.view import ViewClass


#initialize pygame
p.init()

#components
ui_instance = UiState()

#View
view_instance = ViewClass(ui_instance)

def main():    
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

    #AI
    ai_instance = AiClass(gs)
    
    gs.BlackOrWhiteMove()
    validMoves = gs.get_all_legit_moves()
    
    SquaresList = []
    SquareSelected = ()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1: #Left == 1, Right ==3             
                location = p.mouse.get_pos()
                print_detect_mouse(gs, location) #Checking square
                # print(ui_instance)
                help_square = detect_mouse_board_iterator(gs, location)

                if not ui_instance.show_menu:
                    view_instance.buttons["meni_icons_button"].handle_event(e)

                if ui_instance.show_menu_icons and not ui_instance.show_menu:
                    view_instance.buttons["meni_button"].handle_event(e)
                    view_instance.buttons["table_color_button"].handle_event(e)
                    view_instance.buttons["sound_button"].handle_event(e)
                    view_instance.buttons["control_button"].handle_event(e)

                    if view_instance.buttons["reset_button"].is_clicked(e.pos):
                        for i in range(len(gs.ListOfStupidMoves)):
                            gs.undoStupidMove(gs.board)
                        
                        if ui_instance.ai_white:
                            print(ai_instance.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))
                
                if ui_instance.show_menu:
                    view_instance.buttons["background_style_button"].handle_event(e)
                    view_instance.buttons["meni_button_in_meni"].handle_event(e)
                    view_instance.buttons["meni_button_in_meni_2"].handle_event(e)
                    view_instance.buttons["manual_button"].handle_event(e)

                    #ai state control
                    if view_instance.buttons["ai_white_button"].is_clicked(e.pos) or \
                        view_instance.buttons["human_vs_human_button"].is_clicked(e.pos) or view_instance.buttons["ai_black_button"].is_clicked(e.pos):
                        
                        for i in range(len(gs.ListOfStupidMoves)): #restart a game, because game mode is set
                            gs.undoStupidMove(gs.board)
                        
                        gs.BlackOrWhiteMove()
                        #set state
                        view_instance.buttons["ai_white_button"].handle_event(e)
                        view_instance.buttons["human_vs_human_button"].handle_event(e)
                        view_instance.buttons["ai_black_button"].handle_event(e)

                        if view_instance.buttons["ai_white_button"].is_clicked(e.pos):
                            print(ai_instance.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))

                        ui_instance.show_menu = False #play game!
                                            
                
                if (SquareSelected != help_square) and not ((-1 in help_square) or (8 in help_square)) and not ui_instance.show_menu:
                    SquareSelected = help_square
                    SquaresList.append(SquareSelected)
                    print(help_square)
                    
                else:
                    SquareSelected = ()
                    SquaresList = []
                
                if len(SquaresList) == 2:
                    move = game_state.Move(SquaresList[0], SquaresList[1], gs.board)
                    validMoves = gs.get_all_legit_moves()
                    
                    if move in validMoves:
                        gs.MakeStupidMove(move, gs.board)
                        print(f"White king position is: {gs.WhiteKingPosition}")
                        print(f"Black king position is: {gs.BlackKingPosition}")
                        
                        if ui_instance.ai_white:
                            print(ai_instance.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))
                        elif ui_instance.ai_black:
                            print(ai_instance.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "b"))
                        
                        gs.Check()
                        validMoves = gs.get_all_legit_moves()
                        
                        SquaresList = []
                        SquareSelected = ()
                        gs.BlackOrWhiteMove()
                    else:   
                        print("Move is invalid")
                        SquaresList = []
                        SquareSelected = ()
            
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 3:
                #undo move option is disabled in menu and when ai is playing
                if not ui_instance.show_menu and ui_instance.human_vs_human: 
                    SquareSelected = ()
                    SquaresList = []
                    gs.undoStupidMove(gs.board)
                    gs.BlackOrWhiteMove()
                    validMoves = gs.get_all_legit_moves()
                    print(f"White king position is: {gs.WhiteKingPosition}")
                    print(f"Black king position is: {gs.BlackKingPosition}")
            
            elif ui_instance.show_manual:            
                view_instance.manual.handle_event(e)

                
        # display table and options 
        if not ui_instance.show_menu:
            ViewClass.draw_notation_rank_file(gs, background, ui_instance.show_control, ui_instance.table_color)
            ViewClass.draw_pieces(gs, background)           
            if ui_instance.show_menu_icons:
                ViewClass.draw_menu_icons(skeleton_icons, ui_instance.sound, "b" if not gs.whiteToMove else "w")
                screen.blit(skeleton_icons, (0,0))
                view_instance.buttons["meni_button"].draw(screen)
                view_instance.buttons["table_color_button"].draw(screen)
                view_instance.buttons["sound_button"].draw(screen)
                view_instance.buttons["control_button"].draw(screen)
                view_instance.buttons["reset_button"].draw(screen)

            else:     
                screen.blit(skeleton, (0,0))    
            screen.blit(background,(ADDITIONAL_WIDTH, ADDITIONAL_HEIGHT))

            view_instance.buttons["meni_icons_button"].draw(screen)

        else:
            view_instance.draw_menu(menu, view_instance, ui_instance.board_style, ui_instance.show_manual)

            screen.blit(menu,(0, 0))
            view_instance.buttons["meni_button_in_meni"].draw(screen)
            view_instance.buttons["meni_button_in_meni_2"].draw(screen)
            view_instance.buttons["background_style_button"].draw(screen)

            view_instance.buttons["ai_white_button"].draw(screen)
            view_instance.buttons["ai_black_button"].draw(screen)
            view_instance.buttons["human_vs_human_button"].draw(screen)
            view_instance.buttons["manual_button"].draw(screen)

                
            
        clock.tick(MAX_FPS)
        p.display.flip()
    
    print(gs.mc)
    print(gs.uc)
    p.quit()
    
            
def print_detect_mouse(gs, location):
    if location[1]//64 - 1 in range(8) and location[0]//64 - 1 in range(8):
        print(gs.board_notation[location[1]//64 - 1][location[0]//64 - 1])

def detect_mouse(gs, location):
    return gs.board_notation[location[1]//64 - 1][location[0]//64 - 1]

def detect_mouse_board_iterator(gs, location):
    return (location[1]//64 - 1, location[0]//64 - 1)
 
    
if __name__ == "__main__":    
    main()
