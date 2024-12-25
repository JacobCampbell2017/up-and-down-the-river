"""
cards.py

Contains classes for Card and Wild

"""

from enum import Enum
from game_errors import InvalidChangeError


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


class Card:
    def __init__(self, name: Name, suit: Suit):
        self.name = name
        self.suit = suit
        self.value = self._assign_value()

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
            return "JOKER"
        else:
            return f"{self.name.name} of {self.suit.name}"

    def __str__(self):
        if self.name.name == "JOKER":
            return "JOKER"
        else:
            return f"{self.name.name} of {self.suit.name}"

    def __lt__(self, other):
        """Defines how cards are compared for sorting"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.name.value < other.name.value

    def __gt__(self, other):
        """Defines how cards are compared for sorting"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.name.value >= other.name.value


class Wild(Card):
    def __init__(self, name, suit):
        super().__init__(name, suit)
        self.chosen_name = Name.INVALID
        self.chosen_suit = Suit.WILD

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
        return super().__repr__() + f" - Temp value -> {chosen_value}"

    def __str__(self):
        return (
            super().__str__()
            + " - Temp value ->  "
            + self.chosen_name.name
            + " of "
            + self.chosen_suit.name
        )

    def __lt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented
        if isinstance(other, Wild) and other.chosen_name != Name.INVALID:
            if isinstance(self, Wild) and self.chosen_name != Name.INVALID:
                return self.chosen_name.value < other.chosen_name.value
        if isinstance(other, Card) and self.chosen_name == Name.INVALID:
            return self.value < other.name.value

        return self.chosen_name.value < other.name.value

    def __gt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented
        if isinstance(other, Wild) and other.chosen_name != Name.INVALID:
            if isinstance(self, Wild) and self.chosen_name != Name.INVALID:
                return self.chosen_name.value > other.chosen_name.value
        if isinstance(other, Card) and self.chosen_name == Name.INVALID:
            return self.value > other.name.value
        return self.chosen_name.value > other.name.value
