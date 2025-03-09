from chess_engine.constants import *
from chess_engine.move import Move

class GameState():
    #test boards
    board_test_1 = [
        ["bR",  "bN", "bB", "--", "bK", "--", "--", "--"],
        ["bP", "bP", "bP", "bP", "bP", "--", "--", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],     
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "bQ", "wQ", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP",  "wP", "wP", "--", "wP", "wR", "wP", "wP"],
        ["--",  "wN", "wB", "wQ", "wK", "wB", "wN", "--"]
    ]

    board_test_2 = [
        ["--",  "--", "--", "--", "bK", "--", "--", "--"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],     
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "wQ", "bQ", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP",  "wP", "--", "wR", "wP", "--", "wP", "wP"],
        ["--",  "wN", "wB", "--", "wK", "wB", "wN", "--"]
    ]

    board_test_2 = [
        ["--",  "wK", "--", "--", "bK", "--", "--", "bR"],
        ["bN", "bN", "bN", "bP", "bP", "bP", "bP", "bP"],
        ["bB", "bB", "bB", "--", "--", "--", "--", "--"],     
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "wQ", "bQ", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP",  "wP", "--", "wR", "wP", "--", "wP", "wP"],
        ["--",  "--", "wB", "--", "--", "wB", "wN", "--"]
    ]

    def __init__(self, start_board = None):
        """
        board is 8*8 2D list, each element of list has 2 characters
        firts character represents the color of piece
        second character represents type of piece
        "--" empty space with no piece

        Args:
            start_board: used for testing different positions, by default is None
        """
       
        self.board_default = [
            ["bR",  "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],     
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP",  "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR",  "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.board = start_board if start_board != None else self.board_default
        
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
        
        self.ListOfStupidMoves = [] #this is an example: ['bP(1, 3)(3, 3)--Basic', 'wP(6, 1)(5, 1)--Basic', 'bN(0, 6)(2, 5)--Basic']
        
        self.black_is_in_check = False
        self.black_is_mated = False
        self.white_is_in_check = False
        self.white_is_mated = False
        self.stalmate = False
        
        
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
    def Control(self, color, board):
        """
        Computes the set of squares controlled (attacked) by all pieces of a given color on the board.

        This method aggregates the squares that can potentially be attacked or reached by the pieces of the specified color.
        It defines and uses local helper functions (e.g., Controled_by_pawn, Controled_by_knight) to calculate control
        for individual piece types, such as pawns and knights. The resulting set represents all unique board coordinates
        that are under control by the pieces of that color.

        Args:
            color (str): The color of the pieces to evaluate ('w' for white or 'b' for black).
            board (list[list]): The current board state

        Returns:
            set: A set of tuples, where each tuple represents the coordinates (row, column) of a square controlled by the specified color
        """
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
        
        #print(All_Controled_Squares) #debug
        return All_Controled_Squares
        
    def MakeStupidMove(self, move, board):
        """
        Executes a move on the board without verifying full move legality.

        This method applies the given move (an instance of the Move class) to the board,
        updating the game state in a "brute-force" manner. It handles special moves such as
        en passant, castling, and pawn promotion by modifying both the board and various internal
        state variables (e.g., king and rook first-move flags, king positions, and castling rights).
        
        Note that this move execution does not check for situations like leaving the king in check;
        it simply updates the board and state, and records the move in the ListOfStupidMoves.

        Parameters:
            move: An instance of the Move class representing the move to be executed.
            board (list): A 2D list representing the current state of the chess board.

        Side Effects:
            - Updates the board by moving the piece from the start square to the end square.
            - Handles en passant by setting the en passant square and capturing the appropriate pawn.
            - Processes castling by moving the rook accordingly when conditions are met.
            - Updates first-move flags for kings and rooks, and updates king positions.
            - Promotes a pawn to a queen if it reaches the back rank.
            - Appends the move's signature to the ListOfStupidMoves.
            - Toggles the side to move (whiteToMove).
        """
        #An passan      
        if move.startSquarePiece[1] == 'P' and move.endSquarePiece == "--" and abs(move.endCol - move.startCol) == 2:
            self.AnPassanSquare = (move.endCol - (-1 if self.whiteToMove else 1), move.startRow)
            self.AnPassanPossibleNextMove[len(self.ListOfStupidMoves)+1] = self.AnPassanSquare
            #print(f"An passan square is {self.AnPassanPossibleNextMove}")
        
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
        """
        Reverts the last executed move from the game state without full move legality checks.

        This method undoes the most recent move recorded in ListOfStupidMoves by parsing its encoded string
        and restoring the board to its previous state. It handles special cases including en passant,
        long castling, short castling, and pawn promotions by reversing the changes made to the board.
        Additionally, it updates internal state variables such as king positions, first-move flags for kings
        and rooks, mating status, and toggles the active player (whiteToMove). Finally, it recalculates
        the castling rights by calling the Rights_to_castle() method.

        Args:
            board (list): A 2D list representing the current state of the chess board

        Example of coded moves:
            ['bP(1, 2)(3, 2)--Basic', 'wP(6, 3)(4, 3)--Basic', 'bP(3, 2)(4, 3)wPBasic',
            'wP(6, 2)(4, 2)--Basic', 'bP(4, 3)(5, 2)--ENPassan', 'wN(7, 1)(5, 0)--Basic',
            'bP(5, 2)(6, 1)wPBasic', 'wN(5, 0)(4, 2)--Basic', 'bP(6, 1)(7, 2)wBPromotion',
            'wN(7, 6)(5, 5)--Basic', 'bQ(7, 2)(7, 3)wQBasic', 'wN(4, 2)(2, 3)--Basic',
            'bQ(7, 3)(2, 3)wNBasic', 'wK(7, 4)(7, 2)--LCastle']
        """
        
        if len(self.ListOfStupidMoves) != 0:
            MoveToUndo = self.ListOfStupidMoves.pop()

            #print(MoveToUndo)
            board[int(MoveToUndo[9])][int(MoveToUndo[12])] = MoveToUndo[14:16]
            board[int(MoveToUndo[3])][int(MoveToUndo[6])] = MoveToUndo[0:2]
            
            #An passan rules
            if len(self.ListOfStupidMoves)+1 in self.AnPassanPossibleNextMove:
                self.AnPassanPossibleNextMove.pop(len(self.ListOfStupidMoves)+1)
                #print(f"An passan square is {self.AnPassanPossibleNextMove}")
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
                    
            if self.white_is_mated: self.white_is_mated = False
            if self.black_is_mated: self.black_is_mated = False
            
            self.whiteToMove = not self.whiteToMove
            
        self.Rights_to_castle()
        #print(self.ListOfStupidMoves)
    
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
         
        #castle moves
        if Col == 7 and Row == 4 and color == "w":
            if self.board[7][0] == "wR" and self.RightToCastleWhiteLong and self.board[7][1:4] == ["--", "--", "--"]:
                valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
            if self.board[7][7] == "wR" and self.RightToCastleWhiteShort and self.board[7][5:7] == ["--", "--"]:
                valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))

        if Col == 0 and Row == 4 and color == "b":
            if self.board[0][0] == "bR" and self.RightToCastleBlackLong and self.board[0][1:4] == ["--", "--", "--"]:
                valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
            if self.board[0][7] == "bR" and self.RightToCastleBlackShort and self.board[0][5:7] == ["--", "--"]:
                valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))


        # if self.board[7][7] == "bR" and self.board[7][4] == "bK" and self.RightToCastleWhiteLong and self.board[7][1:4] == ["--", "--", "--"]:
        #     valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
        # if color == "w" and self.RightToCastleWhiteShort and self.board[7][5:7] == ["--", "--"]:
        #     valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))

        # if color == "b" and self.RightToCastleBlackLong and self.board[0][1:4] == ["--", "--", "--"]:
        #     valid_king_moves.append(Move((Col, Row),(Col, Row - 2), board))
        # if color == "b" and self.RightToCastleBlackShort and self.board[0][5:7] == ["--", "--"]:
        #     valid_king_moves.append(Move((Col, Row),(Col, Row + 2), board))
                    
        return valid_king_moves        
        
    def getAllValidMoves(self, board):
        """
        Generates a list of Move instances representing all valid moves for the current player based on the board state. The moves generated follow
        the standard movement rules for each chess piece but do not account for situations where the king remains in check after a move.

        This method iterates through every square of the 8x8 board and, for the current player (determined by self.whiteToMove),
        collects moves for each piece by invoking piece-specific helper methods (e.g., get_all_pawn_moves, get_all_knight_moves,
        get_all_rook_moves, get_all_valid_bishop_moves, get_all_queen_moves, and get_all_king_moves). 
        In other words, while the moves are valid with respect to basic chess movement rules, they do not verify whether a move
        resolves a check condition.

        Args:
            board (list): A 2D list representing the current chess board state, where each element is a string indicating the piece
                        ('wP' for white pawn, 'bK' for black king, '--' for an empty square ...)

        Returns:
            list: A list of Move class instances representing all basic valid moves available for the current player.
                These moves may include invalid moves that do not escape from check.
        """
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
            # print("Beli je u sahu")
            return True
        else: 
            return False
        
    def BlackKingInCheck(self):
        control = self.Control("w", self.board)
        if self.BlackKingPosition in control:
            # print("Crni je u sahu")
            return True
        else: 
            return False
    
    def Check(self):
        if self.whiteToMove:
            return self.WhiteKingInCheck()
        else:
            return self.BlackKingInCheck()
            
    
    def get_all_legit_moves(self):
        """
        Returns a list of legal moves (as Move instances) for the current player by filtering out moves
        that would leave the king in check.

        This method first generates all potential moves based on standard piece movement rules using
        getAllValidMoves. It then iterates over the list of moves in reverse order, temporarily executing
        each move with MakeStupidMove and toggling the active player. After the move is made, the method
        calculates the opponent's controlled squares using the Control method. If the current player's king
        is found in these controlled squares, the move is removed from the list. Special checks are performed
        for castling moves to ensure that the intermediate squares are not attacked. After evaluating each move,
        the move is undone using undoStupidMove and the active player is reverted.

        Additionally, if no legal moves remain and the king is in check, the appropriate mating flag (black_is_mated
        or white_is_mated) is set.

        Returns:
            list: A list of Move instances representing all legal moves that do not leave the king in check.
        """
        moves = self.getAllValidMoves(self.board)
        #controled_squares = self.Control("b") if self.whiteToMove else self.Control("w")
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

        if len(moves) == 0 and self.BlackKingInCheck():
                self.black_is_mated = True
                # print("GAME STATE CLASS: black_is_mated")
        if len(moves) == 0 and self.WhiteKingInCheck():
                self.white_is_mated = True
                # print("GAME STATE CLASS: white_is_mated")
            
        return moves
            



    