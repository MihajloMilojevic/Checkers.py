import pygame as pg
from src.hints import clear_hints, draw_hints
from src.cell_state import CellState
from src.constans import Constants
from src.player import Player

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.selected = None
        self.possible_moves = []
        self.possible_jumps = {}
        self.pieces = [
            [CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK],
            [CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY],
            [CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK, CellState.EMPTY, CellState.BLACK],
            [CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY],
            [CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY, CellState.EMPTY],
            [CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY],
            [CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE],
            [CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY, CellState.WHITE, CellState.EMPTY]
        ]
    
    def draw(self):
        for row_index in range(Constants.CELL_COUNT):
            for cell_index in range(Constants.CELL_COUNT):
                if self.pieces[row_index][cell_index] == CellState.EMPTY:
                    continue
                radius = Constants.PIECE_SIZE
                center_x = cell_index * Constants.CELL_SIZE + Constants.CELL_SIZE // 2
                center_y = row_index * Constants.CELL_SIZE + Constants.CELL_SIZE // 2
                isCurrentPlayer = False
                isQueen = self.pieces[row_index][cell_index] in [CellState.WHITE_QUEEN, CellState.BLACK_QUEEN]
                if self.pieces[row_index][cell_index] in [CellState.WHITE, CellState.WHITE_QUEEN]:
                    color = Constants.WHITE_COLOR
                    queen_color = Constants.WHITE_QUEEN_COLOR
                    if self.player.is_white():
                        isCurrentPlayer = True
                elif self.pieces[row_index][cell_index] in [CellState.BLACK, CellState.BLACK_QUEEN]:
                    color = Constants.BLACK_COLOR
                    queen_color = Constants.BLACK_QUEEN_COLOR
                    if self.player.is_black():
                        isCurrentPlayer = True
                elif self.pieces[row_index][cell_index] == CellState.MOVE:
                    color = (0, 0, 200)
                    radius = Constants.MOVE_JUMP_SIZE
                elif self.pieces[row_index][cell_index] == CellState.JUMP:
                    color = (0, 200, 0)
                    radius = Constants.MOVE_JUMP_SIZE
                pg.draw.circle(
                    self.screen, 
                    color, 
                    (center_x, center_y),   
                    radius
                )
                if isQueen:
                    pg.draw.circle(
                        self.screen, 
                        queen_color, 
                        (center_x, center_y),   
                        Constants.QUEEN_SIZE
                    )
                if isCurrentPlayer:
                    pg.draw.circle(
                        self.screen, 
                        (0, 255, 255), 
                        (center_x, center_y),   
                        radius,
                        2
                    )
