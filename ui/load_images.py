"""Loading all images"""
from chess_engine.constants import *
import pygame as p

class LoadImages:
    def __init__(self):
        self.pieces_names = [
            "bK", "bQ", "bN", "bR", "bP", "bB", "bK_w", "bK_l", "wP", "wR","wN", "wB", "wK", "wQ", "wK_w", "wK_l"
        ]
        self.menu_images_size_map = {
            "menu1":(1,1, ".png"), "sound2":(1,1, ".png"), "sound1":(1,1, ".png"), "Robots2":(1,1, ".png"),
            **{"background"+str(i):(BASE_DIMENSION + 2, BASE_DIMENSION + 1, ".jpg") for i in range(1, 4)},
            "N2":(1,1, ".jpg"), "N1":(2,1, ".jpeg"), "N3":(2,1, ".jpg"), "Robots":(2,1, ".jpg"),
            "Robots3":(1,1, ".jpg"), "whiteK2":(1,1, ".jpg"), "blackK2":(1,1, ".png"), "blackK":(1,1, ".jpg"), "whiteK":(1,1, ".jpg")
        }

        self.piece_images_map = {}
        self.meni_images_map = {}

        self.load_piece_images()
        self.load_menu_images()

    def get_all_images(self):
        print(self.piece_images_map, len(self.piece_images_map))
        return self.piece_images_map, self.meni_images_map
    
    def load_piece_images(self):
        for piece in self.pieces_names:
            self.piece_images_map[piece] = p.transform.scale(
                    p.image.load("Images/" + piece + ".png"),
                    (SQUARE_SIZE, SQUARE_SIZE))

    def load_menu_images(self):
        for name, size_type in self.menu_images_size_map.items():
            self.meni_images_map[name] = p.transform.scale(
                    p.image.load("ImgsMenu/" + name + size_type[2]),
                    (size_type[0]*SQUARE_SIZE, size_type[1]*SQUARE_SIZE))
        
        