import pygame as p
import GameState
from Constants import *
import time

p.init()
Images = {}
Menu = {}



def main():
    show_menu_icon, show_menu = False, False
    #backgrounds = ["background1", "background2", "background3"]
    robot, bs, table = 0, 0, False
    ai_black, ai_white, ai_ai = False, False, False
    sound = False
    important_squares = [(1, -1), (2, -1), (3, -1), (4, -1), (5, -1),(6, -1)]
    show_control = False
    
    loadImages()
    menu_images()
    
    screen = p.display.set_mode((Width_all, Height_all))
    background = p.Surface((Width, Height))
    background.fill(p.Color("black"))
    skeleton = p.Surface((Width_all, Height_all))
    skeleton.fill(p.Color("white"))
    skeleton_icons = p.Surface((Width_all, Height_all)) 
    skeleton_icons.fill(p.Color("white"))
    menu = p.Surface((Width_all, Height_all))
    
    clock = p.time.Clock()

    gs = GameState.GameState()
    #print(gs.min_max_alpha_beta(gs.board,0, True, -1000, 1000))
#    move = GameState.Move((1,2), (3, 2), gs.board)
#    gs.MakeStupidMove(move, gs.board)
    

    
    
    
    
    gs.BlackOrWhiteMove()
    validMoves = gs.get_all_legit_moves(gs.board)
    #print(validMoves)
    #print(gs.board[0][5])
    

    
    
    
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
                
                if help_square == (3, -1) and show_menu_icon and not show_menu:
                    show_menu = True
                    
                if help_square == (4, -1) and show_menu_icon and not show_menu:
                    sound = True if not sound else False
                   
                if help_square == (2, -1) and show_menu_icon and not show_menu:
                    table = True if not table else False
                
                if help_square == (5, -1) and show_menu_icon and not show_menu:
                    show_control = True if not show_control else False
                    
                if help_square == (6, -1) and show_menu_icon and not show_menu:
                    for i in range(len(gs.ListOfStupidMoves)):
                        gs.undoStupidMove(gs.board)
                
                if (help_square in important_squares and show_menu_icon) and not show_menu:
                    pass
                   
                if show_menu: 
                    if help_square == (8, -1):
                        show_menu = False
                    elif help_square == (8, 0) or help_square == (8, 1):
                        bs += 1; bs = bs%3;
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
                        
                        
                    
                if ((-1 in help_square) or (8 in help_square)) and (not help_square in important_squares or not show_menu_icon): 
                    show_menu_icon = False if show_menu_icon else True
                    
                
                if not ai_ai:
                    if (SquareSelected != help_square) and not ((-1 in help_square) or (8 in help_square)) and not show_menu:
                        SquareSelected = help_square
                        SquaresList.append(SquareSelected)
                        print(help_square)
                        
                    else:
                        SquareSelected = ()
                        SquaresList = []
                    
                    if len(SquaresList) == 2:
                        move = GameState.Move(SquaresList[0], SquaresList[1], gs.board)
                        validMoves = gs.get_all_legit_moves(gs.board)
                        #move.analyzeStupidMove()
                        if move in validMoves:
                            gs.MakeStupidMove(move, gs.board)
                            print(f"White king position is: {gs.WhiteKingPosition}")
                            print(f"Black king position is: {gs.BlackKingPosition}")
                            #print(gs.whiteToMove)
                            if ai_white:
                                print(gs.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "w"))
                            elif ai_black:
                                print(gs.min_max_alpha_beta(gs.board, 0, True, -1000, 1000, "b"))
                            
                            # if (len(gs.ListOfStupidMoves) == 2):
                            #     print(gs.min_max_alpha_beta(gs.board,0, True, -1000, 1000))
                            #     print(gs.ListOfStupidMoves)
                            
                            gs.Check()
                            validMoves = gs.get_all_legit_moves(gs.board)
                            
                            SquaresList = []
                            SquareSelected = ()
                            gs.BlackOrWhiteMove()
                        else:   
                            #print(gs.min_max_alpha_beta(gs.board,0, True, -1000, 1000))
                            print("Move is invalid")
                            SquaresList = []
                            SquareSelected = ()
            
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 3:
                SquareSelected = ()
                SquareList = []
                gs.undoStupidMove(gs.board)
                gs.BlackOrWhiteMove()
                validMoves = gs.get_all_legit_moves(gs.board)
                print(f"White king position is: {gs.WhiteKingPosition}")
                print(f"Black king position is: {gs.BlackKingPosition}")
                
                    
                
                
                
                
        if not show_menu:
            drawNotationRankFile(gs, background, show_control, table);
            #drawBoard(background)
            drawPieces(gs, background)           
            if show_menu_icon: 
                draw_menu_icons(skeleton_icons, sound, "b" if not gs.whiteToMove else "w")
                screen.blit(skeleton_icons, (0,0))
            else:     
                screen.blit(skeleton, (0,0))    
            screen.blit(background,(Add_Width, Add_Height))
        else:
            draw_menu(menu, bs)
            screen.blit(menu,(0, 0))
            
            
        clock.tick(Max_fps)
        p.display.flip()
    
    print(gs.mc)
    print(gs.uc)
    p.quit()
    
    
  
