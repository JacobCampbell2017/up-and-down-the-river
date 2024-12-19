"""
12/18/2024

Contains game logic and related classes

Future Considerations for game rules:
 - Minimum/Maximum players changing the cards dealt and deck count


"""

from enum import Enum


class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3
    JOKER = 4


class Name(Enum):
    JOKER = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Game:
    def __init__(self):
        # List of Players (Turn Order)
        # Deck
        self.winner = False
        pass

    def game_loop(self):
        while self.winner == False:
            pass


class Player:
    # Hand
    # Score
    pass


class Hand:
    # of cards
    # list of cards
    pass


class Card:
    def __init__(self, name: Name, suit: Suit):
        self.name = name
        self.suit = suit
        self.value = self._assignValue()

    def _assignValue(self):
        """Assigns point value to card based on the values given to constructor."""
        if self.name.value >= 3 and self.name.value <= 9:
            self.value = 5
        elif self.name.value >= 10 and self.name.value <= 13:
            self.value = 10
        elif self.name.value == 14:
            self.value = 15
        else:
            self.value = 20

    def __repr__(self):
        if self.name.name == "JOKER":
            return "Value: Joker"
        else:
            return f"Value: {self.name.name}, Suit: {self.suit.name}"

    def __str__(self):
        if self.name.name == "JOKER":
            return "JOKER"
        else:
            return f"{self.name.name} of {self.suit.name}"
