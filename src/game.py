import pygame as pg
from src.board import Board
from src.constans import Constants
from src.state import GameState
from src.cell_state import CellState
from src.hints import clear_hints
from src.click_event import white_click_handler, black_click_handler

class Checkers:
    SINGLE_PLAYER = 1
    TWO_PLAYERS = 2
    def __init__(self, mode) -> None:
        pg.init()
        pg.display.set_caption("Checkers")
        self.screen = pg.display.set_mode((Constants.CELL_COUNT * Constants.CELL_SIZE, Constants.CELL_COUNT * Constants.CELL_SIZE))
        self.board = Board(self.screen)
        self.state = GameState(self.screen)
        self.mode = mode

    def run(self, onEnd):
        while True:
            try:
                if self.state.is_game_over():
                    print("Game Over")
                    onEnd(self)
                    pg.quit()
                    return
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        return
                    if event.type == pg.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        row = y // Constants.CELL_SIZE
                        col = x // Constants.CELL_SIZE
                        self.handle_click(row, col)
                self.board.draw()
                self.state.draw()
                pg.display.update()
            except Exception as e:
                # raise e
                print(e)
    
    def handle_click(self, row, col):
        
        # if an empty cell is clicked no need to do anything
        if self.state.pieces[row][col] == CellState.EMPTY:
            clear_hints(self.state)
            self.state.selected = None
            self.state.possible_moves = []
            self.state.possible_jumps = {}
            return
        if self.state.player.is_white():
            white_click_handler(self, row, col)
        elif self.mode == Checkers.TWO_PLAYERS:
            black_click_handler(self, row, col)
        else:
            pass