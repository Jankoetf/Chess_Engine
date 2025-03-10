import numpy as np
import threading

from chess_engine.constants import *

class AiClass:
    def __init__(self, game_state_instance):
        """
        Responsible for AI moves, uses alpha-beta prunning algorithm for finding best move

        Args:
            game_state_instance (GameState): reference to GameState
        """

        self.pieces_values = { #standard piece evaluation, Bishop is usualy considered stronger than Knight
            'bP': -1.0, 'bB': -3.3, 'bN': -3.0, 'bR': -5.0, 'bQ': -9.0, 'bK':-1000,
            'wP': 1.0, 'wB': 3.3, 'wN': 3.0, 'wR': 5.0, 'wQ': 9.0, "--": 0, 'wK': 1000
        }

        #control squares -> center is most important -> so it will give more points to heuristic
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

        self.game_state_instance = game_state_instance #reference to game state instance
        self.thinking_thread = None #thread is instance atribut, more options

    def evaluate_board(self):
        """
        this is always from white players's perspective, used heuristic consists of:
        - piece evaluation
        - center control
        - checking oponent 

        Returns:
            evaluation (float) : evaluation for the whole board, from white's perspective
        """
        evaluation = 0

        #mate
        if self.game_state_instance.black_is_mated:
            evaluation = 1000
            return evaluation
        if self.game_state_instance.white_is_mated:
            evaluation = -1000
            return evaluation

        #classical piece evaluation, each piece is valuable
        for Col in range(8):
            for Row in range(8):
                evaluation += self.pieces_values[self.game_state_instance.board[Col][Row]]

        #positional evaluation
        control_temp = self.game_state_instance.Control('b', self.game_state_instance.board)
        for con in control_temp:
            evaluation -= self.c_board[con[0]][con[1]]
            
        control_temp = self.game_state_instance.Control('w', self.game_state_instance.board)
        for con in control_temp:
            evaluation += self.c_board[con[0]][con[1]]

        # check
        if self.game_state_instance.BlackKingInCheck():
            evaluation += 1
        elif self.game_state_instance.WhiteKingInCheck():
            evaluation -= 1
        
        return evaluation

    def min_max_alpha_beta(self, board, depth, isMaximizePlayer, alpha, beta, who_is_playing):
        """
        Implements the minimax algorithm enhanced with alpha-beta pruning, used when AI is playing.
        This function will also automaticaly play the best found move

        This function uses the classical minimax approach to determine the optimal move, but with a crucial
        optimization: alpha-beta pruning. Instead of exploring every branch of the game tree, alpha-beta
        pruning eliminates paths that cannot possibly influence the final decision.

        Parameters:
            board: The current state of the game board.
            depth (int): The maximum depth to search in the game tree. When depth reaches zero or a terminal
                        state is encountered, the board is evaluated
            isMaximizePlayer (bool): True if the current move is for the maximizing player; False for the minimizing player
            alpha: The best value that the maximizing player is assured of so far
            beta: The best value that the minimizing player is assured of so far
            who_is_playing: white or black, w or b

        Returns:
            The evaluated score of the board state after applying the minimax algorithm with alpha-beta pruning.
        """
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
                
            if depth == 0 and len(ai_moves_val) > 0:
                self.game_state_instance.MakeStupidMove(moves[np.argmax(ai_moves_val)], board)
                self.game_state_instance.get_all_legit_moves()
            
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
            if depth == 0 and len(ai_moves_val) > 0:
                self.game_state_instance.MakeStupidMove(moves[np.argmax(ai_moves_val)],board)
                self.game_state_instance.get_all_legit_moves()
            
            return bestVal
        
    def make_best_move_threaded(self, white_is_playing, callback):
        """
        Starts a separate thread to compute the AI move using the minimax algorithm with alpha-beta pruning,
        ensuring that the GUI remains responsive during the calculation.

        
        Initiates a daemon thread that calls the 'min_max_alpha_beta' method with appropriate parameters.
        A daemon thread is a background thread that will not block the main program from exiting; 
        it is automatically terminated when the main thread (in this case, the GUI)
        Once the move evaluation is complete, the provided callback function is executed to update the UI state
        (e.g., to signal that the AI is no longer thinking)

        Parameters:
            white_is_playing (bool): True if the white player is to move; False otherwise.
            callback (callable): A function to be called after the move evaluation is complete, used for UI state updates.

        Returns:
            bool: True if the background thread is successfully started.
        """

        who_is_playing = "w" if white_is_playing else "b"
        def thinking_thread():
            try:
                if who_is_playing == "w":
                    self.min_max_alpha_beta(self.game_state_instance.board, 0, True, -1000, 1000, "w")
                elif who_is_playing == "b":
                    self.min_max_alpha_beta(self.game_state_instance.board, 0, True, -1000, 1000, "b")
                
                callback() #communication with ui state through callback, ai_thinking is set to True in main.py, here it will be set to False again
            
            except Exception as e:
                print(f"Error with AI: {e}")
        
        self.thinking_thread = threading.Thread(target=thinking_thread)
        self.thinking_thread.daemon = True  # thread will stop when main program is stopped
        self.thinking_thread.start()
        
        return True

