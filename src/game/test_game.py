import game
from cards import Card, Wild, Name, Suit
from player import Player


def test_is_valid_set():

    # Four, Four, Four -> True because there are three fours
    play0 = [
        Card(Name.FOUR, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.DIAMONDS, 2),
        Card(Name.FOUR, Suit.CLUBS, 3),
    ]

    # Ace, Two, Ace -> True because two is wild
    play1 = [
        Card(Name.ACE, Suit.DIAMONDS, 1),
        Wild(Name.TWO, Suit.DIAMONDS, 2),
        Card(Name.ACE, Suit.CLUBS, 3),
    ]

    # Joker, King, King -> True because Joker is wild
    play2 = [
        Wild(Name.JOKER, Suit.WILD, 1),
        Card(Name.KING, Suit.DIAMONDS, 2),
        Card(Name.KING, Suit.CLUBS, 3),
    ]

    # Ace, Two, Three -> False because Ace and Three are not of the same Set
    invalid_play0 = [
        Card(Name.ACE, Suit.DIAMONDS, 1),
        Wild(Name.TWO, Suit.DIAMONDS, 2),
        Card(Name.THREE, Suit.CLUBS, 3),
    ]

    # Joker, Two, Two -> False because there is no non-wild card
    invalid_play1 = [
        Wild(Name.JOKER, Suit.WILD, 1),
        Wild(Name.TWO, Suit.DIAMONDS, 3),
        Wild(Name.TWO, Suit.CLUBS, 2),
    ]

    # Six, Nine, Eight -> False because all different cards
    invalid_play2 = [
        Card(Name.SIX, Suit.DIAMONDS, 1),
        Card(Name.NINE, Suit.DIAMONDS, 2),
        Card(Name.EIGHT, Suit.CLUBS, 3),
    ]

    # Jack -> False because not enough cards for a set
    invalid_one_card = [Card(Name.JACK, Suit.SPADES, 1)]

    # Six, Six, Six, Six -> False because too many cards for a set
    invalid_four_card = [
        Card(Name.SIX, Suit.DIAMONDS, 1),
        Card(Name.SIX, Suit.DIAMONDS, 2),
        Card(Name.SIX, Suit.CLUBS, 3),
        Card(Name.SIX, Suit.SPADES, 4),
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
        Card(Name.THREE, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.DIAMONDS, 2),
        Card(Name.FIVE, Suit.DIAMONDS, 3),
        Card(Name.SIX, Suit.DIAMONDS, 4),
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        Card(Name.TEN, Suit.CLUBS, 5),
        Card(Name.JACK, Suit.CLUBS, 6),
        Card(Name.KING, Suit.CLUBS, 7),
        Card(Name.QUEEN, Suit.CLUBS, 8),
    ]

    wildcard1 = Wild(Name.TWO, Suit.CLUBS, 9)
    wildcard1.set_value("EIGHT")
    wildcard2 = Wild(Name.JOKER, Suit.WILD, 10)
    wildcard2.set_value("NINE")

    # Wild, Wild, Ten, Jack of Hearts run, it is valid because the wilds were given their temporary values before hand
    play2 = [
        wildcard1,
        wildcard2,
        Card(Name.TEN, Suit.HEARTS, 1),
        Card(Name.JACK, Suit.HEARTS, 2),
    ]

    wildcard1.set_value("NINE")
    wildcard2.set_value("QUEEN")
    # Ten, Wild , Jack, Wild of Diamonds run, it is valid because wilds are given temporary values before hand
    # and sorted before validation
    play3 = [
        Card(Name.TEN, Suit.HEARTS, 1),
        wildcard2,
        Card(Name.JACK, Suit.HEARTS, 2),
        wildcard1,
    ]

    # Invalid runs
    # Cards are not in sequence
    invalid_play0 = [
        Card(Name.THREE, Suit.DIAMONDS, 1),
        Card(Name.FIVE, Suit.DIAMONDS, 2),
        Card(Name.SIX, Suit.DIAMONDS, 3),
        Card(Name.SEVEN, Suit.DIAMONDS, 4),
    ]

    # Cards are not of the same suit
    invalid_play1 = [
        Card(Name.THREE, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.CLUBS, 2),
        Card(Name.FIVE, Suit.DIAMONDS, 3),
        Card(Name.SIX, Suit.HEARTS, 4),
    ]

    # Wildcards are not assigned temporary values
    invalid_play2 = [
        Wild(Name.TWO, Suit.CLUBS, 1),
        Wild(Name.JOKER, Suit.WILD, 2),
        Card(Name.THREE, Suit.CLUBS, 3),
        Card(Name.FOUR, Suit.CLUBS, 4),
    ]

    # Duplicates in the run
    invalid_play3 = [
        Card(Name.SEVEN, Suit.DIAMONDS, 1),
        Card(Name.SEVEN, Suit.DIAMONDS, 2),
        Card(Name.EIGHT, Suit.DIAMONDS, 3),
        Card(Name.NINE, Suit.DIAMONDS, 4),
    ]

    # Too many cards in the run
    invalid_play4 = [
        Card(Name.SIX, Suit.CLUBS, 1),
        Card(Name.FIVE, Suit.CLUBS, 2),
        Card(Name.THREE, Suit.CLUBS, 3),
        Card(Name.FOUR, Suit.CLUBS, 4),
        Card(Name.SEVEN, Suit.CLUBS, 5),
    ]

    # Not enough cards in the run
    invalid_play5 = [
        Card(Name.SEVEN, Suit.DIAMONDS, 1),
        Card(Name.EIGHT, Suit.DIAMONDS, 2),
        Card(Name.NINE, Suit.DIAMONDS, 3),
    ]

    wildcard3 = Wild(Name.JOKER, Suit.WILD, 80)
    wildcard4 = Wild(Name.JOKER, Suit.WILD, 50)
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
    wildcard1 = Wild(Name.TWO, Suit.CLUBS, 100)
    wildcard1.set_value("JACK")
    wildcard2 = Wild(Name.JOKER, Suit.WILD, 200)
    wildcard2.set_value("QUEEN")

    play0 = [
        Card(Name.THREE, Suit.DIAMONDS, 1),
        Card(Name.FOUR, Suit.DIAMONDS, 2),
        Card(Name.FIVE, Suit.DIAMONDS, 3),
        Card(Name.SIX, Suit.DIAMONDS, 4),
        Card(Name.SEVEN, Suit.DIAMONDS, 5),
        Card(Name.EIGHT, Suit.DIAMONDS, 6),
        Card(Name.NINE, Suit.DIAMONDS, 7),
        Card(Name.TEN, Suit.DIAMONDS, 8),
        Card(Name.KING, Suit.DIAMONDS, 9),
        Card(Name.ACE, Suit.DIAMONDS, 10),
        wildcard1,
        wildcard2,
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        Card(Name.TEN, Suit.CLUBS, 1),
        Card(Name.JACK, Suit.CLUBS, 2),
        Card(Name.KING, Suit.CLUBS, 3),
        Card(Name.QUEEN, Suit.CLUBS, 4),
        Card(Name.ACE, Suit.CLUBS, 5),
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
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
        ]
    )

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FOUR, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Card(Name.FOUR, Suit.DIAMONDS, 8),
                Card(Name.FOUR, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Wild(Name.JOKER, Suit.WILD, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SIX, Suit.CLUBS, 1),
                Card(Name.SIX, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
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
                Card(Name.JACK, Suit.DIAMONDS, 1),
                Card(Name.JACK, Suit.HEARTS, 2),
                Card(Name.JACK, Suit.SPADES, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES, 100)
    wildcard1.set_value("JACK")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
            ],
            [
                Card(Name.NINE, Suit.DIAMONDS, 4),
                Card(Name.TEN, Suit.DIAMONDS, 5),
                wildcard1,
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES, 200)
    wildcard1.set_value("NINE")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS, 300)
    wildcard2.set_value("JACK")
    wildcard3 = Wild(Name.JOKER, Suit.WILD, 400)
    wildcard3.set_value("EIGHT")

    assert game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
            ],
            [
                wildcard2,
                Card(Name.TEN, Suit.DIAMONDS, 4),
                wildcard1,
                wildcard3,
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FOUR, Suit.CLUBS, 6),
                Card(Name.FOUR, Suit.DIAMONDS, 7),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.HEARTS, 5),
                Card(Name.FIVE, Suit.HEARTS, 6),
                Card(Name.SIX, Suit.HEARTS, 7),
                Card(Name.SEVEN, Suit.HEARTS, 8),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.DIAMONDS, 9),
                Card(Name.SIX, Suit.DIAMONDS, 10),
                Card(Name.SEVEN, Suit.DIAMONDS, 11),
            ],
        ]
    )

    wildcard4 = Wild(Name.JOKER, Suit.WILD, 500)
    wildcard4.set_value("TEN")
    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
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
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SEVEN, Suit.DIAMONDS, 8),
            ],
        ]
    )

    wildcard1 = Wild(Name.TWO, Suit.SPADES, 100)
    wildcard1.set_value("JACK")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS, 200)
    wildcard2.set_value("JACK")

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.NINE, Suit.DIAMONDS, 1),
                Card(Name.TEN, Suit.DIAMONDS, 2),
                wildcard2,
                Card(Name.QUEEN, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.NINE, Suit.DIAMONDS, 4),
                Card(Name.TEN, Suit.DIAMONDS, 5),
                wildcard1,
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
        ]
    )

    # Invalid Hands
    wildcard1 = Wild(Name.TWO, Suit.SPADES, 983)
    wildcard1.set_value("NINE")
    wildcard2 = Wild(Name.TWO, Suit.CLUBS, 209)
    wildcard2.set_value("JACK")
    wildcard3 = Wild(Name.JOKER, Suit.WILD, 304)
    wildcard3.set_value("EIGHT")
    wildcard4 = Wild(Name.JOKER, Suit.WILD, 121)
    wildcard4.set_value("TEN")

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
            ],
            [
                wildcard2,
                Card(Name.TEN, Suit.DIAMONDS, 4),
                wildcard1,
                wildcard3,
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FOUR, Suit.CLUBS, 6),
                Card(Name.FOUR, Suit.DIAMONDS, 7),
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
                Card(Name.FOUR, Suit.HEARTS, 1),
                Card(Name.FIVE, Suit.HEARTS, 2),
                Card(Name.SIX, Suit.HEARTS, 3),
                Card(Name.SEVEN, Suit.HEARTS, 4),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.DIAMONDS, 9),
                Card(Name.SIX, Suit.DIAMONDS, 10),
                Card(Name.SEVEN, Suit.DIAMONDS, 11),
            ],
        ]
    )

    wildcard4 = Wild(Name.JOKER, Suit.WILD, 3213)
    wildcard4.set_value("TEN")
    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FOUR, Suit.HEARTS, 2),
                Card(Name.FOUR, Suit.SPADES, 3),
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
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SIX, Suit.DIAMONDS, 81),
                Card(Name.SIX, Suit.CLUBS, 9),
            ],
        ]
    )

    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                Wild(Name.TWO, Suit.DIAMONDS, 8),
                Wild(Name.JOKER, Suit.WILD, 9),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FOUR, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Card(Name.FIVE, Suit.DIAMONDS, 8),
                Card(Name.SIX, Suit.DIAMONDS, 9),
                Card(Name.SEVEN, Suit.DIAMONDS, 10),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Wild(Name.JOKER, Suit.WILD, 8),
                Card(Name.FOUR, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Wild(Name.JOKER, Suit.WILD, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Wild(Name.TWO, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                Wild(Name.TWO, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SIX, Suit.CLUBS, 1),
                Card(Name.SIX, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
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
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.HEARTS, 4),
                Card(Name.SIX, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.CLUBS, 6),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS, 7),
                Card(Name.SIX, Suit.DIAMONDS, 8),
                Card(Name.NINE, Suit.DIAMONDS, 9),
                Card(Name.SEVEN, Suit.DIAMONDS, 10),
            ],
        ]
    )

    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS, 120)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS, 121)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.DIAMONDS, 3),
            ],
            [
                Wild(Name.TWO, Suit.DIAMONDS, 1),
                Card(Name.ACE, Suit.SPADES, 2),
                Card(Name.ACE, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 5),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FIVE, Suit.CLUBS, 3),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS, 4),
                Card(Name.JACK, Suit.DIAMONDS, 5),
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.DIAMONDS, 9),
                Card(Name.SIX, Suit.DIAMONDS, 10),
                Card(Name.SEVEN, Suit.DIAMONDS, 11),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Wild(Name.JOKER, Suit.WILD, 8),
                Card(Name.FOUR, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Wild(Name.JOKER, Suit.WILD, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                Wild(Name.TWO, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SEVEN, Suit.DIAMONDS, 8),
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
                Card(Name.SEVEN, Suit.DIAMONDS, 1),
                Card(Name.SEVEN, Suit.DIAMONDS, 2),
                Card(Name.SEVEN, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Card(Name.SIX, Suit.DIAMONDS, 5),
                Card(Name.SEVEN, Suit.DIAMONDS, 6),
                Card(Name.EIGHT, Suit.DIAMONDS, 7),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
                Card(Name.SIX, Suit.DIAMONDS, 9),
                Card(Name.NINE, Suit.DIAMONDS, 10),
                Card(Name.SEVEN, Suit.DIAMONDS, 11),
            ],
        ]
    )

    wildcard1 = Wild(Name.JOKER, Suit.WILD, 111)
    wildcard1.set_value("SIX")
    wildcard2 = Wild(Name.TWO, Suit.DIAMONDS, 112)
    wildcard2.set_value("KING")
    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS, 113)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS, 114)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.FIVE, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS, 4),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS, 5),
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS, 1),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FIVE, Suit.CLUBS, 3),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS, 4),
                Card(Name.ACE, Suit.SPADES, 5),
                Card(Name.ACE, Suit.DIAMONDS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
                Card(Name.FOUR, Suit.CLUBS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SEVEN, Suit.DIAMONDS, 8),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 9),
                Card(Name.FIVE, Suit.DIAMONDS, 10),
                Card(Name.SIX, Suit.DIAMONDS, 11),
                Card(Name.SEVEN, Suit.DIAMONDS, 12),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Wild(Name.JOKER, Suit.WILD, 8),
                Card(Name.FOUR, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Wild(Name.JOKER, Suit.WILD, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                Wild(Name.TWO, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SEVEN, Suit.DIAMONDS, 8),
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
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 5),
                Card(Name.SIX, Suit.DIAMONDS, 6),
                Card(Name.SEVEN, Suit.DIAMONDS, 7),
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
            [
                Card(Name.EIGHT, Suit.DIAMONDS, 9),
                Card(Name.SIX, Suit.DIAMONDS, 10),
                Card(Name.NINE, Suit.DIAMONDS, 11),
                Card(Name.SEVEN, Suit.DIAMONDS, 12),
            ],
        ]
    )

    wildcard1 = Wild(Name.JOKER, Suit.WILD, 291)
    wildcard1.set_value("SIX")
    wildcard2 = Wild(Name.TWO, Suit.DIAMONDS, 292)
    wildcard2.set_value("KING")
    wildcard3 = Wild(Name.TWO, Suit.DIAMONDS, 293)
    wildcard3.set_value("SIX")
    wildcard4 = Wild(Name.TWO, Suit.DIAMONDS, 294)
    wildcard4.set_value("SEVEN")
    assert game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS, 1),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FIVE, Suit.DIAMONDS, 3),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS, 4),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS, 5),
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
        ]
    )

    # Invalid Hands
    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.SEVEN, Suit.DIAMONDS, 1),
                wildcard1,
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FIVE, Suit.CLUBS, 3),
            ],
            [
                Card(Name.ACE, Suit.DIAMONDS, 4),
                wildcard2,
                Card(Name.JACK, Suit.DIAMONDS, 5),
                Card(Name.QUEEN, Suit.DIAMONDS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                wildcard3,
                wildcard4,
                Card(Name.EIGHT, Suit.DIAMONDS, 8),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FOUR, Suit.DIAMONDS, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 4),
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FOUR, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Card(Name.FIVE, Suit.DIAMONDS, 8),
                Card(Name.SIX, Suit.DIAMONDS, 9),
                Card(Name.SEVEN, Suit.DIAMONDS, 10),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Card(Name.FOUR, Suit.CLUBS, 3),
            ],
            [
                Card(Name.SIX, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 7),
                Wild(Name.JOKER, Suit.WILD, 8),
                Card(Name.FOUR, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Wild(Name.JOKER, Suit.WILD, 1),
                Wild(Name.JOKER, Suit.WILD, 2),
                Wild(Name.JOKER, Suit.WILD, 3),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 4),
                Wild(Name.TWO, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.CLUBS, 6),
            ],
            [
                Card(Name.FIVE, Suit.DIAMONDS, 7),
                Wild(Name.TWO, Suit.DIAMONDS, 8),
                Card(Name.FIVE, Suit.CLUBS, 9),
            ],
        ]
    )

    assert not game_instance.is_valid_play_down(
        [
            [
                Card(Name.FOUR, Suit.DIAMONDS, 1),
                Card(Name.FIVE, Suit.DIAMONDS, 2),
                Card(Name.SIX, Suit.DIAMONDS, 3),
                Card(Name.SEVEN, Suit.DIAMONDS, 4),
            ],
            [
                Card(Name.FOUR, Suit.DIAMONDS, 5),
                Card(Name.FIVE, Suit.DIAMONDS, 6),
                Card(Name.SIX, Suit.DIAMONDS, 7),
                Card(Name.SEVEN, Suit.DIAMONDS, 8),
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
        Card(Name.SEVEN, Suit.DIAMONDS, 1),
        Card(Name.SEVEN, Suit.DIAMONDS, 2),
        Card(Name.SEVEN, Suit.DIAMONDS, 3),
    ]

    set_wild = [
        Wild(Name.JOKER, Suit.WILD, 3),
        Card(Name.SEVEN, Suit.DIAMONDS, 4),
        Card(Name.SEVEN, Suit.DIAMONDS, 5),
    ]

    run = [
        Card(Name.FOUR, Suit.DIAMONDS, 6),
        Card(Name.FIVE, Suit.DIAMONDS, 7),
        Card(Name.SIX, Suit.DIAMONDS, 8),
        Card(Name.SEVEN, Suit.DIAMONDS, 9),
    ]

    wildcard1 = Wild(Name.TWO, Suit.CLUBS, 100)
    wildcard1.set_value("EIGHT")
    run_wild = [
        wildcard1,
        Card(Name.FIVE, Suit.DIAMONDS, 10),
        Card(Name.SIX, Suit.DIAMONDS, 11),
        Card(Name.SEVEN, Suit.DIAMONDS, 12),
    ]

    assert game_instance.is_set(set)
    assert game_instance.is_set(set_wild)
    assert not game_instance.is_set(run)
    assert not game_instance.is_set(run_wild)
