"""
12/18/2024 - The Beginning

Goal: Get a text version of the game to be able to played by one terminal

Contains game logic and related classes

Future Considerations for game rules:
 - Minimum/Maximum players changing the cards dealt and deck count


"""

from enum import Enum

import random


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


class Game:
    def __init__(self):
        self.players = [Player("A"), Player("B"), Player("C")]
        self.deck = self._generateDeck()
        self.discard = None
        self.winner = False
        self.currentPlayer = self.players[0]
        pass

    # Game Essentials

    def game_loop(self):
        """Main loop that will run the game until final round is played"""
        while self.winner == False:
            pass

    def drawCard(self) -> Card:
        """Returns a card from last Card in self.deck"""
        return self.deck.pop()

    def shuffleDeck(self) -> list:
        """Shuffles self.deck. Can be Called without storing in a variable.

        Returns:
            list: the shuffled deck
        """
        return random.shuffle(self.deck)

    def dealCards(self):
        """Adds 11 Cards to every players hand. The deck continues to be shuffled until the top card that is
        added to the discard pile is not a wild card.
        """
        for _ in range(11):
            for player in self.players:
                player.addCard(self.drawCard())
        x = self.deck[-1]
        while x.value == 20:
            self.shuffleDeck()
            x = self.deck[-1]
        self.discard = x

    # Display Functions #

    def displayDeck(self):
        """displays cards left in the deck"""
        for card in self.deck:
            print(str(card))

    def displayPlayers(self):
        """Displays players"""
        for player in self.players:
            print(player)

    def displayDiscard(self):
        """Displays the current card in the discard pile"""
        print(str(self.discard))

    # Game Setup #

    def _generateDeck(self) -> list:
        deck = []
        for suit in list(Suit)[:4]:
            for name in list(Name)[1:]:
                deck.append(Card(name, suit))
        deck.extend([Card(Name.JOKER, Suit.JOKER) for _ in range(4)])
        return deck * 2

    def _generatePlayers(self, num: int) -> list:
        players = []
        for _ in range(num):
            players.append(Player())
        return players

    # Magic Methods #

    def __repr__(self):
        return str(f"{self.players} {self.deck} {self.winner}")


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.hand = []

    def addCard(self, card: Card) -> list:
        return self.hand.append(card)

    def __str__(self):
        return str(f"{self.name} {self.score} {self.hand}")


z = Game()
z.shuffleDeck()
z.dealCards()
