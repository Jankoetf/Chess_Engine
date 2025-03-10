class Move():   
    def __init__(self, startSq, endSq, board):
        """
        Creates a move with all informations about it like if it is a castle, a promotion, a en passan...

        Args:
            startSq: starting square of a move, tuple
            ekdSq: ending square of a move, tuple
            board: reference to game board
        """

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
        """
        move types: Promotion, LCastle, SCastle, ENPassan, Basic

        Returns: which type is move
        """
        Special_char = "Promotion" if self.move_is_promotion else "LCastle" if self.is_move_long_castle() \
            else "SCastle" if self.is_move_short_castle() else "ENPassan" if self.move_is_en_passant else "Basic"
        
        return Special_char
        
        
    def __eq__(self, other):
        """checking if two moves have the same starting and ending square"""
        if isinstance(other, Move):
            return self.startSq == other.startSq and self.endSq == other.endSq
    
    def __str__(self):
        return f"({self.startSq}, {self.endSq}), ({self.startSquarePiece}, {self.endSquarePiece})\n"