def drawBoard(board):
    colors = [p.Color("white"), p.Color("grey")]
    for rank in range(Dim):
        for file in range(Dim):
            color = colors[((rank+file)%2)]
            p.draw.rect(board, color,
            p.Rect(rank*Square_size, file*Square_size, Square_size, Square_size))
            

def drawNotationRankFile(gs, board, showControl, c):
    color = "b" if gs.whiteToMove else "w"
    op_color = "w" if gs.whiteToMove else "b"
    controled = gs.Control(color, gs.board)
    controled2  = gs.Control(op_color, gs.board)
    Font = p.font.SysFont(None, 24)
    #p.Color("white"), p.Color("green")
    colors = [p.Color((224, 224, 224)), p.Color((128, 128, 128)), p.Color((120, 80, 40)), p.Color((80, 40, 120)),p.Color((120, 120, 20))]
    if c:
        colors = [p.Color("white"), p.Color("green"), p.Color((120, 80, 40)), p.Color((80, 40, 120)),p.Color((120, 120, 20))]
        
    
    for rank in range(Dim):
        for file in range(Dim):
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
            board.blit(img, (file*Square_size,rank*Square_size))
            


def loadImages():
    Pieces = ["bK", "bQ", "bN", "bR", "bP", "bB", "bK_w", "bK_l",
              "wP", "wR","wN", "wB", "wK", "wQ", "wK_w", "wK_l"];       
    for piece in Pieces:
        Images[piece] = p.transform.scale(
                p.image.load("Images/" + piece + ".png"),
                (Square_size, Square_size))
        
def menu_images():
    imgs = ["menu1", "sound2", "sound1", "Robots2"];          
    
    for img in imgs:
        Menu[img] = p.transform.scale(
                p.image.load("ImgsMenu/" + img + ".png"),
                (Square_size, Square_size))
    backgrounds = ["background1", "background2", "background3"]
    for b in backgrounds:
        Menu[b] = p.transform.scale(
                p.image.load("ImgsMenu/" + b + ".jpg"),
                (Width_all, Height + Square_size))
    Menu["N2"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "N2" + ".jpg"),
                (1*Square_size, 1*Square_size))
    Menu["N3"] = p.transform.scale(
                 p.image.load("ImgsMenu/" + "N3" + ".jpg"),
                (2*Square_size, 1*Square_size))
    
    Menu["N1"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "N1" + ".jpeg"),
                (2*Square_size, 1*Square_size))
    Menu["Robots3"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "Robots3" + ".jpg"),
                (Square_size, Square_size))
    Menu["whiteK2"] =  p.transform.scale(
                p.image.load("ImgsMenu/" + "whiteK2" + ".jpg"),
                (Square_size, Square_size))
    Menu["blackK2"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "blackK2" + ".png"),
                (Square_size, Square_size))
    Menu["Robots"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "Robots" + ".jpg"),
                (2*Square_size, Square_size))
    Menu["blackK"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "blackK" + ".jpg"),
                (Square_size, Square_size))
    Menu["whiteK"] = p.transform.scale(
                p.image.load("ImgsMenu/" + "whiteK" + ".jpg"),
                (Square_size, Square_size))
    
    
