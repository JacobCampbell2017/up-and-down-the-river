import game
from cards import Card, Wild, Name, Suit
from player import Player


def test_is_valid_set():

    # Four, Four, Four -> True because there are three fours
    play0 = [
        Card(Name.FOUR, Suit.DIAMONDS),
        Card(Name.FOUR, Suit.DIAMONDS),
        Card(Name.FOUR, Suit.CLUBS),
    ]

    # Ace, Two, Ace -> True because two is wild
    play1 = [
        Card(Name.ACE, Suit.DIAMONDS),
        Wild(Name.TWO, Suit.DIAMONDS),
        Card(Name.ACE, Suit.CLUBS),
    ]

    # Joker, King, King -> True because Joker is wild
    play2 = [
        Wild(Name.JOKER, Suit.WILD),
        Card(Name.KING, Suit.DIAMONDS),
        Card(Name.KING, Suit.CLUBS),
    ]

    # Ace, Two, Three -> False because Ace and Three are not of the same Set
    invalid_play0 = [
        Card(Name.ACE, Suit.DIAMONDS),
        Wild(Name.TWO, Suit.DIAMONDS),
        Card(Name.THREE, Suit.CLUBS),
    ]

    # Joker, Two, Two -> False because there is no non-wild card
    invalid_play1 = [
        Wild(Name.JOKER, Suit.WILD),
        Wild(Name.TWO, Suit.DIAMONDS),
        Wild(Name.TWO, Suit.CLUBS),
    ]

    # Six, Nine, Eight -> False because all different cards
    invalid_play2 = [
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.NINE, Suit.DIAMONDS),
        Card(Name.EIGHT, Suit.CLUBS),
    ]

    # Jack -> False because not enough cards for a set
    invalid_one_card = [Card(Name.JACK, Suit.SPADES)]

    # Six, Six, Six, Six -> False because too many cards for a set
    invalid_four_card = [
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SIX, Suit.CLUBS),
        Card(Name.SIX, Suit.SPADES),
    ]

    # None -> False because no cards silly!
    invalid_no_card = []

    game_instance = game.Game()

    # Valid Sets
    assert game_instance.is_valid_set(play0)
    assert game_instance.is_valid_set(play1)
    assert game_instance.is_valid_set(play2)

    # Invalid Sets
    assert not game_instance.is_valid_set(invalid_play0)
    assert not game_instance.is_valid_set(invalid_play1)
    assert not game_instance.is_valid_set(invalid_play2)
    assert not game_instance.is_valid_set(invalid_one_card)
    assert not game_instance.is_valid_set(invalid_four_card)
    assert not game_instance.is_valid_set(invalid_no_card)


