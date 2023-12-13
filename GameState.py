from Constants import *
import numpy as np



class GameState():
    
    def __init__(self):
        #board is 8*8 2D list, each element of list has 2 characters
        #firts character represents the color of piece
        #second character represents type of piece
        #"--" empty space with no piece
        self.mc = 0
        self.uc = 0
        
        self.board = [["bR",  "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],     
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wP",  "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR",  "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.c_board = [[0.001, 0.002, 0.004, 0.008, 0.008, 0.004, 0.002, 0.001],
                       [0.002, 0.004, 0.008, 0.016, 0.016, 0.008, 0.004, 0.002],
                       [0.004, 0.008, 0.016, 0.032, 0.032, 0.016, 0.008, 0.004],     
                       [0.008, 0.016, 0.032, 0.064, 0.064, 0.032, 0.016, 0.008],
                       [0.008, 0.016, 0.032, 0.064, 0.064, 0.032, 0.016, 0.008],
                       [0.004, 0.008, 0.016, 0.032, 0.032, 0.016, 0.008, 0.004],
                       [0.002,  0.004, 0.008, 0.016, 0.016, 0.008, 0.004, 0.002],
                       [0.001,  0.002, 0.004, 0.008, 0.008, 0.004, 0.002, 0.001]
        ]
        
        
        self.help_board = [["bR",  "bN", "bB", "bQ", "bK", "bB", "--", "bR"],
                          ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                          ["--", "--", "--", "bN", "--", "--", "--", "--"],     
                          ["--", "bP", "--", "--", "--", "--", "--", "wP"],
                          ["--", "--", "bN", "bP", "--", "--", "wP", "--"],
                          ["--", "--", "--", "--", "--", "--", "--", "wR"],
                          ["wP",  "wP", "wP", "wP", "wP", "--", "wP", "wP"],
                          ["wR",  "wN", "--", "--", "wK", "wB", "wN", "--"]
        ]             
        
        self.control_board = [["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],     
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        
        self.board_notation = [["a8",  "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
                              ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                              ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],     
                              ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                              ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                              ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                              ["a2",  "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                              ["a1",  "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
        ]
        
        self.whiteToMove = True
        
        self.AnPassanPossibleNextMove = {}
        
        #king + castle
        self.BlackKingIsInCheck = False
        self.WhiteKingIsInCheck = False
        
        self.BlackKingPosition = (0, 4)
        self.WhiteKingPosition = (7, 4)
        
        self.BlackKingPosition_HELP = (0, 4)
        self.WhiteKingPosition_HELP = (7, 4)
        
        self.WhiteKingFirstMove = 0
        self.BlackKingFirstMove = 0
        
        self.WhiteLongRookFirstMove = 0
        self.WhiteShortRookFirstMove = 0
        self.BlackLongRookFirstMove = 0
        self.BlackShortRookFirstMove = 0
        
        self.RightToCastleWhiteLong = False
        self.RightToCastleWhiteShort = False
        self.RightToCastleBlackLong = False
        self.RightToCastleBlackShort = False
        
        self.ListOfStupidMoves = []
        #['bP(1, 3)(3, 3)--Basic', 'wP(6, 1)(5, 1)--Basic', 'bN(0, 6)(2, 5)--Basic'],
        
        self.ListOfRealMoves = []
        self.black_is_in_check = False
        self.black_is_mated = False
        self.white_is_in_check = False
        self.white_is_mated = False
        self.stalmate = False
        
        
        
        #AI
        self.DEPTH = 2
        
        
    def kings_position(self, board):
        white_king = (7,4)
        black_king = (0,4)
        for c in range(8):
            for r in range(8):
                if board[c][r] == "wK":
                    white_king = (c, r)
                if board[c][r] == "bK":
                    black_king = (c, r)
        return [white_king, black_king]
        
        
    def Rights_to_castle(self):
        self.RightToCastleWhiteLong = self.WhiteKingFirstMove == 0 and self.WhiteLongRookFirstMove == 0
        self.RightToCastleWhiteShort = self.WhiteKingFirstMove == 0 and self.WhiteShortRookFirstMove == 0
        self.RightToCastleBlackLong = self.BlackKingFirstMove == 0 and self.BlackLongRookFirstMove == 0
        self.RightToCastleBlackShort = self.BlackKingFirstMove == 0 and self.BlackShortRookFirstMove == 0
        
    def BlackOrWhiteMove(self):
        s = "It is white turn" if self.whiteToMove else "It is black turn"
        print(s)
        
        
        
    #Control squares
    def Control(self, color, board): #color maybe
        All_Controled_Squares = set() #end square of moves - squares that pieces can attack - set
        
        def Controled_by_pawn(Col, Row, color):
            control_squares = []
            direction, opponent_color = (1,'b') if color == 'w' else (-1,'w')
            if Row <= 6:# and (self.board[Col-direction][Row + 1][0] == color or self.board[Col-direction][Row + 1] == "--"):
                control_squares.append((Col - direction, Row + 1))
            
            if Row >= 1: #and (self.board[Col-direction][Row - 1][0] == color or self.board[Col-direction][Row - 1] == "--"):        
                control_squares.append((Col-direction, Row - 1))
            
            control = set(control_squares)
            return control
          
        def Controled_by_knight(Col, Row, color):
            #opponent_color = 'b' if color == 'w' else 'w'
            control_squares = []
            directions =[(2, -1), (2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2), (-2, 1), (-2, -1)]
            for d in directions:
                if GameState.is_on_the_board(d[0] + Col, d[1] + Row):
                    control_squares.append((d[0] + Col, d[1] + Row))
            control = set(control_squares)
            return control
        
        def Controled_by_bishop(Col, Row, color, board):
            control_squares = []    
            #opponent_color = 'b' if color == 'w' else 'w'
            directions = [(-1,-1), (-1,1), (1, -1), (1,1)]
            for d in directions:
                for i in range(1, 8):
                    if GameState.is_on_the_board(Col + i*d[0], Row + i*d[1]):
                        if board[Col + i*d[0]][Row + i*d[1]] == "--":
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                        
                        #elif self.board[Col + i*d[0]][Row + i*d[1]][0] == color or self.board[Col + i*d[0]][Row + i*d[1]][0] == opponent_color:
                        else:
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                            break
                            
                    else:
                        break
                    
            control = set(control_squares)
            return control
        
        def Controled_by_rook(Col, Row, color, board):
            control_squares = []    
            #opponent_color = 'b' if color == 'w' else 'w'
            directions = [(0,-1), (0,1), (1, 0), (-1,0)]
            for d in directions:
                for i in range(1, 8):
                    if GameState.is_on_the_board(Col + i*d[0], Row + i*d[1]):
                        if board[Col + i*d[0]][Row + i*d[1]] == "--":
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                        else:
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                            break
#                        if self.board[Col + i*d[0]][Row + i*d[1]][0] == color:
#                            control_squares.append((Col + i*d[0],Row + i*d[1]))
#                            break
#                            
#                        if self.board[Col + i*d[0]][Row + i*d[1]] == "--":
#                            control_squares.append((Col + i*d[0],Row + i*d[1]))
#                        else:
#                            break
                    else:
                        break
                    
            control = set(control_squares)
            return control
        
        def Controled_by_queen(Col, Row, color, board):
            control_squares = []    
            #opponent_color = 'b' if color == 'w' else 'w'
            directions = [(0,-1), (0,1), (1, 0), (-1,0), (-1,-1), (-1,1), (1, -1), (1,1)]
            for d in directions:
                for i in range(1, 8):
                    if GameState.is_on_the_board(Col + i*d[0], Row + i*d[1]):
                        if board[Col + i*d[0]][Row + i*d[1]] == "--":
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                            
                        else:
                            control_squares.append((Col + i*d[0],Row + i*d[1]))
                            break
                    else:
                        break
                    
            control = set(control_squares)
            return control
        
        def Controled_by_king(Col, Row, color):
            control_squares = []   
            directions = [(1,0), (-1, -1), (1, 1), (1,-1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
            for d in directions:
                if GameState.is_on_the_board(Col + d[0], Row + d[1]):
                    control_squares.append((Col + d[0], Row + d[1]))
                        
                       
            control = set(control_squares)
            return control
            
        
        for Col in range(8):
            for Row in range(8):
                if board[Col][Row][0] == color and board[Col][Row][1] == "P":
                    All_Controled_Squares.update(Controled_by_pawn(Col, Row, color))
                if board[Col][Row][0] == color and board[Col][Row][1] == "N":
                    All_Controled_Squares.update(Controled_by_knight(Col, Row, color))
                if board[Col][Row][0] == color and board[Col][Row][1] == "B":
                    All_Controled_Squares.update(Controled_by_bishop(Col, Row, color, board))
                if board[Col][Row][0] == color and board[Col][Row][1] == "R":
                    All_Controled_Squares.update(Controled_by_rook(Col, Row, color, board))
                if board[Col][Row][0] == color and board[Col][Row][1] == "Q":
                    All_Controled_Squares.update(Controled_by_queen(Col, Row, color, board))
                if board[Col][Row][0] == color and board[Col][Row][1] == "K":
                    All_Controled_Squares.update(Controled_by_king(Col, Row, color))
        
        #print(All_Controled_Squares)
        return All_Controled_Squares
    
    

            
            
        
        
    def MakeStupidMove(self, move, board):
        #self.Control("b")
        #self.Check()
        #An passan      
        if move.startSquarePiece[1] == 'P' and move.endSquarePiece == "--" and abs(move.endCol - move.startCol) == 2:
            self.AnPassanSquare = (move.endCol - (-1 if self.whiteToMove else 1), move.startRow)
            self.AnPassanPossibleNextMove[len(self.ListOfStupidMoves)+1] = self.AnPassanSquare
            print(f"An passan square is {self.AnPassanPossibleNextMove}")
        
        color = move.startSquarePiece[0]
        op_c = 'b' if color == 'w' else 'w'
        direction = 1 if color == 'w' else -1
        if move.is_move_an_passant():
            if move.endSquarePiece == "--" and move.startSquarePiece[1] == 'P' and board[move.endCol + direction][move.endRow] == (op_c + 'P'):
                board[move.endCol + direction][move.endRow] = "--"
                
        #Castle - hardcode
        if move.is_move_a_castle():
            if color == "w" and self.RightToCastleWhiteLong and self.board[7][1:4] == ["--", "--", "--"] and move.endRow == 2:
                board[7][0], board[7][3] = "--", "wR"
            if color == "w" and self.RightToCastleWhiteShort and self.board[7][5:7] == ["--", "--"] and move.endRow == 6:
                board[7][7], board[7][5] = "--", "wR"
            if color == "b" and self.RightToCastleBlackLong and self.board[0][1:4] == ["--", "--", "--"] and move.endRow == 2:
                board[0][0], board[0][3] = "--", "bR"
            if color == "b" and self.RightToCastleBlackShort and self.board[0][5:7] == ["--", "--"] and move.endRow == 6:
                board[0][7], board[0][5] = "--", "bR"
        
        
        
        if move.startSquarePiece == "wK":
            if self.WhiteKingFirstMove == 0:
                self.WhiteKingFirstMove = len(self.ListOfStupidMoves) + 1
            
        if move.startSquarePiece == "bK":
            if self.BlackKingFirstMove == 0:
                self.BlackKingFirstMove = len(self.ListOfStupidMoves) + 1
            
        if move.startSquarePiece == "wR" and move.startRow == 0:
            if self.WhiteLongRookFirstMove == 0:
                self.WhiteLongRookFirstMove = len(self.ListOfStupidMoves) + 1
            
        if move.startSquarePiece == "wR" and move.startRow == 7:
            if self.WhiteShortRookFirstMove == 0:
                self.WhiteShortRookFirstMove = len(self.ListOfStupidMoves) + 1
            
        if move.startSquarePiece == "bR" and move.startRow == 0:
            if self.BlackLongRookFirstMove == 0:
                self.BlackLongRookFirstMove = len(self.ListOfStupidMoves) + 1
                       
        if move.startSquarePiece == "bR" and move.startRow == 7:
            if self.BlackShortRookFirstMove == 0:
                self.BlackShortRookFirstMove = len(self.ListOfStupidMoves) + 1
            
        if move.startSquarePiece[1] == "K":  
            if color == "w":               
                self.WhiteKingPosition = (move.endCol, move.endRow)
                #print(f"White king: {self.WhiteKingPosition}")
            else: 
                self.BlackKingPosition = (move.endCol, move.endRow)
                #print(f"Black king: {self.BlackKingPosition}")
                
        self.Rights_to_castle()

        
        Signature = move.get_Move_signature()
        
        board[move.startCol][move.startRow] = "--"
        board[move.endCol][move.endRow] = move.startSquarePiece
        #Promotion
        if move.startSquarePiece[1] == "P" and (move.endCol == 0 or move.endCol == 7):
            board[move.endCol][move.endRow] = move.startSquarePiece[0] + "Q"
            
        self.ListOfStupidMoves.append(move.startSquarePiece + str(move.startSq) + str(move.endSq) + move.endSquarePiece + Signature)
        #print(move.startSquarePiece + str(move.startSq) + str(move.endSq) + str(move.endSq) + move.endSquarePiece)
        #print(self.ListOfStupidMoves)
        self.whiteToMove = not self.whiteToMove
        
        
        
    def undoStupidMove(self, board):
    # ['bP(1, 2)(3, 2)--Basic', 'wP(6, 3)(4, 3)--Basic', 'bP(3, 2)(4, 3)wPBasic',
    #  'wP(6, 2)(4, 2)--Basic', 'bP(4, 3)(5, 2)--ENPassan', 'wN(7, 1)(5, 0)--Basic',
    #  'bP(5, 2)(6, 1)wPBasic', 'wN(5, 0)(4, 2)--Basic', 'bP(6, 1)(7, 2)wBPromotion',
    #  'wN(7, 6)(5, 5)--Basic', 'bQ(7, 2)(7, 3)wQBasic', 'wN(4, 2)(2, 3)--Basic',
    #  'bQ(7, 3)(2, 3)wNBasic', 'wK(7, 4)(7, 2)--LCastle']
        if len(self.ListOfStupidMoves) != 0:
            MoveToUndo = self.ListOfStupidMoves.pop()

            #print(MoveToUndo)
            board[int(MoveToUndo[9])][int(MoveToUndo[12])] = MoveToUndo[14:16]
            board[int(MoveToUndo[3])][int(MoveToUndo[6])] = MoveToUndo[0:2]
            
            #An passan rules
            if len(self.ListOfStupidMoves)+1 in self.AnPassanPossibleNextMove:
                self.AnPassanPossibleNextMove.pop(len(self.ListOfStupidMoves)+1)
                print(f"An passan square is {self.AnPassanPossibleNextMove}")
            if MoveToUndo[16:] == "ENPassan":
                op_color = "b" if MoveToUndo[0] == "w" else "w"
                board[int(MoveToUndo[3])][int(MoveToUndo[12])] = op_color + "P"
                
            elif MoveToUndo[16:] == "LCastle":
                op_color = "b" if MoveToUndo[0] == "w" else "w"
                board[7 if op_color == "b" else 0][0] = MoveToUndo[0] + "R"
                board[7 if op_color == "b" else 0][3] = "--"
                if op_color == "w":
                    self.BlackKingFirstMove, self.BlackLongRookFirstMove = 0,0
                else:
                    self.WhiteKingFirstMove, self.WhiteLongRookFirstMove = 0,0
                
            elif MoveToUndo[16:] == "SCastle":
                op_color = "b" if MoveToUndo[0] == "w" else "w"
                board[7 if op_color == "b" else 0][7] = MoveToUndo[0] + "R"
                board[7 if op_color == "b" else 0][5] = "--"
                if op_color == "w":
                    self.BlackKingFirstMove, self.BlackShortRookFirstMove = 0,0
                else:
                    self.WhiteKingFirstMove, self.WhiteShortRookFirstMove = 0,0
                    
            elif MoveToUndo[0:2] == "wK":
                self.WhiteKingPosition = (int(MoveToUndo[3]), int(MoveToUndo[6]))
                if self.WhiteKingFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.WhiteKingFirstMove = 0
                    
                    
            elif MoveToUndo[0:2] == "bK":                
                self.BlackKingPosition = (int(MoveToUndo[3]), int(MoveToUndo[6]))
                if self.BlackKingFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.BlackKingFirstMove = 0
                    
                
            if MoveToUndo[0:2] == "wR" and int(MoveToUndo[6]) == 0:
                #print("Long White Rook Undo")
                if self.WhiteLongRookFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.WhiteLongRookFirstMove = 0
                    
                    
            if MoveToUndo[0:2] == "wR" and int(MoveToUndo[6]) == 7:
                #print("Short White Rook undo")
                if self.WhiteShortRookFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.WhiteShortRookFirstMove = 0
                    
            if MoveToUndo[0:2] == "bR" and int(MoveToUndo[6]) == 0:
                #print("Long Black Rook Undo")
                if self.BlackLongRookFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.BlackLongRookFirstMove = 0
                    
            if MoveToUndo[0:2] == "bR" and int(MoveToUndo[6]) == 7:
                #print("Short Black Rook Undo")
                if self.BlackShortRookFirstMove == (len(self.ListOfStupidMoves) + 1):
                    self.BlackShortRookFirstMove = 0
            
            self.whiteToMove = not self.whiteToMove
            
        self.Rights_to_castle()
        #print(self.ListOfStupidMoves)
        
        
        
    def MakeRealMove(self, move):
        pass
        
    
    def get_all_pawn_moves(self, color, Col, Row, board):
        valid_pawn_moves = []
        
        direction, starting_col, opponent_color = (1,6, 'b') if color == 'w' else (-1,1, 'w')
        
        if board[Col - direction][Row] == "--":        
            valid_pawn_moves.append(Move((Col, Row), (Col - direction, Row), board))
            
            #print(f"StartCol and startRow: {(Col, Row)}, endCol and endRow:{(Col-1, Row)}")
            if Col == starting_col and board[Col - direction][Row] == "--" and board[Col - 2*direction][Row] == "--":
                valid_pawn_moves.append(Move((Col, Row), (Col -2*direction, Row), board))

             
        if Row <= 6 and (board[Col-direction][Row + 1][0] == opponent_color or (len(self.ListOfStupidMoves) in self.AnPassanPossibleNextMove and\
                                                                                self.AnPassanPossibleNextMove[len(self.ListOfStupidMoves)] == (Col-direction,Row + 1))):
            valid_pawn_moves.append(Move((Col, Row), (Col-direction, Row+1), board))
            
        if Row >= 1 and (board[Col-direction][Row - 1][0] == opponent_color or (len(self.ListOfStupidMoves) in self.AnPassanPossibleNextMove and\
                                                                                self.AnPassanPossibleNextMove[len(self.ListOfStupidMoves)] == (Col-direction,Row - 1))):      
            valid_pawn_moves.append(Move((Col, Row), (Col-direction, Row-1), board))
            
               
        return valid_pawn_moves
    
    @staticmethod
    def is_on_the_board(*args):
        for arg in args:
            if arg > 7 or arg < 0:
                return False
        return True
    
    def get_all_knight_moves(self, color, Col, Row, board):
        opponent_color = 'b' if color == 'w' else 'w'
        valid_knight_moves = []
        directions =[(2, -1), (2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2), (-2, 1), (-2, -1)]
        for d in directions:
            if GameState.is_on_the_board(d[0] + Col, d[1] + Row):
                if board[d[0] + Col][d[1] + Row][0] == opponent_color or board[d[0] + Col][d[1] + Row] == '--':
                    valid_knight_moves.append(Move((Col, Row), (d[0] + Col, d[1] + Row), self.board))
        return valid_knight_moves
    
    def get_all_rook_moves(self, color, Col, Row, board):
        valid_rook_moves = []
        opponent_color = 'b' if color == 'w' else 'w'
        directions = [(0,-1), (0,1), (-1, 0), (1, 0)]
        for d in directions:
            for i in range(1, 8):
                if GameState.is_on_the_board(d[0]*i + Col, d[1]*i + Row):
                    if board[Col + d[0]*i][Row + d[1]*i][0] == opponent_color:
                        valid_rook_moves.append(Move((Col, Row), (d[0]*i + Col, d[1]*i + Row), board))
                        break
                    if board[Col + d[0]*i][Row + d[1]*i] == '--':
                        valid_rook_moves.append(Move((Col, Row), (d[0]*i + Col, d[1]*i + Row), board)) 
                    else:
                        break
                else:
                    break
        return valid_rook_moves
    
    def get_all_valid_bishop_moves(self, color, Col, Row, board):
        valid_bishop_moves = []
        opponent_color = 'b' if color == 'w' else 'w'
        directions = [(-1,-1), (-1,1), (1, -1), (1,1)]
        for d in directions:
            for i in range(1, 8):
                if GameState.is_on_the_board(Col + i*d[0], Row + i*d[1]):
                    if board[Col + i*d[0]][Row + i*d[1]][0] == opponent_color:
                        valid_bishop_moves.append(Move((Col, Row),(Col + i*d[0], Row + i*d[1]), board))
                        break
                    if board[Col + i*d[0]][Row + i*d[1]] == "--":
                        valid_bishop_moves.append(Move((Col, Row),(Col + i*d[0], Row + i*d[1]), board))
                    else:
                        break
                else:
                    break
        return valid_bishop_moves
    
    def get_all_queen_moves(self, color, Col, Row, board):
        valid_queen_moves = []
        valid_queen_moves.extend(self.get_all_valid_bishop_moves(color, Col, Row, board))
        valid_queen_moves.extend(self.get_all_rook_moves(color, Col, Row, board))
        return valid_queen_moves
                
    
    def get_all_king_moves(self, color, Col, Row, board):
        opponent_color = 'b' if color == 'w' else 'w'
        valid_king_moves= []
        directions = [(1,0), (-1, -1), (1, 1), (1,-1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
        for d in directions:
            if GameState.is_on_the_board(Col + d[0], Row + d[1]):
                if board[Col + d[0]][Row + d[1]] == "--" or board[Col + d[0]][Row + d[1]][0] == opponent_color:
                    valid_king_moves.append(Move((Col, Row),(Col + d[0], Row + d[1]), board))
         
        #castle move
        if color == "w" and self.RightToCastleWhiteLong and self.board[7][1:4] == ["--", "--", "--"]:
            valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
        if color == "w" and self.RightToCastleWhiteShort and self.board[7][5:7] == ["--", "--"]:
            valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))
        if color == "b" and self.RightToCastleBlackLong and self.board[0][1:4] == ["--", "--", "--"]:
            valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
        if color == "b" and self.RightToCastleBlackShort and self.board[0][5:7] == ["--", "--"]:
            valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))
                    
        return valid_king_moves        
        
    def getAllValidMoves(self, board):
        AllValidMoves = []
        for Col in range(8):
            for Row in range(8):
                #Pawn Moves
                if self.whiteToMove and board[Col][Row] == 'wP':
                    AllValidMoves.extend(self.get_all_pawn_moves('w', Col, Row, board))
                   
                         
                if (not self.whiteToMove) and board[Col][Row] == 'bP':
                   AllValidMoves.extend(self.get_all_pawn_moves('b', Col, Row, board))
                    
                        
                #knight Moves       
                if self.whiteToMove and board[Col][Row] == 'wN':
                    AllValidMoves.extend(self.get_all_knight_moves('w', Col, Row, board))
                    
                
                if (not self.whiteToMove) and board[Col][Row] == 'bN':
                    AllValidMoves.extend(self.get_all_knight_moves('b', Col, Row, board))
                    
                    
                #rook Moves       
                if self.whiteToMove and board[Col][Row] == 'wR':
                    AllValidMoves.extend(self.get_all_rook_moves('w', Col, Row, board))
                    
                
                if (not self.whiteToMove) and board[Col][Row] == 'bR':
                    AllValidMoves.extend(self.get_all_rook_moves('b', Col, Row, board))
                    
                #bishop Moves
                if self.whiteToMove and board[Col][Row] == 'wB':
                    AllValidMoves.extend(self.get_all_valid_bishop_moves('w', Col, Row, board))
                    
                
                if (not self.whiteToMove) and board[Col][Row] == 'bB':
                    AllValidMoves.extend(self.get_all_valid_bishop_moves('b', Col, Row, board))             
                    
                #queen Moves
                if self.whiteToMove and board[Col][Row] == 'wQ':
                    AllValidMoves.extend(self.get_all_queen_moves('w', Col, Row, board))
                    
                
                if (not self.whiteToMove) and board[Col][Row] == 'bQ':
                    AllValidMoves.extend(self.get_all_queen_moves('b', Col, Row, board))  
                    
                #king Moves
                if self.whiteToMove and board[Col][Row] == 'wK':
                    AllValidMoves.extend(self.get_all_king_moves('w', Col, Row, board))
                    
                
                if (not self.whiteToMove) and board[Col][Row] == 'bK':
                    AllValidMoves.extend(self.get_all_king_moves('b', Col, Row, board))  
                    
                
        return AllValidMoves
    
    
    def WhiteKingInCheck(self):
        control = self.Control("b", self.board)
        if self.WhiteKingPosition in control:
            print("Beli je u sahu")
            return True
        else: 
            return False
        
    def BlackKingInCheck(self):
        control = self.Control("w", self.board)
        if self.BlackKingPosition in control:
            print("Crni je u sahu")
            return True
        else: 
            return False
    
    def Check(self):
        if self.whiteToMove:
            #print("beli u sahu")
            return self.WhiteKingInCheck()
        else:
            #print("crni u sahu")
            return self.BlackKingInCheck()
        
    
    def evaluate_board(self, board):
        
        
        pieces_values = {'bP': -1.0, 'bB': -3.3, 'bN': -3.0, 'bR': -5.0, 'bQ': -9.0, 'bK':-1000,
                 'wP': 1.0, 'wB': 3.3, 'wN': 3.0, 'wR': 5.0, 'wQ': 9.0, "--": 0, 'wK': 1000}
        evaluation = 0
        for Col in range(8):
            for Row in range(8):
                evaluation += pieces_values[board[Col][Row]]
                
        control_temp = self.Control('b', self.board)
        for con in control_temp:
            evaluation -= self.c_board[con[0]][con[1]]
            
        control_temp = self.Control('w', self.board)
        for con in control_temp:
            evaluation += self.c_board[con[0]][con[1]]
            
        #control_temp = self.Control('b', self.board)
        # for con in control_temp:
        #     score = 6 - m.floor(abs(con[0] - 3.5)) - m.floor(abs(con[1] - 3.5))
        #     evaluation -= 0.001*(2**(score))
            
        # control_temp = self.Control('w', self.board)
        # for con in control_temp:
        #     score = 6 - m.floor(abs(con[0] - 3.5)) - m.floor(abs(con[1] - 3.5))
        #     evaluation += 0.001*(2**(score))
        
        # control_temp = self.Control('b', self.board)
        # for con in control_temp:
        #     score = 6 - (abs(con[0] - 3.5))//1 - (abs(con[1] - 3.5))//1
        #     evaluation -= 0.001*(2**(score))
            
        # control_temp = self.Control('w', self.board)
        # for con in control_temp:
        #     score = 6 - (abs(con[0] - 3.5))//1 - (abs(con[1] - 3.5))//1
        #     evaluation += 0.001*(2**(score))
            
        #floor: a//1, ceil: -(-a // 1) !
        # def ceil(n):
        #     return int(-1 * n // 1 * -1)
        
        # def floor(n):
        #     return int(n // 1)
        
            
        return evaluation
    
    
    def min_max_max(self, alpha, beta, depth):
        pass
    
    def min_max_min(self, alpha, beta, depth):
        pass
    
    def min_max_alpha_beta(self, board, depth, isMaximizePlayer, alpha, beta, who_is_playing):
        m = 1 if who_is_playing == "w" else -1
        ai_moves_val = []
        
        if depth == self.DEPTH:
            return_value = m * self.evaluate_board(board)
            #self.undoStupidMove(board)
            #self.uc +=1
            return return_value
        
        if isMaximizePlayer:
            bestVal = -1000
            moves = self.get_all_legit_moves(board)
            # if depth == 0:
            #     num_of_first_moves = len(moves)
                
            for move in moves:
                self.MakeStupidMove(move, board)
                self.mc +=1
                value = self.min_max_alpha_beta(board, depth +1, False, alpha, beta, who_is_playing)
                bestVal = max(bestVal, value)
                alpha = max(alpha, bestVal)
                self.undoStupidMove(board)
                self.uc += 1
                if depth == 0:
                    ai_moves_val.append(bestVal)
                if beta <= alpha:
                    break
                
            if depth == 0:
                if len(ai_moves_val) != 0:
                    self.MakeStupidMove(moves[np.argmax(ai_moves_val)], board)
                
            return bestVal
        
        else:
            bestVal = 1000
            moves = self.get_all_legit_moves(board)
            for move in moves:
                self.MakeStupidMove(move, board)
                self.mc +=1
                value = self.min_max_alpha_beta(board, depth +1, True, alpha, beta, who_is_playing)
                bestVal = min(bestVal, value)
                alpha = min(alpha, bestVal)
                self.undoStupidMove(board)
                self.uc +=1
                if depth == 0:
                    ai_moves_val.append(bestVal)
                if beta <= alpha:
                    break
            if depth == 0:
                self.MakeStupidMove(moves[np.argmax(ai_moves_val)],board)                    
                    
            return bestVal
            
    
    def get_AI_move(self, alpha, beta, depth):
        pass
        
        
        
    def get_all_legit_moves(self, board):
        moves = self.getAllValidMoves(self.board)
        #controled_squares = self.Control("b") if self.whiteToMove else self.Control("w")
        #self.help_board = self.board
        for i in range(len(moves) -1, -1, -1):
            move_removed = False
            move = moves[i]
            self.MakeStupidMove(move, self.board)
            self.whiteToMove = not self.whiteToMove
            
            
            if self.whiteToMove:
                control = self.Control("b", self.board)
                #print(self.WhiteKingPosition)
                if self.WhiteKingPosition in control:
                    moves.remove(move)
                    move_removed = True
            else:
                control = self.Control("w", self.board)
                #print(self.BlackKingPosition)
                if self.BlackKingPosition in control:
                    moves.remove(move)
                    move_removed = True
                    
            if move.is_move_a_castle() and (not move_removed):
                if move.is_move_long_castle():
                    if move.startSquarePiece == "wK":
                        if (7, 3) in control or (7, 4) in control:
                            moves.remove(move)
                    else:
                        if (0, 3) in control or (0, 4) in control:
                            moves.remove(move)
                else:
                    if move.startSquarePiece == "wK":
                        if (7, 4) in control or (7, 5) in control:
                            moves.remove(move)
                    else:
                        if (0, 4) in control or (0, 5) in control:
                            moves.remove(move)
                            
            
            self.undoStupidMove(self.board)
            self.whiteToMove = not self.whiteToMove
        
        #for m in moves:
            #print(m.startSquarePiece + str(m.startSq) + str(m.endSq) + m.endSquarePiece + move.get_Move_signature())
            
        return moves
                
        
class Move():   
    def __init__(self, startSq, endSq, board):
        #Start end squares
        self.startSq = startSq
        self.endSq = endSq
        self.startCol = startSq[0]
        self.startRow = startSq[1]
        self.endCol = endSq[0]
        self.endRow = endSq[1]
        self.startSquarePiece = board[self.startCol][self.startRow]
        self.endSquarePiece = board[self.endCol][self.endRow]
        
        #Special options
        self.move_is_en_passant = self.is_move_an_passant()
        self.move_is_promotion = self.is_move_a_promotion()
        self.move_is_castle = self.is_move_a_castle()
        self.whos_turn = 1 if board[self.startCol][self.startRow][0] == 'w' else -1
        

    
    
    def is_move_an_passant(self):
        return self.startSquarePiece[1] == 'P' and self.endSquarePiece == '--' and (self.startRow != self.endRow)
        
    def is_move_a_castle(self):
        return self.startSquarePiece[1] == 'K' and self.endSquarePiece == '--' and\
            abs(self.startRow - self.endRow) == 2 and abs(self.startCol - self.endCol) == 0 and (self.startCol in [0,7])
    
    def is_move_short_castle(self):
        return self.is_move_a_castle() and self.endRow == 6
    
    def is_move_long_castle(self):
        return self.is_move_a_castle() and self.endRow == 2
    
    def is_move_a_promotion(self):
        return (self.endCol == 7 or self.endCol == 0) and self.startSquarePiece[1] == "P"
    
    def get_Move_signature(self):
        Special_char = "Promotion" if self.move_is_promotion else "LCastle" if self.is_move_long_castle() \
            else "SCastle" if self.is_move_short_castle() else "ENPassan" if self.move_is_en_passant else "Basic"
        #return self.startSquarePiece + self.endSquarePiece + Special_char
        return Special_char
        
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.startSq == other.startSq and self.endSq == other.endSq
        
    
        
    
        
class Square():
    piece_values = {'bP': -1.0, 'bB': -3.3, 'bN': -3.0, 'bR': -5.0, 'bQ': -9.0,
                     'wP': 1.0, 'wB': 3.3, 'wN': 3.0, 'wR': 5.0, 'wQ': 9.0}
      
    def __init__(self, Col, Row):
        self.col = Col
        self.row = Row
        self.empty = True
        self.piece = None
        
    def add_piece(self, piece):
        self.piece = piece
        
    def square_value(self, piece):
        #value = piece_values[piece]
        #return value
        pass
    
    
        
        
    def is_square_empty(self):
        return self.empty



    