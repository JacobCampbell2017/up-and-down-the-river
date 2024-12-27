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
        self.winner = []
        self.currentPlayer = self.players[0]
        self.round = 0
        pass

    # Game Essentials

    def game_loop(self):
        """Main loop that will run the game until final round is played"""
        self.shuffle_deck()
        self.deal_cards()
        while len(self.winner) == 0:
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
        for _ in range(num_of_cards):
            for player in self.players:
                player.add_card(self.draw_card())
        self.discard = self.deck[-1:]
        while self.discard[0].is_wild():
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
        if not self.is_valid_play_down(played_hand):
            return False

        original_hand = player.hand.copy()

        player.play_hand(played_hand)
        for hand in played_hand:
            player.remove_cards(hand)

        if (self.round != 7 and player.has_leftover_card()) or (
            self.round == 7 and not player.has_leftover_card()
        ):
            return True

        player.hand = original_hand
        return False

    def play_to_piles(player: Player, played_card: Card, target_pile: list) -> bool:
        if not player.has_played():
            return False

        return False

    def shuffle_deck(self) -> None:
        """Shuffles self.deck and updates in place.

        It modifies the deck directly and can be called without storing the result.

        Returns:
            list: the shuffled deck
        """
        return random.shuffle(self.deck)

    ########################
    # Validation Functions #
    ########################

    def is_set(self, pile: list[Card]) -> bool:
        """Determines if played down pile is set, can be used inverse to determine if run

        Returns:
            bool: True if set, False if run
        """
        wilds: Wild = []
        non_wilds = []
        for card in pile:
            if card.is_wild():
                wilds.append(card)
            else:
                non_wilds.append(card)

        name = non_wilds[0].name
        if all(card.name == non_wilds[0].name for card in non_wilds) and all(
            card.chosen_name == Name.INVALID for card in wilds
        ):
            return True
        return False

    def is_valid_play_down(self, played_hand: list[list]) -> bool:
        """Determines if the played hands are valid according to the current round.

        Args:
            played_hand (list[list]): The list of hands played. Divided into players choice of cards.

        Returns:
            bool: True if every round requirement is met or False if incorrect hands for the current round.
        """

        # Round requirements
        round_requirements = {
            1: [self.is_valid_set, self.is_valid_set],
            2: [self.is_valid_set, self.is_valid_run],
            3: [self.is_valid_run, self.is_valid_run],
            4: [self.is_valid_set, self.is_valid_set, self.is_valid_set],
            5: [self.is_valid_set, self.is_valid_set, self.is_valid_run],
            6: [self.is_valid_set, self.is_valid_run, self.is_valid_run],
            7: [self.is_valid_run, self.is_valid_run, self.is_valid_run],
        }

        if self.round not in round_requirements:
            raise ValueError(f"Invalid round number: {self.round}")

        requirements = round_requirements[self.round]

        if len(played_hand) != len(requirements):
            return False

        for hand, validate in zip(played_hand, requirements):
            if not validate(hand):
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
            if not card.is_wild():
                suit = card.suit
        if suit == Suit.WILD:
            return False

        base_card = played_hand[0]

        for card in played_hand[1:3]:
            if card.suit != suit and not card.is_wild():
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

        if played_hand[0].is_wild():
            return False

        if (
            played_hand[0].name != played_hand[1].name and not played_hand[1].is_wild()
        ) or (
            played_hand[0].name != played_hand[2].name and not played_hand[2].is_wild()
        ):
            return False

        return True

    #####################
    # Display Functions #
    #####################

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

    #################
    # Magic Methods #
    #################

    def __repr__(self):
        return f"{self.players} {self.deck} {self.winner}"