def drawPieces(gs, board1):
    for rank in range(Dim):
        for file in range(Dim):
            piece = gs.board[rank][file];
            if piece != "--":
                board1.blit(Images[piece], p.Rect(file*Square_size,
                            rank*Square_size, Square_size, Square_size))
    if gs.black_is_mated:
        board1.blit(Images["wK_w"], p.Rect(gs.WhiteKingPosition[1]*Square_size, gs.WhiteKingPosition[0]*Square_size, Square_size, Square_size))
        board1.blit(Images["bK_l"], p.Rect(gs.BlackKingPosition[1]*Square_size, gs.BlackKingPosition[0]*Square_size, Square_size, Square_size))
    elif gs.white_is_mated:
        board1.blit(Images["wK_l"], p.Rect(gs.WhiteKingPosition[1]*Square_size, gs.WhiteKingPosition[0]*Square_size, Square_size, Square_size))
        board1.blit(Images["bK_w"], p.Rect(gs.BlackKingPosition[1]*Square_size, gs.BlackKingPosition[0]*Square_size, Square_size, Square_size))

def draw_menu_icons(board, sound, turn = "b"):
    board.blit(Menu["menu1"], (0*Square_size, 4*Square_size))
    if sound:
        board.blit(Menu["sound1"], (0*Square_size, 5*Square_size))
    else:
        board.blit(Menu["sound2"], (0*Square_size, 5*Square_size))
    Font = p.font.SysFont(None, 38)
    board.blit(Menu["Robots3"], (0*Square_size, 6*Square_size))
    board.blit(Menu["N1"], (0*Square_size, 3*Square_size))
    if turn == "b":
        board.blit(Menu["blackK"], (0*Square_size, 2*Square_size))
    else:
        board.blit(Menu["whiteK"], (0*Square_size, 2*Square_size))
    board.blit(Menu["N2"], (0*Square_size, 7*Square_size))
    #img = Font.render("R", True, (0, 0, 0))
    #board.blit(img, (Square_size*0 + 20, Square_size*6 + 10))
    
def draw_menu(menu, back = 0, ai = False):
    Font = p.font.SysFont(None, 28)
    if back == 0:
        menu.blit(Menu["background1"], (0,0))
    elif back == 1:
        menu.blit(Menu["background2"], (0,0))
    else:
        menu.blit(Menu["background3"], (0,0))
    
    menu.blit(Menu["N1"], (Square_size*4, Square_size*9))
    img = Font.render("Normal game", True, (0, 0, 0))
    menu.blit(img, (Square_size*4, Square_size*9 + 40))
    
    menu.blit(Menu["whiteK2"], (Square_size*3, Square_size*9))
    img = Font.render("AI", True, (0, 0, 0))
    menu.blit(img, (Square_size*3, Square_size*9 + 10))
    
    menu.blit(Menu["blackK2"], (Square_size*6, Square_size*9))
    img = Font.render("AI", True, (0, 0, 0))
    menu.blit(img, (Square_size*6, Square_size*9 + 10))
    
    menu.blit(Menu["Robots"], (Square_size*7, Square_size*9))
    menu.blit(Menu["menu1"], (Square_size*0, Square_size*9))
    menu.blit(Menu["N3"], (Square_size*1, Square_size*9))
    
    
    
    
    
    
    
    
            
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
