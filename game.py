from board import Board
from pieces import Piece
from rules import (
    parse_move, is_valid_move, apply_move, 
    check_kinging, get_all_moves, has_valid_moves, check_win
)


class Game:
    """Checkers game with turn alternation and state management."""
    
    def __init__(self):
        """Initialize a new Checkers game."""
        self.board = Board()
        self.board.place_initial_pieces()
        self.current_player = 'red'
        self.game_over = False
        self.winner = None
        self.must_capture = False
        self.capture_from = None
        self.move_history = []
    
    def switch_turn(self):
        """Switch to the other player's turn."""
        self.current_player = 'white' if self.current_player == 'red' else 'red'
    
    def get_valid_moves_for_player(self, player=None):
        """Get all valid moves for current or specified player."""
        if player is None:
            player = self.current_player
        
        if self.must_capture and self.capture_from is not None:
            return self._get_captures_from_position(player, self.capture_from)
        
        all_moves = get_all_moves(self.board, player)
        
        capture_moves = []
        non_capture_moves = []
        for from_pos, to_pos in all_moves:
            if abs(to_pos[0] - from_pos[0]) == 2:
                capture_moves.append((from_pos, to_pos))
            else:
                non_capture_moves.append((from_pos, to_pos))
        
        if capture_moves:
            return capture_moves
        return non_capture_moves
    
    def _get_captures_from_position(self, player, position):
        """Get all capture moves from a specific position."""
        row, col = position
        piece = self.board.get_position(row, col)
        if piece is None or piece.player != player:
            return []
        
        moves = []
        for dr, dc in piece.get_valid_directions():
            to_row = row + 2 * dr
            to_col = col + 2 * dc
            if is_valid_move(self.board, row, col, to_row, to_col, player):
                moves.append(((row, col), (to_row, to_col)))
        return moves
    
    def execute_move(self, move_str):
        """Execute a move from notation string. Returns success status and message."""
        if self.game_over:
            return False, "Game is already over"
        
        coords = parse_move(move_str)
        if coords is None:
            return False, "Invalid move format. Use 'e6-d5' format"
        
        from_row, from_col, to_row, to_col = coords
        
        if self.must_capture and self.capture_from is not None:
            if (from_row, from_col) != self.capture_from:
                return False, f"Must continue capturing from {chr(ord('a') + self.capture_from[1])}{self.capture_from[0] + 1}"
            
            if not is_valid_move(self.board, from_row, from_col, to_row, to_col, self.current_player):
                return False, "Invalid capture move"
            
            apply_move(self.board, from_row, from_col, to_row, to_col)
            captures = [(to_row - from_row, to_col - from_col)]
            
            new_pos = (to_row, to_col)
            if check_kinging(self.board, to_row, to_col):
                self.must_capture = False
                self.capture_from = None
                self.switch_turn()
                return True, f"Piece promoted to king! Turn passed to {self.current_player}"
            
            if self._has_additional_captures(to_row, to_col):
                self.capture_from = new_pos
                return True, f"Capture! Continue from {chr(ord('a') + new_pos[1])}{new_pos[0] + 1}"
            
            self.must_capture = False
            self.capture_from = None
            self.switch_turn()
            return True, f"Move executed. {self.current_player}'s turn"
        
        if not is_valid_move(self.board, from_row, from_col, to_row, to_col, self.current_player):
            return False, "Invalid move"
        
        captures = apply_move(self.board, from_row, from_col, to_row, to_col)
        check_kinging(self.board, to_row, to_col)
        
        if captures:
            if abs(to_row - from_row) == 2 and self._has_additional_captures(to_row, to_col):
                self.must_capture = True
                self.capture_from = (to_row, to_col)
                return True, f"Capture! Continue from {chr(ord('a') + to_col)}{to_row + 1}"
            else:
                self.switch_turn()
                return True, f"Move executed. {self.current_player}'s turn"
        else:
            self.switch_turn()
            return True, f"Move executed. {self.current_player}'s turn"
    
    def _has_additional_captures(self, row, col):
        """Check if additional captures are available from a position."""
        return len(self._get_captures_from_position(self.current_player, (row, col))) > 0
    
    def check_game_state(self):
        """Check if game has ended."""
        winner = check_win(self.board)
        if winner:
            self.game_over = True
            self.winner = winner
            return True
        
        if not has_valid_moves(self.board, self.current_player):
            self.game_over = True
            self.winner = 'white' if self.current_player == 'red' else 'red'
            return True
        
        return False
    
    def display(self):
        """Display the current game state."""
        self.board.display()
        print(f"Current turn: {self.current_player}")
        if self.must_capture:
            print(f"Must continue capturing from {chr(ord('a') + self.capture_from[1])}{self.capture_from[0] + 1}")
        if self.game_over:
            print(f"Game over! Winner: {self.winner}")
    
    def get_valid_moves_str(self):
        """Get string representation of valid moves."""
        moves = self.get_valid_moves_for_player()
        if not moves:
            return "No valid moves available"
        return ", ".join(
            f"{chr(ord('a') + fr[1])}{fr[0] + 1}-{chr(ord('a') + to[1])}{to[0] + 1}"
            for fr, to in moves
        )
