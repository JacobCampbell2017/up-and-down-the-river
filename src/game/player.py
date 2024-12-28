"""
player.py

contains class for player
"""

from cards import Card


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.hand = []
        self.played_hands = []

    def add_card(self, card: Card) -> None:
        return self.hand.append(card)

    def has_leftover_card(self) -> bool:
        return len(self.hand) >= 1

    def has_played(self) -> bool:
        return len(self.played_hands) > 0

    def play_hand(self, played_hand: list[list]) -> list:
        for hand in played_hand:
            self.played_hands.append(hand.copy())
        return played_hand

    def remove_cards(self, cards: list) -> list:
        self.hand = [card for card in self.hand if card.id not in [c.id for c in cards]]
        return self.hand

    def __repr__(self):
        hand_str = ", ".join(str(card) for card in self.hand[:5]) + (
            "..." if len(self.hand) > 5 else ""
        )
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}] | Piles: {self.played_hands}"

    def __str__(self):
        hand_str = ", ".join(str(card) for card in self.hand[:5]) + (
            "..." if len(self.hand) > 5 else ""
        )
        return f"Player {self.name} | Score: {self.score} | Hand: [{hand_str}] | Piles: {self.played_hands}"

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
