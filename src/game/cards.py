"""
cards.py

Contains classes for Card and Wild

"""

from enum import Enum
from game_errors import InvalidChangeError


class Suit_Emoji(Enum):
    HEARTS = "\N{black heart suit}"
    DIAMONDS = "\N{black diamond suit}"
    SPADES = "\N{black spade suit}"
    CLUBS = "\N{black club suit}"
    WILD = "\N{playing card black joker}"


class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3
    WILD = 4


class Name(Enum):
    INVALID = 0
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


class Name_Print(Enum):
    INVALID = "Uh Oh"
    JOKER = "JOKER"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class Card:
    def __init__(self, name: Name, suit: Suit, id: int = -1):
        self.name = name
        self.suit = suit
        self.value = self._assign_value()
        self.id = id
        self.number = name.value

    def is_wild(self) -> bool:
        return self.suit == Suit.WILD or self.name == Name.TWO

    def _assign_value(self) -> int:
        """Assigns point value to card based on the values given to constructor."""
        if self.name.value >= 3 and self.name.value <= 9:
            return 5
        elif self.name.value >= 10 and self.name.value <= 13:
            return 10
        elif self.name.value == 14:
            return 15
        else:
            return 20

    def __repr__(self):
        if self.name.name == "JOKER":
            return f"|{Suit_Emoji.WILD.value}|"
        else:
            return f"|{Name_Print[self.name.name].value}{Suit_Emoji[self.suit.name].value}|"

    def __str__(self):
        if self.name.name == "JOKER":
            return f"{Suit_Emoji.WILD.value}"
        else:
            return f"|{Name_Print[self.name.name].value}{Suit_Emoji[self.suit.name].value}|"

    def __lt__(self, other):
        """Defines how cards are compared for sorting"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.number < other.number

    def __gt__(self, other):
        """Defines how cards are compared for sorting"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.number >= other.number


class Wild(Card):
    def __init__(self, name, suit, id=-1):
        super().__init__(name, suit, id)
        self.chosen_name = Name.INVALID
        self.chosen_suit = Suit.WILD
        self.number = 20

    def is_not_set(self) -> bool:
        return self.chosen_name == Name.INVALID

    def set_value(self, chosen: str) -> Name:
        """Changes the wildcard's temporary value to a valid card name.

        Args:
        chosen (str): The name of the card to substitute the wildcard for.

        Raises:
            InvalidChangeError: If the chosen name is invalid (JOKER or TWO).

        Returns:
            Name: The updated name assigned to the wildcard.
        """
        if chosen == "TWO" or chosen == "JOKER":
            raise InvalidChangeError

        for name in Name:
            if chosen == name.name:
                self.chosen_name = Name(name)
                self.number = self.chosen_name.value
                return self.chosen_name
        raise InvalidChangeError

    def set_suit(self, chosen: str) -> Suit:
        """Changes temporary suit to suit of users choice.

        Args:
            chosen (str): Name of card user wants to use wild in place of.
        """
        if chosen == "WILD":
            raise InvalidChangeError

        for suit in Suit:
            if chosen == suit.name:
                self.chosen_suit = Suit(suit)

        return self.chosen_suit

    def __repr__(self):
        chosen_value = (
            f"{self.chosen_name.name} of {self.chosen_suit.name}"
            if self.chosen_name != Name.INVALID
            else "Not Set"
        )
        return super().__repr__()

    def __str__(self):
        return self.chosen_name.name + " of " + self.chosen_suit.name + " [WILD]"

    def __lt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented

        return self.number < other.number

    def __gt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.number > other.number
