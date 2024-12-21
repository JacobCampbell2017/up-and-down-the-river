import game


def test_isValidSet():

    # Four, Four, Four -> True because there are three fours
    play0 = [
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.DIAMONDS),
        game.Card(game.Name.FOUR, game.Suit.CLUBS),
    ]

    # Ace, Two, Ace -> True because two is wild
    play1 = [
        game.Card(game.Name.ACE, game.Suit.DIAMONDS),
        game.Card(game.Name.TWO, game.Suit.DIAMONDS),
        game.Card(game.Name.ACE, game.Suit.CLUBS),
    ]

    # Joker, King, King -> True because Joker is wild
    play2 = [
        game.Card(game.Name.JOKER, game.Suit.WILD),
        game.Card(game.Name.KING, game.Suit.DIAMONDS),
        game.Card(game.Name.KING, game.Suit.CLUBS),
    ]

    # Ace, Two, Three -> False because Ace and Three are not of the same Set
    invalid_play0 = [
        game.Card(game.Name.ACE, game.Suit.DIAMONDS),
        game.Card(game.Name.TWO, game.Suit.DIAMONDS),
        game.Card(game.Name.THREE, game.Suit.CLUBS),
    ]

    # Joker, Two, Two -> False because there is no non-wild card
    invalid_play1 = [
        game.Card(game.Name.JOKER, game.Suit.DIAMONDS),
        game.Card(game.Name.TWO, game.Suit.DIAMONDS),
        game.Card(game.Name.TWO, game.Suit.CLUBS),
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
    assert game_instance.isValidSet(play0) == True
    assert game_instance.isValidSet(play1) == True
    assert game_instance.isValidSet(play2) == True

    # Invalid Sets
    assert game_instance.isValidSet(invalid_play0) == False
    assert game_instance.isValidSet(invalid_play1) == False
    assert game_instance.isValidSet(invalid_play2) == False
    assert game_instance.isValidSet(invalid_one_card) == False
    assert game_instance.isValidSet(invalid_four_card) == False
    assert game_instance.isValidSet(invalid_no_card) == False


def test_isValidRun():

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
    wildcard1.change_value("EIGHT")
    wildcard2 = game.Wild(game.Name.JOKER, game.Suit.WILD)
    wildcard2.change_value("NINE")

    # Wild, Wild, Ten, Jack of Hearts run, it is valid because the wilds were given their temporary values before hand
    play2 = [
        wildcard1,
        wildcard2,
        game.Card(game.Name.TEN, game.Suit.HEARTS),
        game.Card(game.Name.JACK, game.Suit.HEARTS),
    ]

    wildcard1.change_value("NINE")
    wildcard2.change_value("QUEEN")
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
    assert game_instance.isValidRun(play0) == True
    assert game_instance.isValidRun(play1) == True
    assert game_instance.isValidRun(play2) == True
    assert game_instance.isValidRun(play3) == True

    # Invalid runs
    assert game_instance.isValidRun(invalid_play0) == False
    assert game_instance.isValidRun(invalid_play1) == False
    assert game_instance.isValidRun(invalid_play2) == False
    assert game_instance.isValidRun(invalid_play3) == False
    assert game_instance.isValidRun(invalid_play4) == False
    assert game_instance.isValidRun(invalid_play5) == False
    assert game_instance.isValidRun(invalid_play6) == False
