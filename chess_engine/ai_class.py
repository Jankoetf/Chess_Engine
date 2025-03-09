import numpy as np

from chess_engine.constants import *

class AiClass:
    def __init__(self, game_state_instance):
        self.pieces_values = {
            'bP': -1.0, 'bB': -3.3, 'bN': -3.0, 'bR': -5.0, 'bQ': -9.0, 'bK':-1000,
            'wP': 1.0, 'wB': 3.3, 'wN': 3.0, 'wR': 5.0, 'wQ': 9.0, "--": 0, 'wK': 1000
        }

        self.c_board = [
            [0.001, 0.002, 0.004, 0.008, 0.008, 0.004, 0.002, 0.001],
            [0.002, 0.004, 0.008, 0.016, 0.016, 0.008, 0.004, 0.002],
            [0.004, 0.008, 0.016, 0.032, 0.032, 0.016, 0.008, 0.004],     
            [0.008, 0.016, 0.032, 0.064, 0.064, 0.032, 0.016, 0.008],
            [0.008, 0.016, 0.032, 0.064, 0.064, 0.032, 0.016, 0.008],
            [0.004, 0.008, 0.016, 0.032, 0.032, 0.016, 0.008, 0.004],
            [0.002,  0.004, 0.008, 0.016, 0.016, 0.008, 0.004, 0.002],
            [0.001,  0.002, 0.004, 0.008, 0.008, 0.004, 0.002, 0.001]
        ]

        self.game_state_instance = game_state_instance

    def evaluate_board(self):
        evaluation = 0
        for Col in range(8):
            for Row in range(8):
                evaluation += self.pieces_values[self.game_state_instance.board[Col][Row]]
                
        control_temp = self.game_state_instance.Control('b', self.game_state_instance.board)
        for con in control_temp:
            evaluation -= self.c_board[con[0]][con[1]]
            
        control_temp = self.game_state_instance.Control('w', self.game_state_instance.board)
        for con in control_temp:
            evaluation += self.c_board[con[0]][con[1]]
            
        return evaluation

    def min_max_alpha_beta(self, board, depth, isMaximizePlayer, alpha, beta, who_is_playing):
        m = 1 if who_is_playing == "w" else -1
        ai_moves_val = []
        
        if depth == AI_DEPTH:
            return_value = m * self.evaluate_board()
            return return_value
        
        if isMaximizePlayer:
            bestVal = -1000
            moves = self.game_state_instance.get_all_legit_moves()
                
            for move in moves:
                self.game_state_instance.MakeStupidMove(move, board)
                value = self.min_max_alpha_beta(board, depth +1, False, alpha, beta, who_is_playing)
                bestVal = max(bestVal, value)
                alpha = max(alpha, bestVal)
                self.game_state_instance.undoStupidMove(board)
                if depth == 0:
                    ai_moves_val.append(bestVal)
                if beta <= alpha:
                    break
                
            if depth == 0:
                if len(ai_moves_val) != 0:
                    self.game_state_instance.MakeStupidMove(moves[np.argmax(ai_moves_val)], board)
                
            return bestVal
        
        else:
            bestVal = 1000
            moves = self.game_state_instance.get_all_legit_moves()
            for move in moves:
                self.game_state_instance.MakeStupidMove(move, board)

                value = self.min_max_alpha_beta(board, depth +1, True, alpha, beta, who_is_playing)
                bestVal = min(bestVal, value)
                alpha = min(alpha, bestVal)
                self.game_state_instance.undoStupidMove(board)
                if depth == 0:
                    ai_moves_val.append(bestVal)
                if beta <= alpha:
                    break
            if depth == 0:
                self.game_state_instance.MakeStupidMove(moves[np.argmax(ai_moves_val)],board)                    
                    
            return bestVal

    