"""
12/18/2024 - The Beginning

Goal: Get a text version of the game to be able to played by one terminal

Contains game logic and related classes

Future Considerations for game rules:
 - Minimum/Maximum players changing the cards dealt and deck count


12/23/2024
FINISH LOGIC FOR VALID HANDS BASED ON ROUND
"""

from enum import Enum
from game_errors import EmptyDecksError
from cards import Card, Wild, Suit, Name
from player import Player

import random


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

    def play_down(self, player: Player, played_hand: list[list]) -> bool:
        temp = []
        if self.is_valid_play_down(played_hand):
            player.play_hand(played_hand)
            for hand in played_hand:
                player.remove_cards(hand)
                temp.append(hand)
            if player.has_leftover_card() and self.round != 7:
                return True
            if not player.has_leftover_card() and self.round == 7:
                return True
            for ls in temp:
                for card in ls:
                    player.add_card(card)
        return False

    def is_valid_play_down(self, played_hand: list[list]) -> bool:
        """Determines if the played hands are valid according to the current round.

        Args:
            played_hand (list[list]): The list of hands played. Divided into players choice of cards.

        Returns:
            bool: True if every round requirement is met or false if incorrect hands for the current round.
        """

        # Match for rounds
        copy_hand = played_hand.copy()
        match (self.round):
            case 1:
                return (
                    len(played_hand) == 2
                    and self.is_valid_set(copy_hand[0])
                    and self.is_valid_set(copy_hand[1])
                )

            case 2:
                # The issue is do I want to allow the player to select their group of cards in any order?
                # i.e (if round 2, player selects set first, then run. OR The player can choose the run first or set.)
                # Limiting the choice of what the player wants to select makes this part easier. Always setting sets firsts
                # makes testing easier

                # Make sets chosen first, later on in development perhaps comeback to allow for either order
                return (
                    len(played_hand) == 2
                    and self.is_valid_set(copy_hand[0])
                    and self.is_valid_run(copy_hand[1])
                )

            case 3:
                return (
                    len(played_hand) == 2
                    and self.is_valid_run(copy_hand[0])
                    and self.is_valid_run(copy_hand[1])
                )

            case 4:
                return (
                    len(played_hand) == 3
                    and self.is_valid_set(copy_hand[0])
                    and self.is_valid_set(copy_hand[1])
                    and self.is_valid_set(copy_hand[2])
                )

            case 5:
                return (
                    len(played_hand) == 3
                    and self.is_valid_set(copy_hand[0])
                    and self.is_valid_set(copy_hand[1])
                    and self.is_valid_run(copy_hand[2])
                )

            case 6:
                return (
                    len(played_hand) == 3
                    and self.is_valid_set(copy_hand[0])
                    and self.is_valid_run(copy_hand[1])
                    and self.is_valid_run(copy_hand[2])
                )

            case 7:
                return (
                    len(played_hand) == 3
                    and self.is_valid_run(copy_hand[0])
                    and self.is_valid_run(copy_hand[1])
                    and self.is_valid_run(copy_hand[2])
                )

            case _:
                raise ValueError

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
        print(played_hand)

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

    def is_wild(self, card: Card) -> bool:
        return card.suit == Suit.WILD or card.value == 20

    def play_hands(self, player: Player, played_hand: list[list]) -> bool:
        pass

    def shuffle_deck(self) -> None:
        """Shuffles self.deck and updates in place.

        It modifies the deck directly and can be called without storing the result.

        Returns:
            list: the shuffled deck
        """
        return random.shuffle(self.deck)

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
        id = 1
        deck = []
        for suit in list(Suit)[:4]:
            for name in list(Name)[2:]:
                if name == Name.TWO:
                    deck.append(Wild(name, suit, id))
                    id += 1
                    deck.append(Wild(name, suit, id))
                    id += 1
                else:
                    deck.append(Card(name, suit, id))
                    id += 1
                    deck.append(Card(name, suit, id))
                    id += 1
        for _ in range(2):
            deck.append(Wild(Name.JOKER, Suit.WILD, id))
            id += 1
            deck.append(Wild(Name.JOKER, Suit.WILD, id))
            id += 1

        return deck

    def _generate_players(self, num: int) -> list:
        players = []
        for _ in range(num):
            players.append(Player())
        return players

    # Magic Methods #

    def __repr__(self):
        return f"{self.players} {self.deck} {self.winner}"


g = Game()
g.round = 1
g.display_players()
g.players[0].hand = [
    Card(Name.FOUR, Suit.DIAMONDS, 1),
    Card(Name.FOUR, Suit.DIAMONDS, 2),
    Card(Name.FOUR, Suit.CLUBS, 3),
    Card(Name.FIVE, Suit.DIAMONDS, 4),
    Card(Name.FIVE, Suit.DIAMONDS, 5),
    Card(Name.FIVE, Suit.CLUBS, 6),
    Card(Name.FOUR, Suit.DIAMONDS, 7),
    Card(Name.FOUR, Suit.DIAMONDS, 8),
    Card(Name.FOUR, Suit.CLUBS, 9),
]

g.display_players()
g.play_down(
    g.players[0],
    [
        [
            Card(Name.FOUR, Suit.DIAMONDS, 1),
            Card(Name.FOUR, Suit.DIAMONDS, 2),
            Card(Name.FOUR, Suit.CLUBS, 3),
        ],
        [
            Card(Name.FIVE, Suit.DIAMONDS, 4),
            Card(Name.FIVE, Suit.DIAMONDS, 5),
            Card(Name.FIVE, Suit.CLUBS, 6),
        ],
    ],
)
g.display_players()
