import pygame as pg
from src.hints import calucate_moves, calcuate_jumps, clear_hints
from src.cell_state import CellState
from src.constans import Constants
from src.player import Player

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.winner = None
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
        self.number_white_queens = 0
        self.number_black_queens = 0
        self.number_white_pieces = 12
        self.number_black_pieces = 12
        self.white_centar_rate = 20
        self.black_centar_rate = 20
        self.white_defences = 9
        self.black_defences = 9
        self.white_positions = {(5, 0), (5, 2), (5, 4), (5, 6), (6, 1), (6, 3), (6, 5), (6, 7), (7, 0), (7, 2), (7, 4), (7, 6)}
        self.black_positions = {(0, 1), (0, 3), (0, 5), (0, 7), (1, 0), (1, 2), (1, 4), (1, 6), (2, 1), (2, 3), (2, 5), (2, 7)}
        self.center_matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.current_player_moves = {(5, 0): {(4, 1, None)}, (5, 2): {(4, 1, None), (4, 3, None)}, (5, 4): {(4, 3, None), (4, 5, None)}, (5, 6): {(4, 5, None), (4, 7, None)}}
    
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

    def make_move(self, from_cell, to_cell=None, path=None):
        if path is None:
            self.__move_piece(from_cell, to_cell)
        else:
            self.__jump_path(from_cell, path)
        self.player.change_player()
        clear_hints(self)
        self.calculacte_moves()
        self.is_game_over()
        print(self.current_player_moves)
        print(self.white_positions)
        print(self.black_positions)
        for i in range(8):
            for j in range(8):
                print(self.pieces[i][j], end=" ")
            print()

    # all of the unnecessary calculations are for quicker calucation of the heuristic

    def __delete_piece(self, row, col):
        if self.pieces[row][col] == CellState.WHITE:
            self.number_white_pieces -= 1
            self.white_positions.remove((row, col))
            self.white_defences = self.__calculate_defence(7)
        elif self.pieces[row][col] == CellState.BLACK:
            self.number_black_pieces -= 1
            self.black_positions.remove((row, col))
            self.white_defences = self.__calculate_defence(0)
            self.black_centar_rate -= self.center_matrix[row][col]
        elif self.pieces[row][col] == CellState.WHITE_QUEEN:
            self.number_white_queens -= 1
            self.white_centar_rate -= self.center_matrix[row][col]
            self.white_positions.remove((row, col))
            self.white_defences = self.__calculate_defence(7)
        elif self.pieces[row][col] == CellState.BLACK_QUEEN:
            self.number_black_queens -= 1
            self.black_positions.remove((row, col))
            self.black_centar_rate -= self.center_matrix[row][col]
            self.white_defences = self.__calculate_defence(0)
        self.pieces[row][col] = CellState.EMPTY

    def __promote_piece(self, row, col):

        if self.pieces[row][col] == CellState.WHITE:
            self.pieces[row][col] = CellState.WHITE_QUEEN
            self.number_white_queens += 1
            self.number_white_pieces -= 1
        elif self.pieces[row][col] == CellState.BLACK:
            self.pieces[row][col] = CellState.BLACK_QUEEN
            self.number_black_queens += 1
            self.number_black_pieces -= 1
        
    def __move_piece(self, from_cell, to_cell):
        from_row, from_col = from_cell
        to_row, to_col = to_cell
        if self.pieces[from_row][from_col] in [CellState.WHITE, CellState.WHITE_QUEEN]:
            if to_row == 0:
                self.__promote_piece(from_row, from_col)
            self.white_positions.remove((from_row, from_col))
            self.white_positions.add((to_row, to_col))
            self.white_centar_rate -= self.center_matrix[from_row][from_col]
            self.white_centar_rate += self.center_matrix[to_row][to_col]
            self.white_defences = self.__calculate_defence(7)
        elif self.pieces[from_row][from_col] in [CellState.BLACK, CellState.BLACK_QUEEN]:
            if to_row == 7:
                self.__promote_piece(from_row, from_col)
            self.black_positions.remove((from_row, from_col))
            self.black_positions.add((to_row, to_col))
            self.black_centar_rate -= self.center_matrix[from_row][from_col]
            self.black_centar_rate += self.center_matrix[to_row][to_col]
            self.white_defences = self.__calculate_defence(0)
        self.pieces[to_row][to_col] = self.pieces[from_row][from_col]
        self.pieces[from_row][from_col] = CellState.EMPTY

    def __jump_path(self, from_cell, path):
        for jump in path:
            self.__jump_piece(from_cell, jump)
            from_cell = jump

    def __jump_piece(self, from_cell, to_cell):
        from_row, from_col = from_cell
        to_row, to_col = to_cell
        middle_row = (from_row + to_row) // 2
        middle_col = (from_col + to_col) // 2
        if to_col != from_col:
            self.__delete_piece(middle_row, middle_col)
        elif from_col == 1:
            self.__delete_piece(middle_row, 0)
        elif from_col == Constants.CELL_COUNT - 2:
            self.__delete_piece(middle_row, Constants.CELL_COUNT - 1)
        self.__move_piece(from_cell, to_cell)

    def __calculate_defence(self, row):
        if row == 7:
            map(lambda x: x[1] == 0, self.white_positions)
            arr = filter(lambda x: x[0] in [CellState.BLACK, CellState.BLACK_QUEEN], [
                    (self.pieces[0][0], 1),
                    (self.pieces[0][2], 3),
                    (self.pieces[0][4], 3), 
                    (self.pieces[0][6], 2)
                ])
        else:
            arr = filter(lambda x: x[0] in [CellState.WHITE, CellState.WHITE_QUEEN], [
                    (self.pieces[7][1], 1),
                    (self.pieces[7][3], 2),
                    (self.pieces[7][5], 2), 
                    (self.pieces[7][7], 2)
                ])
        return sum(map(lambda x: x[1], arr))
    def is_game_over(self):
        if (self.number_black_pieces + self.number_black_queens) == 0:
            self.winner = Player.WHITE
            return True
        if (self.number_white_pieces + self.number_white_queens) == 0:
            self.winner = Player.BLACK
            return True
        if len(self.current_player_moves) == 0:
            if self.player.is_white():
                self.winner = Player.BLACK
            else:
                self.winner = Player.WHITE
            return True
        return False
        
    def calculacte_moves(self):
        if self.player.is_white():
            positions = self.white_positions
        else:
            positions = self.black_positions
        self.current_player_moves.clear()
        for position in positions:
            row, col = position
            moves = calucate_moves(self, row, col)
            jumps = calcuate_jumps(self, row, col)
            print(f"Moves: {moves}, jumps: {jumps} for {position}")
            moves_for_position = set()
            for move in moves:
                moves_for_position.add((move[0], move[1], None))
            for jump_cell, path in jumps.items():
                moves_for_position.add((jump_cell[0], jump_cell[1], tuple(path)))
            if len(moves_for_position) > 0:
                print(f"Calulated moves: {moves_for_position} for position: {position}")
                self.current_player_moves[position] = moves_for_position