def test_is_valid_run():

    # Valid runs
    # Three, Four, Five, Six, Seven of diamonds run
    play0 = [
        Card(Name.THREE, Suit.DIAMONDS),
        Card(Name.FOUR, Suit.DIAMONDS),
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        Card(Name.TEN, Suit.CLUBS),
        Card(Name.JACK, Suit.CLUBS),
        Card(Name.KING, Suit.CLUBS),
        Card(Name.QUEEN, Suit.CLUBS),
    ]

    wildcard1 = Wild(Name.TWO, Suit.CLUBS)
    wildcard1.set_value("EIGHT")
    wildcard2 = Wild(Name.JOKER, Suit.WILD)
    wildcard2.set_value("NINE")

    # Wild, Wild, Ten, Jack of Hearts run, it is valid because the wilds were given their temporary values before hand
    play2 = [
        wildcard1,
        wildcard2,
        Card(Name.TEN, Suit.HEARTS),
        Card(Name.JACK, Suit.HEARTS),
    ]

    wildcard1.set_value("NINE")
    wildcard2.set_value("QUEEN")
    # Ten, Wild , Jack, Wild of Diamonds run, it is valid because wilds are given temporary values before hand
    # and sorted before validation
    play3 = [
        Card(Name.TEN, Suit.HEARTS),
        wildcard2,
        Card(Name.JACK, Suit.HEARTS),
        wildcard1,
    ]

    # Invalid runs
    # Cards are not in sequence
    invalid_play0 = [
        Card(Name.THREE, Suit.DIAMONDS),
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
    ]

    # Cards are not of the same suit
    invalid_play1 = [
        Card(Name.THREE, Suit.DIAMONDS),
        Card(Name.FOUR, Suit.CLUBS),
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.HEARTS),
    ]

    # Wildcards are not assigned temporary values
    invalid_play2 = [
        Wild(Name.TWO, Suit.CLUBS),
        Wild(Name.JOKER, Suit.WILD),
        Card(Name.THREE, Suit.CLUBS),
        Card(Name.FOUR, Suit.CLUBS),
    ]

    # Duplicates in the run
    invalid_play3 = [
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.EIGHT, Suit.DIAMONDS),
        Card(Name.NINE, Suit.DIAMONDS),
    ]

    # Too many cards in the run
    invalid_play4 = [
        Card(Name.SIX, Suit.CLUBS),
        Card(Name.FIVE, Suit.CLUBS),
        Card(Name.THREE, Suit.CLUBS),
        Card(Name.FOUR, Suit.CLUBS),
        Card(Name.SEVEN, Suit.CLUBS),
    ]

    # Not enough cards in the run
    invalid_play5 = [
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.EIGHT, Suit.DIAMONDS),
        Card(Name.NINE, Suit.DIAMONDS),
    ]

    wildcard3 = Wild(Name.JOKER, Suit.WILD)
    wildcard4 = Wild(Name.JOKER, Suit.WILD)
    wildcard3.set_value("TEN")
    wildcard4.set_value("JACK")
    invalid_play6 = [
        wildcard1,
        wildcard2,
        wildcard3,
        wildcard4,
    ]

    game_instance = game.Game()

    # Valid runs
    assert game_instance.is_valid_run(play0)
    assert game_instance.is_valid_run(play1)
    assert game_instance.is_valid_run(play2)
    assert game_instance.is_valid_run(play3)

    # Invalid runs
    assert not game_instance.is_valid_run(invalid_play0)
    assert not game_instance.is_valid_run(invalid_play1)
    assert not game_instance.is_valid_run(invalid_play2)
    assert not game_instance.is_valid_run(invalid_play3)
    assert not game_instance.is_valid_run(invalid_play4)
    assert not game_instance.is_valid_run(invalid_play5)
    assert not game_instance.is_valid_run(invalid_play6)


def test_is_valid_runRound7():
    """Tests runs when game round is 7. Runs can be longer than 4"""

    # Valid runs
    wildcard1 = Wild(Name.TWO, Suit.CLUBS)
    wildcard1.set_value("JACK")
    wildcard2 = Wild(Name.JOKER, Suit.WILD)
    wildcard2.set_value("QUEEN")

    play0 = [
        Card(Name.THREE, Suit.DIAMONDS),
        Card(Name.FOUR, Suit.DIAMONDS),
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.EIGHT, Suit.DIAMONDS),
        Card(Name.NINE, Suit.DIAMONDS),
        Card(Name.TEN, Suit.DIAMONDS),
        Card(Name.KING, Suit.DIAMONDS),
        Card(Name.ACE, Suit.DIAMONDS),
        wildcard1,
        wildcard2,
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        Card(Name.TEN, Suit.CLUBS),
        Card(Name.JACK, Suit.CLUBS),
        Card(Name.KING, Suit.CLUBS),
        Card(Name.QUEEN, Suit.CLUBS),
        Card(Name.ACE, Suit.CLUBS),
    ]

    game_instance = game.Game()
    game_instance.round = 7

    # Valid runs
    assert game_instance.is_valid_run(play0)
    assert game_instance.is_valid_run(play1)


