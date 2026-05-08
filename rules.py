from board import Board
from pieces import Piece


def parse_move(move_str):
    """Parse move notation like 'e6-d5' into coordinates."""
    try:
        from_pos, to_pos = move_str.split('-')
        from_col = ord(from_pos[0].lower()) - ord('a')
        from_row = int(from_pos[1]) - 1
        to_col = ord(to_pos[0].lower()) - ord('a')
        to_row = int(to_pos[1]) - 1
        return (from_row, from_col, to_row, to_col)
    except (ValueError, IndexError):
        return None


def is_valid_move(board, from_row, from_col, to_row, to_col, player):
    """Check if a move is valid for the given player."""
    piece = board.get_position(from_row, from_col)
    if piece is None or piece.player != player:
        return False
    
    if not board.is_valid_position(to_row, to_col):
        return False
    
    if board.get_position(to_row, to_col) is not None:
        return False
    
    if not board.is_dark_square(to_row, to_col):
        return False
    
    dr = to_row - from_row
    dc = to_col - from_col
    
    directions = piece.get_valid_directions()
    valid_step = (dr, dc) in directions
    
    if not valid_step:
        return False
    
    if abs(dr) == 1 and abs(dc) == 1:
        return True
    
    if abs(dr) == 2 and abs(dc) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        mid_piece = board.get_position(mid_row, mid_col)
        return mid_piece is not None and mid_piece.player != player
    
    return False


def get_capture_positions(board, from_row, from_col, to_row, to_col):
    """Get positions of captured pieces during a move."""
    captures = []
    if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        mid_piece = board.get_position(mid_row, mid_col)
        if mid_piece is not None and mid_piece.player != board.get_position(from_row, from_col).player:
            captures.append((mid_row, mid_col))
    return captures


def apply_move(board, from_row, from_col, to_row, to_col):
    """Apply a move to the board and return captured positions."""
    piece = board.get_position(from_row, from_col)
    board.clear_position(from_row, from_col)
    board.set_position(to_row, to_col, piece)
    
    captures = []
    if abs(to_row - from_row) == 2 and abs(to_col - from_col) == 2:
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        mid_piece = board.get_position(mid_row, mid_col)
        if mid_piece is not None:
            board.clear_position(mid_row, mid_col)
            captures.append((mid_row, mid_col))
    
    return captures


def check_kinging(board, row, col):
    """Check if piece at position should be promoted to king."""
    piece = board.get_position(row, col)
    if piece is None or piece.is_king:
        return False
    if piece.player == 'red' and row == 0:
        piece.promote_to_king()
        return True
    if piece.player == 'white' and row == 7:
        piece.promote_to_king()
        return True
    return False


def get_all_moves(board, player):
    """Get all valid moves for a player."""
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board.get_position(row, col)
            if piece is not None and piece.player == player:
                for dr, dc in piece.get_valid_directions():
                    to_row, to_col = row + dr, col + dc
                    if is_valid_move(board, row, col, to_row, to_col, player):
                        moves.append(((row, col), (to_row, to_col)))
    return moves


def has_valid_moves(board, player):
    """Check if player has any valid moves."""
    return len(get_all_moves(board, player)) > 0


def check_win(board):
    """Check if game has been won. Returns winning player or None."""
    red_count = 0
    white_count = 0
    for row in range(8):
        for col in range(8):
            piece = board.get_position(row, col)
            if piece is not None:
                if piece.player == 'red':
                    red_count += 1
                else:
                    white_count += 1
    
    if red_count == 0:
        return 'white'
    if white_count == 0:
        return 'red'
    return None
