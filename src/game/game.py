"""
12/18/2024 - The Beginning

Goal: Get a text version of the game to be able to played by one terminal

Contains game logic and related classes


12/20/2024
 - Left off on correctly adding isValidSet(played_hand) to validate if played hand is a set
    - Sorts cards in played hand to ensure at least one card is not a wildcard 
 - Need to move to Validate a run then decided how to test playing cards in a hand

Future Considerations for game rules:
 - Minimum/Maximum players changing the cards dealt and deck count


"""

from enum import Enum
from game_errors import EmptyDecksError, InvalidChangeError

import random


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
        self.value = self._assignValue()

    def _assignValue(self):
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


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.hand = []

    def addCard(self, card: Card) -> list:
        return self.hand.append(card)

    def __repr__(self):
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}]"

    def __str__(self):
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}]"

    def __lt__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            raise NotImplemented
        return self.score < other.score

    def __gt__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            raise NotImplemented
        return self.score > other.score

    def __eq__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            raise NotImplemented
        return self.score == other.score


class Game:
    def __init__(self):
        self.players = [Player("A"), Player("B"), Player("C")]
        self.deck = self._generateDeck()
        self.discard = []
        self.winner = False
        self.currentPlayer = self.players[0]
        self.round = 0
        pass

    # Game Essentials

    def game_loop(self):
        """Main loop that will run the game until final round is played"""
        while self.winner == False:
            pass

    def drawCard(self) -> Card:
        """Draws a card from the deck or refills it if empty."""
        if len(self.deck) == 0:
            if len(self.discard) == 0:
                raise EmptyDecksError(
                    "Both the deck and discard pile are empty somehow."
                )

            self.deck = self.discard
            self.shuffleDeck()
        return self.deck.pop()

    def shuffleDeck(self) -> list:
        """Shuffles self.deck and updates in place.

        It modifies the deck directly and can be called without storing the result.

        Returns:
            list: the shuffled deck
        """
        return random.shuffle(self.deck)

    def dealCards(self) -> None:
        """Adds 11 Cards to every players hand. The deck continues to be shuffled until the top card that is
        added to the discard pile is not a wild card.
        """
        for _ in range(11):
            for player in self.players:
                player.addCard(self.drawCard())
        self.discard = self.deck[-1:]
        while self.discard[0].value == 20:
            self.shuffleDeck()
            self.discard = self.deck[-1:]
        return None

    def determineWinner(self) -> list:
        winner = [self.players[0]]
        for player in self.players[1:]:
            if player == winner[0] and player is not winner[0]:
                winner.append(player)
            if player < winner[0]:
                winner = [player]
        return winner

    def isValidSet(self, played_hand: list) -> bool:
        """Determines if the selected cards are a valid set.

        Args:
            played_hand (list): Selected cards to play as a set.

        Returns:
            bool: True if valid set or False if invalid set.
        """
        if len(played_hand) != 3:
            return False

        # Sort played hands based on the value
        played_hand.sort()

        if played_hand[0].value == 20:
            return False

        if (
            played_hand[0].name != played_hand[1].name and played_hand[1].value != 20
        ) or (
            played_hand[0].name != played_hand[2].name and played_hand[2].value != 20
        ):
            return False

        return True

    def isValidRun(self, played_hand: list) -> bool:
        """Determines if the selected cards are a valid run.

        Args:
            played_hand (list): Selected cards to play as a run

        Returns:
            bool: True if valid run or False if invalid run.
        """

        # if hand is not exactly 4 cards, if round 7 can be more than 4 cards but not less
        if (self.round == 7 and (len(played_hand) < 4)) or (
            self.round != 7 and len(played_hand) != 4
        ):
            return False

        # Sort played hands based on the value
        played_hand.sort()

        # if all cards are wild cards
        # if multiple suits are played in same hand
        # Take suit of first non wild
        suit = Suit.WILD
        for card in played_hand:
            if card.suit != Suit.WILD and card.value != 20:
                suit = card.suit
        if suit == Suit.WILD:
            return False

        base_card = played_hand[0]

        for card in played_hand[1:3]:
            if card.suit != suit and card.value != 20:
                return False

        # if same suits but cards not in sequence
        for card in played_hand[1:3]:
            if (type(base_card) == Wild and type(card) == Wild) and (
                played_hand[card.chosen_name.value - base_card.chosen_name.value]
                != card
            ):
                return False
            if (type(base_card) == Wild and type(card) != Wild) and (
                played_hand[card.name.value - base_card.chosen_name.value] != card
            ):
                return False
            if (type(base_card) != Wild and type(card) == Wild) and (
                played_hand[card.chosen_name.value - base_card.name.value] != card
            ):
                return False
            if (type(base_card) != Wild and type(card) != Wild) and (
                played_hand[card.name.value - base_card.name.value] != card
            ):
                return False

        return True

    # Display Functions #

    def displayDeck(self) -> None:
        """displays cards left in the deck"""
        for card in self.deck:
            print(str(card))
        return None

    def displayPlayers(self) -> None:
        """Displays players"""
        for player in self.players:
            print(player)
        return None

    def displayDiscard(self) -> None:
        """Displays the current card in the discard pile"""
        print(str(self.discard))
        return None

    # Game Setup #

    def _generateDeck(self) -> list:
        deck = []
        for suit in list(Suit)[:4]:
            for name in list(Name)[2:]:
                if name == Name.TWO:
                    deck.append(Wild(name, suit))
                else:
                    deck.append(Card(name, suit))
        deck.extend([Wild(Name.JOKER, Suit.WILD) for _ in range(2)])

        return deck * 2

    def _generatePlayers(self, num: int) -> list:
        players = []
        for _ in range(num):
            players.append(Player())
        return players

    # Magic Methods #

    def __repr__(self):
        return f"{self.players} {self.deck} {self.winner}"


class Wild(Card):
    def __init__(self, name, suit):
        super().__init__(name, suit)
        self.chosen_name = Name.INVALID
        self.chosen_suit = Suit.WILD

    def change_value(self, chosen: str) -> Name:
        """Changes temporary name to card of users choice.

        Args:
            chosen (str): Name of card user wants to use wild in place of.
        """
        if chosen == "TWO" or chosen == "JOKER":
            raise InvalidChangeError

        for name in Name:
            if chosen == name.name:
                self.chosen_name = Name(name)
                return self.chosen_name
        raise InvalidChangeError

    def change_suit(self, chosen: str) -> Suit:
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
        return (
            super().__repr__()
            + " - Temp value ->  "
            + self.chosen_name.name
            + " of "
            + self.chosen_suit.name
        )

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
        return self.chosen_name.value < other.name.value

    def __gt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.chosen_name.value > other.name.value


z = Game()
