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
        game.Card(game.Name.JOKER, game.Suit.JOKER),
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
