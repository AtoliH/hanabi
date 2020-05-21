import unittest
import hanabi
from hanabi.recommandation_ai import Recommandation as AI
from hanabi.deck import Color, Card, Hand, Deck


class TestRecommendationStrategy(unittest.TestCase):

    def test_hint(self):
        def test_action(ai, action, piles, cards):
            dummy_hand = Hand(Deck([Card(Color.White, 1)]*4), 4)
            ai.game.hands = [dummy_hand, Hand(Deck(cards), 4)]
            ai.game.piles = piles

            ai.update_card_status()
            ai.other_players_actions()

            self.assertEqual(ai.actions[0], action)

        game = hanabi.Game(players=5)
        ai = AI(game)

        # Play
        piles = {
            Color.White: 4,
            Color.Red: 0,
            Color.Blue: 0,
            Color.Green: 0,
            Color.Yellow: 0
        }

        # Jouer une carte de rang 5 quand on le peut
        test_action(ai, (2, 'p'), piles, [
            Card(Color.White, 1),
            Card(Color.White, 1),
            Card(Color.White, 5),
            Card(Color.Blue, 1)
        ])

        # Jouer la carte de rang 5 jouable de plus petit indice
        piles[Color.Blue] = 4

        test_action(ai, (0, 'p'), piles, [
            Card(Color.Blue, 5),
            Card(Color.White, 5),
            Card(Color.White, 1),
            Card(Color.Blue, 1)
        ])

        # Jouer la carte jouable de plus grande valeur, puis de plus petit
        # indice
        piles[Color.White] = 3

        test_action(ai, (1, 'p'), piles, [
            Card(Color.Red, 1),
            Card(Color.White, 4),
            Card(Color.Blue, 1),
            Card(Color.Green, 1)
        ])

        # Discard
        piles = {
            Color.White: 1,
            Color.Red: 1,
            Color.Blue: 1,
            Color.Green: 1,
            Color.Yellow: 1
        }

        # Défausse de la carte de plus petit indice quand on ne peut rien jouer
        test_action(ai, (0, 'd'), piles, [
            Card(Color.White, 1),
            Card(Color.Red, 1),
            Card(Color.Blue, 1),
            Card(Color.Green, 1)
        ])

        # Donner la priorité à la défausse de carte inutiles
        test_action(ai, (3, 'd'), piles, [
            Card(Color.White, 3),
            Card(Color.Green, 3),
            Card(Color.Blue, 3),
            Card(Color.White, 1)
        ])

        # Ne pas défausser les cartes indispensables (il n'y a qu'un seul 5 par
        # exemple)
        test_action(ai, (1, 'd'), piles, [
            Card(Color.White, 5),
            Card(Color.Red, 3),
            Card(Color.Blue, 3),
            Card(Color.Green, 3)
        ])

        # Défausser la carte non indispensable de plus petit indice
        test_action(ai, (0, 'd'), piles, [
            Card(Color.Red, 3),
            Card(Color.Blue, 3),
            Card(Color.Green, 3),
            Card(Color.White, 3)
        ])

        # L'action par défaut est la défausse de la première carte
        test_action(ai, (0, 'd'), piles, [
            Card(Color.Red, 5),
            Card(Color.White, 5),
            Card(Color.Blue, 5),
            Card(Color.Green, 5)
        ])


if __name__ == '__main__':
    unittest.main()
