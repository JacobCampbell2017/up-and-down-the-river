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
        self.players = list()
        self.winner = None
        self.round = 0
        # add deck which is a list of card objects


class Card:
    def __init__(self, name: Name, suit: Suit):
        self.name = name
        self.suit = suit

    def _assignValue(self):
        if self.name.value >= 3 and self.name.value <= 9:
            self.value = 5
        elif self.name.value >= 10 and self.name.value <= 13:
            self.value = 10
        elif self.name.value == 14:
            self.value = 15
        else:
            self.value = 20

    def __repr__(self) -> str:
        if self.name.name == "JOKER":
            return "Joker"
        else:
            return f"{self.name.name} of {self.suit.name}"
