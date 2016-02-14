from unittest import TestCase
from deck import Card
from deck import suits_trump_first


class TestCards(TestCase):

    def test_cards_are_equal_if_same_suit_and_position(self):
        self.assertEqual(
            Card(suit='Hearts', position='Jack'),
            Card(suit='Hearts', position='Jack')
        )

    def test_cards_not_equal_if_suit_and_position_differ(self):
        self.assertNotEqual(
            Card(suit='Diamonds', position='Jack'),
            Card(suit='Hearts', position='Jack')
        )

    def test_non_left_bauer_false(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertFalse(
            card.is_same_suit(suit='Diamonds', trump='Spades')
        )

    def test_left_bauer_true(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertTrue(
            card.is_same_suit(suit='Diamonds', trump='Diamonds')
        )

    def test_same_suit_true(self):
        card = Card(suit='Hearts', position='9')
        self.assertTrue(
            card.is_same_suit(suit='Hearts', trump='Spades')
        )


class Test_effective_suit(TestCase):

    def test_left_bauer_returns_trump_suit(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertEqual(
            'Diamonds',
            card.effective_suit(trump='Diamonds')
        )

    def test_non_left_bauer_returns_own_suit(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertEqual(
            'Hearts',
            card.effective_suit(trump='Spades')
        )


class TestCardsBauers(TestCase):

    def test_is_right_bauer_returns_false_if_no_trump(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertFalse(card.is_right_bauer())

    def test_is_right_bauer_returns_true_if_jack_and_trump(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertTrue(card.is_right_bauer(trump='Hearts'))

    def test_is_right_bauer_returns_false_if_non_trump_jack(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertFalse(card.is_right_bauer('Diamonds'))

    def test_is_right_bauer_returns_false_if_not_jack(self):
        card = Card(suit='Hearts', position='King')
        self.assertFalse(card.is_right_bauer('Hearts'))

    def test_is_left_bauer_returns_false_if_no_trump(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertFalse(card.is_left_bauer())

    def test_is_left_bauer_returns_true_if_jack_and_same_color(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertTrue(card.is_left_bauer(trump='Diamonds'))

    def test_is_left_bauer_returns_false_if_trump_jack(self):
        card = Card(suit='Hearts', position='Jack')
        self.assertFalse(card.is_left_bauer('Hearts'))

    def test_is_left_bauer_returns_false_if_not_jack(self):
        card = Card(suit='Hearts', position='King')
        self.assertFalse(card.is_left_bauer('Diamonds'))


class Testsuits_trump_first(TestCase):

    def test_no_trump_returns_default_order(self):
        order = suits_trump_first()
        self.assertEqual(
            ['Hearts', 'Spades', 'Diamonds', 'Clubs'],
            order
        )

    def test_hearts_as_trump(self):
        order = suits_trump_first('Hearts')
        self.assertEqual(
            ['Hearts', 'Spades', 'Diamonds', 'Clubs'],
            order
        )

    def test_clubs_as_trump(self):
        order = suits_trump_first('Clubs')
        self.assertEqual(
            ['Clubs', 'Hearts', 'Spades', 'Diamonds'],
            order
        )
