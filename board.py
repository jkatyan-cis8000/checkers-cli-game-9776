class Board:
    """8x8 Checkers board representation."""
    
    def __init__(self):
        """Initialize an empty 8x8 board."""
        self._board = [[None for _ in range(8)] for _ in range(8)]
    
    def get_position(self, row, col):
        """Get piece at position (row, col)."""
        return self._board[row][col]
    
    def set_position(self, row, col, piece):
        """Set piece at position (row, col)."""
        self._board[row][col] = piece
    
    def clear_position(self, row, col):
        """Clear piece at position (row, col)."""
        self._board[row][col] = None
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_dark_square(self, row, col):
        """Check if the square is a dark playing square."""
        return (row + col) % 2 == 1
    
    def display(self):
        """Display the board with row numbers and column letters."""
        print("  a b c d e f g h")
        for row in range(7, -1, -1):
            row_str = f"{row + 1} "
            for col in range(8):
                piece = self._board[row][col]
                if piece is None:
                    if self.is_dark_square(row, col):
                        row_str += ". "
                    else:
                        row_str += "  "
                else:
                    row_str += str(piece) + " "
            print(row_str)
        print()
    
    def place_initial_pieces(self):
        """Place pieces in initial Checkers positions."""
        for row in range(8):
            for col in range(8):
                if self.is_dark_square(row, col):
                    if row < 3:
                        from pieces import Piece
                        self.set_position(row, col, Piece('white'))
                    elif row > 4:
                        from pieces import Piece
                        self.set_position(row, col, Piece('red'))
    
    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board()
        for row in range(8):
            for col in range(8):
                new_board.set_position(row, col, self._board[row][col])
        return new_board