def test_determine_winner():
    """Tests if Winner is determined correctly"""
    players = [Player("Nestor"), Player("Jacob"), Player("Summer")]

    players[0].score = 100
    players[1].score = 50
    players[2].score = 150

    game_instance = game.Game()
    game_instance.players = players
    assert game_instance.determine_winner()[0].name == "Jacob"

    players[0].score = 100
    players[1].score = 50
    players[2].score = 50

    winners = game_instance.determine_winner()
    assert winners[0].name == "Jacob" and winners[1].name == "Summer"

    players[0].score = 0
    players = [Player("Nestor")]
    game_instance.players = players
    assert game_instance.determine_winner()[0].name == "Nestor"


def test_round_1():
    game_instance = game.Game()
    game_instance.round = 1

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SIX, Suit.CLUBS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )


def test_round_2():
    game_instance = game.Game()
    game_instance.round = 2

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.JACK, Suit.DIAMONDS),
                Card(Name.JACK, Suit.HEARTS),
                Card(Name.JACK, Suit.SPADES),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES)
    wildcard1.set_value("JACK")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.TEN, Suit.DIAMONDS),
                wildcard1,
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES)
    wildcard1.set_value("NINE")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS)
    wildcard2.set_value("JACK")
    wildcard3 = Wild(Name.JOKER, Suit.WILD)
    wildcard3.set_value("EIGHT")

    assert game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                wildcard2,
                Card(Name.TEN, Suit.DIAMONDS),
                wildcard1,
                wildcard3,
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
                Card(Name.FOUR, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FIVE, Suit.HEARTS),
                Card(Name.SIX, Suit.HEARTS),
                Card(Name.SEVEN, Suit.HEARTS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard4 = Wild(Name.JOKER, Suit.WILD)
    wildcard4.set_value("TEN")
    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                wildcard2,
                wildcard4,
                wildcard1,
                wildcard3,
            ],
        ]
    )


def test_round_3():
    game_instance = game.Game()
    game_instance.round = 3

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES)
    wildcard1.set_value("JACK")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS)
    wildcard2.set_value("JACK")

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.TEN, Suit.DIAMONDS),
                wildcard2,
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.TEN, Suit.DIAMONDS),
                wildcard1,
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
        ]
    )

    # Invalid Hands
    wildcard1 = Wild(Name.TWO, Suit.SPADES)
    wildcard1.set_value("NINE")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS)
    wildcard2.set_value("JACK")
    wildcard3 = Wild(Name.JOKER, Suit.WILD)
    wildcard3.set_value("EIGHT")
    wildcard4 = Wild(Name.JOKER, Suit.WILD)
    wildcard4.set_value("TEN")

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                wildcard2,
                Card(Name.TEN, Suit.DIAMONDS),
                wildcard1,
                wildcard3,
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
                Card(Name.FOUR, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                wildcard4,
                wildcard2,
                wildcard1,
                wildcard3,
            ],
            [
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FIVE, Suit.HEARTS),
                Card(Name.SIX, Suit.HEARTS),
                Card(Name.SEVEN, Suit.HEARTS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard4 = Wild(Name.JOKER, Suit.WILD)
    wildcard4.set_value("TEN")
    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.HEARTS),
                Card(Name.FOUR, Suit.SPADES),
            ],
            [
                wildcard2,
                wildcard4,
                wildcard1,
                wildcard3,
            ],
        ]
    )


def test_round_4():
    game_instance = game.Game()
    game_instance.round = 4

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SIX, Suit.CLUBS),
            ],
        ]
    )

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SIX, Suit.CLUBS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )


def test_round_5():
    game_instance = game.Game()
    game_instance.round = 5

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.HEARTS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SIX, Suit.CLUBS),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.DIAMONDS),
            ],
            [
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.ACE, Suit.SPADES),
                Card(Name.ACE, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS),
                Card(Name.JACK, Suit.DIAMONDS),
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )


def test_round_6():
    game_instance = game.Game()
    game_instance.round = 6

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard1 = Wild(Name.JOKER, Suit.WILD)
    wildcard1.set_value("SIX")
    wildcard2 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard2.set_value("KING")
    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS),
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS),
                Card(Name.ACE, Suit.SPADES),
                Card(Name.ACE, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )


