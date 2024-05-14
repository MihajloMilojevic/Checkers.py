from src.hints import draw_hints
from src.cell_state import CellState
from src.hints import clear_hints, draw_hints, calcuate_jumps, calucate_moves
from src.constans import Constants


def white_click_handler(game, row: int, col: int):
    # if black piece is clicked no need to do anything
    if game.state.pieces[row][col] in [CellState.BLACK, CellState.BLACK_QUEEN]:
        return
    # make a move
    if game.state.selected is not None:
        if game.state.pieces[row][col] == CellState.MOVE:
            if row == 0:
                game.state.pieces[game.state.selected[0]][game.state.selected[1]] = CellState.WHITE_QUEEN
            make_move(game, row, col) 
            game.state.player.change_player()
            clear_hints(game.state)
            return
        if game.state.pieces[row][col] == CellState.JUMP:
            from_row, from_col = game.state.selected
            for jump in game.state.possible_jumps[(row, col)]:
                make_jump(game, from_row, from_col, jump[0], jump[1])
                from_row, from_col = jump
            game.state.player.change_player()
            clear_hints(game.state)
            return
    game.state.selected = (row, col)
    game.state.possible_moves = calucate_moves(game.state, row, col)
    game.state.possible_jumps = calcuate_jumps(game.state, row, col)
    draw_hints(game.state)

def black_click_handler(game, row: int, col: int):
    # if black piece is clicked no need to do anything
    if game.state.pieces[row][col] in [CellState.WHITE, CellState.WHITE_QUEEN]:
        return
    # make a move
    if game.state.selected is not None:
        if game.state.pieces[row][col] == CellState.MOVE:
            if row == Constants.CELL_COUNT - 1:
                game.state.pieces[game.state.selected[0]][game.state.selected[1]] = CellState.BLACK_QUEEN
            make_move(game, row, col)
            game.state.player.change_player()
            clear_hints(game.state)
            return
        if game.state.pieces[row][col] == CellState.JUMP:
            from_row, from_col = game.state.selected
            for jump in game.state.possible_jumps[(row, col)]:
                make_jump(game, from_row, from_col, jump[0], jump[1])
                from_row, from_col = jump
                game.state.player.change_player()
                clear_hints(game.state)
            return
    game.state.selected = (row, col)
    game.state.possible_moves = calucate_moves(game.state, row, col)
    game.state.possible_jumps = calcuate_jumps(game.state, row, col)
    draw_hints(game.state)

def make_move(game, row, col):
    game.state.pieces[row][col] = game.state.pieces[game.state.selected[0]][game.state.selected[1]]
    game.state.pieces[game.state.selected[0]][game.state.selected[1]] = CellState.EMPTY
    game.state.selected = None

def make_jump(game, from_row, from_col, to_row, to_col):
    middle_row = (from_row + to_row) // 2
    middle_col = (from_col + to_col) // 2
    game.state.pieces[to_row][to_col] = game.state.pieces[from_row][from_col]
    game.state.pieces[from_row][from_col] = CellState.EMPTY
    if to_col != from_col:
        game.state.pieces[middle_row][middle_col] = CellState.EMPTY
        return
    if from_col == 1:
        game.state.pieces[middle_row][0] = CellState.EMPTY
    elif from_col == Constants.CELL_COUNT - 2:
        game.state.pieces[middle_row][Constants.CELL_COUNT - 1] = CellState.EMPTY