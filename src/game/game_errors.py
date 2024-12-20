"""
game_errors.py

12/20/2024

Contains custom errors

"""


class EmptyDecksError(Exception):
    """Raised when both the deck and the discard pile are empty. Should not occur due to the rules of the game but oh well!"""
