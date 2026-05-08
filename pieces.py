class Piece:
    """Checkers piece representation."""
    
    def __init__(self, player, is_king=False):
        """Initialize a piece with player color and king status."""
        self.player = player
        self.is_king = is_king
    
    def get_valid_directions(self):
        """Get valid move directions based on player and king status."""
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif self.player == 'red':
            return [(-1, -1), (-1, 1)]
        else:
            return [(1, -1), (1, 1)]
    
    def promote_to_king(self):
        """Promote piece to king."""
        self.is_king = True
    
    def __str__(self):
        """String representation for board display."""
        if self.player == 'red':
            return 'r' if not self.is_king else 'R'
        else:
            return 'w' if not self.is_king else 'W'
