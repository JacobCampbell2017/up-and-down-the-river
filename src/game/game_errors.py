"""
game_errors.py

12/20/2024

Contains custom errors

"""


class EmptyDecksError(Exception):
    """Raised when both the deck and the discard pile are empty. Should not occur due to the rules of the game but oh well!"""


class InvalidChangeError(Exception):
    """Raised when trying to change the value of a wild card to an invalid value. (Another Wild)"""
