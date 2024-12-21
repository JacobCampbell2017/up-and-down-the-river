"""
12/18/2024 - The Beginning

Goal: Get a text version of the game to be able to played by one terminal

Contains game logic and related classes

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


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.hand = []

    def add_card(self, card: Card) -> None:
        return self.hand.append(card)

    def __repr__(self):
        hand_str = ", ".join(str(card) for card in self.hand[:5]) + (
            "..." if len(self.hand) > 5 else ""
        )
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}]"

    def __str__(self):
        hand_str = ", ".join(str(card) for card in self.hand)
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}]"

    def __lt__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            return NotImplemented
        return self.score < other.score

    def __gt__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            return NotImplemented
        return self.score > other.score

    def __eq__(self, other):
        """Determines how players are compared to each other by their score"""
        if not isinstance(other, Player):
            return NotImplemented
        return self.score == other.score


class Game:
    def __init__(self, num_players=3):
        self.players = [Player("A"), Player("B"), Player("C")]
        self.deck = self._generate_deck()
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

    def draw_card(self) -> Card:
        """Draws a card from the deck or refills it if empty."""
        if len(self.deck) == 0:
            if len(self.discard) == 0:
                raise EmptyDecksError(
                    "Both the deck and discard pile are empty somehow."
                )

            self.deck = self.discard
            self.shuffle_deck()
        return self.deck.pop()

    def shuffle_deck(self) -> None:
        """Shuffles self.deck and updates in place.

        It modifies the deck directly and can be called without storing the result.

        Returns:
            list: the shuffled deck
        """
        return random.shuffle(self.deck)

    def deal_cards(self, num_of_cards=11) -> None:
        """Adds a specified Cards to every players hand. The deck continues to be shuffled until the top card that is
        added to the discard pile is not a wild card.
        """
        for _ in range(11):
            for player in self.players:
                player.add_card(self.draw_card())
        self.discard = self.deck[-1:]
        while self.is_wild(self.discard[0]):
            self.shuffle_deck()
            self.discard = self.deck[-1:]
        return None

    def determine_winner(self) -> list:
        winner = [self.players[0]]
        for player in self.players[1:]:
            if player == winner[0] and player is not winner[0]:
                winner.append(player)
            if player < winner[0]:
                winner = [player]
        return winner

    def is_valid_set(self, played_hand: list) -> bool:
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

        if self.is_wild(played_hand[0]):
            return False

        if (
            played_hand[0].name != played_hand[1].name
            and not self.is_wild(played_hand[1])
        ) or (
            played_hand[0].name != played_hand[2].name
            and not self.is_wild(played_hand[2])
        ):
            return False

        return True

    def is_valid_run(self, played_hand: list) -> bool:
        """Determines if the selected cards are a valid run.

        Args:
            played_hand (list): Selected cards to play as a run

        Returns:
            bool: True if valid run or False if invalid run.
        """

        # if hand is not exactly 4 cards, if round 7 can be more than 4 cards but not less
        if (self.round == 7 and len(played_hand) < 4) or (
            self.round != 7 and len(played_hand) != 4
        ):
            return False

        played_hand.sort()

        # if all cards are wild cards
        # if multiple suits are played in same hand
        # Take suit of first non wild
        suit = Suit.WILD
        for card in played_hand:
            if not self.is_wild(card):
                suit = card.suit
        if suit == Suit.WILD:
            return False

        base_card = played_hand[0]

        for card in played_hand[1:3]:
            if card.suit != suit and not self.is_wild(card):
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

    def is_wild(self, card: Card) -> bool:
        return card.suit == Suit.WILD or card.value == 20

    # Display Functions #

    def display_deck(self) -> None:
        """displays cards left in the deck"""
        for card in self.deck:
            print(str(card))
        return None

    def display_players(self) -> None:
        """Displays players"""
        for player in self.players:
            print(player)
        return None

    def display_discard(self) -> None:
        """Displays the current card in the discard pile"""
        print(str(self.discard))
        return None

    # Game Setup #

    def _generate_deck(self) -> list:
        deck = []
        for suit in list(Suit)[:4]:
            for name in list(Name)[2:]:
                if name == Name.TWO:
                    deck.append(Wild(name, suit))
                else:
                    deck.append(Card(name, suit))
        deck.extend([Wild(Name.JOKER, Suit.WILD) for _ in range(2)])

        return deck * 2

    def _generate_players(self, num: int) -> list:
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
        if isinstance(other, Card) and self.chosen_name == Name.INVALID:
            return self.value < other.name.value
        return self.chosen_name.value < other.name.value

    def __gt__(self, other):
        """Defines the way wildcards are compared to others"""
        if not isinstance(other, Card):
            return NotImplemented
        if isinstance(other, Card) and self.chosen_name == Name.INVALID:
            return self.value > other.name.value
        return self.chosen_name.value > other.name.value


z = Game()
z.shuffle_deck()
z.deal_cards()
z.display_discard()