def test_round_7():
    game_instance = game.Game()
    game_instance.round = 7

    # Valid Hands
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.NINE, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    wildcard1 = Wild(Name.JOKER, Suit.WILD)
    wildcard1.set_value("SIX")
    wildcard2 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard2.set_value("KING")
    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS),
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS),
                Card(Name.QUEEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Wild(Name.JOKER, Suit.WILD),
                Card(Name.FOUR, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
                Wild(Name.JOKER, Suit.WILD),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS),
                Wild(Name.TWO, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.CLUBS),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS),
                Card(Name.FIVE, Suit.DIAMONDS),
                Card(Name.SIX, Suit.DIAMONDS),
                Card(Name.SEVEN, Suit.DIAMONDS),
            ],
        ]
    )


def test_play_down():
    g = game.Game()

    # Round 1
    g.round = 1
    g.players[0].hand = [
        Card(Name.FOUR, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.HEARTS, 2),
        Card(Name.FOUR, Suit.CLUBS, 3),
        Card(Name.FIVE, Suit.DIAMONDS, 4),
        Card(Name.FIVE, Suit.HEARTS, 5),
        Card(Name.FIVE, Suit.CLUBS, 6),
        Card(Name.NINE, Suit.CLUBS, 7),
    ]

    assert g.play_down(
        g.players[0],
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.HEARTS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
        ],
    )

    g.players[0].hand = [
        Card(Name.FOUR, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.HEARTS, 2),
        Card(Name.FIVE, Suit.DIAMONDS, 3),
    ]

    assert not g.play_down(
        g.players[0],
        [
            [Card(Name.FOUR, Suit.DIAMONDS, 1), Card(Name.FOUR, Suit.HEARTS, 2)],
            [Card(Name.FIVE, Suit.DIAMONDS, 3)],
        ],
    )

    # Round 2
    g.round = 2
    g.players[0].hand = [
        Card(Name.THREE, Suit.HEARTS, 1),
        Card(Name.FOUR, Suit.HEARTS, 2),
        Card(Name.FIVE, Suit.HEARTS, 3),
        Card(Name.SIX, Suit.HEARTS, 4),
        Card(Name.SEVEN, Suit.HEARTS, 5),
        Card(Name.FIVE, Suit.DIAMONDS, 6),
        Card(Name.FIVE, Suit.CLUBS, 7),
        Card(Name.FIVE, Suit.SPADES, 8),
    ]

    assert g.play_down(
        g.players[0],
        [
            [
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.FIVE, Suit.CLUBS, 7),
                Card(Name.FIVE, Suit.SPADES, 8),
            ],
            [
                Card(Name.THREE, Suit.HEARTS, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FIVE, Suit.HEARTS, 3),
                Card(Name.SIX, Suit.HEARTS, 4),
            ],
        ],
    )

    # Round 3
    g.round = 3
    g.players[0].hand = [
        Card(Name.THREE, Suit.CLUBS, 1),
        Card(Name.FOUR, Suit.CLUBS, 2),
        Card(Name.FIVE, Suit.CLUBS, 3),
        Card(Name.SIX, Suit.CLUBS, 4),
        Card(Name.SEVEN, Suit.DIAMONDS, 5),
        Card(Name.EIGHT, Suit.DIAMONDS, 6),
        Card(Name.NINE, Suit.DIAMONDS, 7),
        Card(Name.TEN, Suit.DIAMONDS, 8),
        Card(Name.THREE, Suit.SPADES, 9),
    ]

    assert g.play_down(
        g.players[0],
        [
            [
                Card(Name.THREE, Suit.CLUBS, 1),
                Card(Name.FOUR, Suit.CLUBS, 2),
                Card(Name.FIVE, Suit.CLUBS, 3),
                Card(Name.SIX, Suit.CLUBS, 4),
            ],
            [
                Card(Name.SEVEN, Suit.DIAMONDS, 5),
                Card(Name.EIGHT, Suit.DIAMONDS, 6),
                Card(Name.NINE, Suit.DIAMONDS, 7),
                Card(Name.TEN, Suit.DIAMONDS, 8),
            ],
        ],
    )

    # Round 4
    g.round = 4
    g.players[0].hand = [
        Card(Name.THREE, Suit.CLUBS, 1),
        Card(Name.THREE, Suit.HEARTS, 2),
        Card(Name.THREE, Suit.SPADES, 3),
        Card(Name.SIX, Suit.CLUBS, 4),
        Card(Name.SIX, Suit.HEARTS, 5),
        Card(Name.SIX, Suit.SPADES, 6),
        Card(Name.NINE, Suit.CLUBS, 7),
        Card(Name.NINE, Suit.HEARTS, 8),
        Card(Name.NINE, Suit.SPADES, 9),
        Card(Name.TEN, Suit.DIAMONDS, 10),
    ]

    assert g.play_down(
        g.players[0],
        [
            [
                Card(Name.THREE, Suit.CLUBS, 1),
                Card(Name.THREE, Suit.HEARTS, 2),
                Card(Name.THREE, Suit.SPADES, 3),
            ],
            [
                Card(Name.SIX, Suit.CLUBS, 4),
                Card(Name.SIX, Suit.HEARTS, 5),
                Card(Name.SIX, Suit.SPADES, 6),
            ],
            [
                Card(Name.NINE, Suit.CLUBS, 7),
                Card(Name.NINE, Suit.HEARTS, 8),
                Card(Name.NINE, Suit.SPADES, 9),
            ],
        ],
    )

    # Round 7
    g.round = 7
    g.players[0].hand = [
        Wild(Name.TWO, Suit.WILD, 1),
        Card(Name.THREE, Suit.CLUBS, 2),
        Card(Name.FOUR, Suit.CLUBS, 3),
        Card(Name.FIVE, Suit.CLUBS, 4),
        Card(Name.FOUR, Suit.HEARTS, 5),
        Card(Name.FIVE, Suit.HEARTS, 6),
        Card(Name.SIX, Suit.HEARTS, 7),
        Card(Name.SEVEN, Suit.HEARTS, 8),
        Card(Name.EIGHT, Suit.HEARTS, 9),
        Card(Name.NINE, Suit.DIAMONDS, 10),
        Card(Name.TEN, Suit.DIAMONDS, 11),
        Card(Name.JACK, Suit.DIAMONDS, 12),
        Card(Name.QUEEN, Suit.DIAMONDS, 13),
    ]
    g.players[0].hand[0].set_value("SIX")

    assert g.play_down(
        g.players[0],
        [
            [
                g.players[0].hand[0],
                Card(Name.THREE, Suit.CLUBS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
                Card(Name.FIVE, Suit.CLUBS, 4),
            ],
            [
                Card(Name.FOUR, Suit.HEARTS, 5),
                Card(Name.FIVE, Suit.HEARTS, 6),
                Card(Name.SIX, Suit.HEARTS, 7),
                Card(Name.SEVEN, Suit.HEARTS, 8),
                Card(Name.EIGHT, Suit.HEARTS, 9),
            ],
            [
                Card(Name.NINE, Suit.DIAMONDS, 10),
                Card(Name.TEN, Suit.DIAMONDS, 11),
                Card(Name.JACK, Suit.DIAMONDS, 12),
                Card(Name.QUEEN, Suit.DIAMONDS, 13),
            ],
        ],
    )


def test_is_run():
    game_instance = game.Game()
    set = [
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
    ]

    set_wild = [
        Wild(Name.JOKER, Suit.WILD),
        Card(Name.SEVEN, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
    ]

    run = [
        Card(Name.FOUR, Suit.DIAMONDS),
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
    ]

    wildcard1 = Wild(Name.TWO, Suit.CLUBS)
    wildcard1.set_value("EIGHT")
    run_wild = [
        wildcard1,
        Card(Name.FIVE, Suit.DIAMONDS),
        Card(Name.SIX, Suit.DIAMONDS),
        Card(Name.SEVEN, Suit.DIAMONDS),
    ]

    assert game_instance.is_set(set)
    assert game_instance.is_set(set_wild)
    assert not game_instance.is_set(run)
    assert not game_instance.is_set(run_wild)
