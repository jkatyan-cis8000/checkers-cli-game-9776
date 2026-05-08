#!/usr/bin/env python3
"""CLI entry point for Checkers game."""

import sys
from game import Game


def main():
    """Main game loop."""
    game = Game()
    print("Welcome to Checkers!")
    print("Enter moves in format: e6-d5 (column-row to column-row)")
    print("Type 'quit' to exit\n")
    
    while not game.game_over:
        game.display()
        print(f"\nValid moves: {game.get_valid_moves_str()}")
        
        try:
            move = input(f"{game.current_player}'s move: ").strip().lower()
            
            if move == 'quit':
                print("Game ended by player")
                break
            
            if move == 'help':
                print("\nMove notation examples:")
                print("  e6-d5  - move from e6 to d5")
                print("  c8-e6  - move from c8 to e6")
                print("  e2-c4  - capture from e2 to c4 (jumping over d3)")
                print("  quit   - exit the game")
                print("  help   - show this help\n")
                continue
            
            success, message = game.execute_move(move)
            print(message)
            
            if success and game.game_over:
                game.display()
                print(f"\nGame over! Winner: {game.winner}")
                break
            
            if not success:
                print("Invalid move. Try again.\n")
        
        except KeyboardInterrupt:
            print("\nGame interrupted")
            break
        except EOFError:
            print("\nEOF - exiting")
            break
    
    print("Thanks for playing!")


if __name__ == '__main__':
    main()
