import game


def test_is_valid_set():

    # Four, Four, Four -> True because there are three fours
    play0 = [
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.CLUBS),
    ]

    # Ace, Two, Ace -> True because two is wild
    play1 = [
        game.Card(game.Name.ACE, game.Suit.DIAMONDS),
        game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
        game.Card(game.Name.ACE, game.Suit.CLUBS),
    ]

    # Joker, King, King -> True because Joker is wild
    play2 = [
        game.Wild(game.Name.JOKER, game.Suit.WILD),
        game.Card(game.Name.KING, game.Suit.DIAMONDS),
        game.Card(game.Name.KING, game.Suit.CLUBS),
    ]

    # Ace, Two, Three -> False because Ace and Three are not of the same Set
    invalid_play0 = [
        game.Card(game.Name.ACE, game.Suit.DIAMONDS),
        game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
        game.Card(game.Name.THREE, game.Suit.CLUBS),
    ]

    # Joker, Two, Two -> False because there is no non-wild card
    invalid_play1 = [
        game.Wild(game.Name.JOKER, game.Suit.WILD),
        game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
        game.Wild(game.Name.TWO, game.Suit.CLUBS),
    ]

    # Six, Nine, Eight -> False because all different cards
    invalid_play2 = [
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
        game.Card(game.Name.NINE, game.Suit.DIAMONDS),
        game.Card(game.Name.EIGHT, game.Suit.CLUBS),
    ]

    # Jack -> False because not enough cards for a set
    invalid_one_card = [game.Card(game.Name.JACK, game.Suit.SPADES)]

    # Six, Six, Six, Six -> False because too many cards for a set
    invalid_four_card = [
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.CLUBS),
        game.Card(game.Name.SIX, game.Suit.SPADES),
    ]

    # None -> False because no cards silly!
    invalid_no_card = []

    game_instance = game.Game()

    # Valid Sets
    assert game_instance.is_valid_set(play0) == True
    assert game_instance.is_valid_set(play1) == True
    assert game_instance.is_valid_set(play2) == True

    # Invalid Sets
    assert game_instance.is_valid_set(invalid_play0) == False
    assert game_instance.is_valid_set(invalid_play1) == False
    assert game_instance.is_valid_set(invalid_play2) == False
    assert game_instance.is_valid_set(invalid_one_card) == False
    assert game_instance.is_valid_set(invalid_four_card) == False
    assert game_instance.is_valid_set(invalid_no_card) == False


def test_is_valid_run():

    # Valid runs
    # Three, Four, Five, Six, Seven of diamonds run
    play0 = [
        game.Card(game.Name.THREE, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        game.Card(game.Name.TEN, game.Suit.CLUBS),
        game.Card(game.Name.JACK, game.Suit.CLUBS),
        game.Card(game.Name.KING, game.Suit.CLUBS),
        game.Card(game.Name.QUEEN, game.Suit.CLUBS),
    ]

    wildcard1 = game.Wild(game.Name.TWO, game.Suit.CLUBS)
    wildcard1.set_value("EIGHT")
    wildcard2 = game.Wild(game.Name.JOKER, game.Suit.WILD)
    wildcard2.set_value("NINE")

    # Wild, Wild, Ten, Jack of Hearts run, it is valid because the wilds were given their temporary values before hand
    play2 = [
        wildcard1,
        wildcard2,
        game.Card(game.Name.TEN, game.Suit.HEARTS),
        game.Card(game.Name.JACK, game.Suit.HEARTS),
    ]

    wildcard1.set_value("NINE")
    wildcard2.set_value("QUEEN")
    # Ten, Wild , Jack, Wild of Diamonds run, it is valid because wilds are given temporary values before hand
    # and sorted before validation
    play3 = [
        game.Card(game.Name.TEN, game.Suit.HEARTS),
        wildcard2,
        game.Card(game.Name.JACK, game.Suit.HEARTS),
        wildcard1,
    ]

    # Invalid runs
    # Cards are not in sequence
    invalid_play0 = [
        game.Card(game.Name.THREE, game.Suit.DIAMONDS),
        game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
        game.Card(game.Name.SEVEN, game.Suit.DIAMONDS),
    ]

    # Cards are not of the same suit
    invalid_play1 = [
        game.Card(game.Name.THREE, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.CLUBS),
        game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.HEARTS),
    ]

    # Wildcards are not assigned temporary values
    invalid_play2 = [
        game.Wild(game.Name.TWO, game.Suit.CLUBS),
        game.Wild(game.Name.JOKER, game.Suit.WILD),
        game.Card(game.Name.THREE, game.Suit.CLUBS),
        game.Card(game.Name.FOUR, game.Suit.CLUBS),
    ]

    # Duplicates in the run
    invalid_play3 = [
        game.Card(game.Name.SEVEN, game.Suit.DIAMONDS),
        game.Card(game.Name.SEVEN, game.Suit.DIAMONDS),
        game.Card(game.Name.EIGHT, game.Suit.DIAMONDS),
        game.Card(game.Name.NINE, game.Suit.DIAMONDS),
    ]

    # Too many cards in the run
    invalid_play4 = [
        game.Card(game.Name.SIX, game.Suit.CLUBS),
        game.Card(game.Name.FIVE, game.Suit.CLUBS),
        game.Card(game.Name.THREE, game.Suit.CLUBS),
        game.Card(game.Name.FOUR, game.Suit.CLUBS),
        game.Card(game.Name.SEVEN, game.Suit.CLUBS),
    ]

    # Not enough cards in the run
    invalid_play5 = [
        game.Card(game.Name.SEVEN, game.Suit.DIAMONDS),
        game.Card(game.Name.EIGHT, game.Suit.DIAMONDS),
        game.Card(game.Name.NINE, game.Suit.DIAMONDS),
    ]
    invalid_play6 = [
        wildcard1,
        wildcard2,
        wildcard2,
        wildcard2,
    ]

    game_instance = game.Game()

    # Valid runs
    assert game_instance.is_valid_run(play0) == True
    assert game_instance.is_valid_run(play1) == True
    assert game_instance.is_valid_run(play2) == True
    assert game_instance.is_valid_run(play3) == True

    # Invalid runs
    assert game_instance.is_valid_run(invalid_play0) == False
    assert game_instance.is_valid_run(invalid_play1) == False
    assert game_instance.is_valid_run(invalid_play2) == False
    assert game_instance.is_valid_run(invalid_play3) == False
    assert game_instance.is_valid_run(invalid_play4) == False
    assert game_instance.is_valid_run(invalid_play5) == False
    assert game_instance.is_valid_run(invalid_play6) == False


