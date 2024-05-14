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
            game.state.move_piece(game.state.selected, (row, col))
            clear_hints(game.state)
            return
        if game.state.pieces[row][col] == CellState.JUMP:
            game.state.jump_path(game.state.selected, game.state.possible_jumps[(row, col)])
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
            game.state.move_piece(game.state.selected, (row, col))
            clear_hints(game.state)
            return
        if game.state.pieces[row][col] == CellState.JUMP:
            game.state.jump_path(game.state.selected, game.state.possible_jumps[(row, col)])
            clear_hints(game.state)
            return
    game.state.selected = (row, col)
    game.state.possible_moves = calucate_moves(game.state, row, col)
    game.state.possible_jumps = calcuate_jumps(game.state, row, col)
    draw_hints(game.state)