def test_is_valid_runRound7():
    """Tests runs when game round is 7. Runs can be longer than 4"""

    # Valid runs
    wildcard1 = game.Wild(game.Name.TWO, game.Suit.CLUBS)
    wildcard1.set_value("JACK")
    wildcard2 = game.Wild(game.Name.JOKER, game.Suit.WILD)
    wildcard2.set_value("QUEEN")

    play0 = [
        game.Card(game.Name.THREE, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
        game.Card(game.Name.SIX, game.Suit.DIAMONDS),
        game.Card(game.Name.SEVEN, game.Suit.DIAMONDS),
        game.Card(game.Name.EIGHT, game.Suit.DIAMONDS),
        game.Card(game.Name.NINE, game.Suit.DIAMONDS),
        game.Card(game.Name.TEN, game.Suit.DIAMONDS),
        game.Card(game.Name.KING, game.Suit.DIAMONDS),
        game.Card(game.Name.ACE, game.Suit.DIAMONDS),
        wildcard1,
        wildcard2,
    ]

    # Ten, Jack, King, Queen of clubs run, it is valid but out of order and works
    play1 = [
        game.Card(game.Name.TEN, game.Suit.CLUBS),
        game.Card(game.Name.JACK, game.Suit.CLUBS),
        game.Card(game.Name.KING, game.Suit.CLUBS),
        game.Card(game.Name.QUEEN, game.Suit.CLUBS),
        game.Card(game.Name.ACE, game.Suit.CLUBS),
    ]

    game_instance = game.Game()
    game_instance.round = 7

    # Valid runs
    assert game_instance.is_valid_run(play0) == True
    assert game_instance.is_valid_run(play1) == True


def test_determine_winner():
    """Tests if Winner is determined correctly"""
    players = [game.Player("Nestor"), game.Player("Jacob"), game.Player("Summer")]

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
    players = [game.Player("Nestor")]
    game_instance.players = players
    assert game_instance.determine_winner()[0].name == "Nestor"


def test_round_1():
    game_instance = game.Game()
    game_instance.round = 1

    # Valid Hands
    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
                [
                    game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
                    game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
                    game.Card(game.Name.FIVE, game.Suit.CLUBS),
                ],
            ]
        )
        == True
    )

    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Wild(game.Name.JOKER, game.Suit.WILD),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
                [
                    game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
                    game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
                    game.Card(game.Name.FIVE, game.Suit.CLUBS),
                ],
            ]
        )
        == True
    )

    # Invalid Hands
    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
            ]
        )
        == False
    )

    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
            ]
        )
        == False
    )

    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
                    game.Wild(game.Name.JOKER, game.Suit.WILD),
                    game.Card(game.Name.FOUR, game.Suit.CLUBS),
                ],
                [
                    game.Card(game.Name.SIX, game.Suit.DIAMONDS),
                    game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
                    game.Card(game.Name.FIVE, game.Suit.CLUBS),
                ],
            ]
        )
        == False
    )

    assert (
        game_instance.is_valid_play_down(
            [
                [
                    game.Wild(game.Name.JOKER, game.Suit.WILD),
                    game.Wild(game.Name.JOKER, game.Suit.WILD),
                    game.Wild(game.Name.JOKER, game.Suit.WILD),
                ],
                [
                    game.Card(game.Name.FIVE, game.Suit.DIAMONDS),
                    game.Wild(game.Name.TWO, game.Suit.DIAMONDS),
                    game.Card(game.Name.FIVE, game.Suit.CLUBS),
                ],
            ]
        )
        == False
    )


def test_round_2():
    pass


def test_round_3():
    pass


def test_round_4():
    pass


def test_round_5():
    pass


def test_round_6():
    pass


def test_round_7():
    pass
