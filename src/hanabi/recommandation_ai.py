import hanabi
import numpy as np


class Recommandation(hanabi.ai.AI):
    """Intelligence Artificielle basée sur la stratégie de recommandation.
    """

    def __init__(self, game):
        hanabi.ai.AI.__init__(self, game)

        self.recommendation_list = {}
        self.played_cards = {}

        for player_name in self.game.players:
            self.recommendation_list[player_name] = " "
            self.played_cards[player_name] = 0

    def update_card_status(self):
        """Retourne une table contenant à la case (i,j) le statut de la jème
        carte du ième joueur
        0 : défaussable
        1 : jouable
        2 : indispensable
        3 : non-indispensable
        """

        game = self.game
        status_list = np.zeros((4, 4))
        other_hands = self.other_hands

        for i in range(len(other_hands)):
            # Quand il n'y a plus de cartes dans la pioche, les joueurs n'ont
            # pas forcément le même nombre de cartes
            for j in range(len(other_hands[i])):
                card = other_hands[i].cards[j]

                # La carte peut être posée sur le dessus d'une pile
                if card.number == game.piles[card.color] + 1:
                    status_list[i, j] = 1

                # La carte ne peut plus être posée et peut donc être défaussée
                elif card.number <= game.piles[card.color]:
                    status_list[i, j] = 0

                # La carte est la dernière de son type il faut la conserver
                elif self.is_last_card(card, game.deck, game.discard_pile):
                    status_list[i, j] = 2

                # La carte n'est pas indispensable
                else:
                    status_list[i, j] = 3
        self.list_status = status_list

    def is_last_card(self, card, deck, discard):
        """Retourne True si la carte est la dernière représentante de sa couleur
        et de sa valeur.
        """
        return deck.card_count[card.number] == discard.cards.count(card) + 1

    def other_players_actions(self):
        """Retourne une liste de couples, un pour chaque joueur, comprenant
        l'indice de la carte (en commençant à 0) et une lettre
        déterminant s'il faut la jouer ou la défausser"""

        other_hands = self.other_hands

        self.actions = []

        for i in range(len(other_hands)):
            # Liste des cartes jouables par le joueur i
            playable = []
            for k in range(len(other_hands[i])):
                card = other_hands[i].cards[k]
                if self.list_status[i][k] == 1:
                    playable.append((k, card.number))

            # Donner un indice sur la carte que le joueur devrait jouer
            if playable != []:
                self.hint_play(playable)
            # Donner un indice sur la carte que le joueur devrait défausser
            else:
                self.hint_discard(other_hands[i].cards, self.list_status[i])

    def hint_play(self, cards):
        """Donne un indice sur la carte à jouer suivant une liste de cartes
        """

        j = 0
        was_found = False
        while j < len(cards) and not(was_found):
            card_number = cards[j][1]
            if card_number == 5:
                # Indice de la carte trouvée et lettre déterminant si
                # elle doit être jouée ou défaussée
                self.actions.append((cards[j][0], 'p'))
                was_found = True
            j += 1

            # On a pas trouvé de carte de valeur 5 qui soit jouable
            if not(was_found):
                min_card_number = cards[0][1]
                card_index = cards[0][0]
                for p in range(len(cards)):
                    if cards[p][1] < min_card_number:
                        card_index = cards[p][0]
                was_found = True
                self.actions.append((card_index, 'p'))

    def hint_discard(self, cards, status):
        """Donne un indice sur la carte à défausser suivant une liste de cartes
        et le statut de chaque carte déterminé jusqu'à présent.
        """

        discardable = []  # Liste des cartes défaussables

        for a in range(len(cards)):
            card = cards[a]
            if status[a] == 0:
                discardable.append((a, card.number))

        # Défausser la carte inutile de plus petit indice
        if discardable:
            self.actions.append((discardable[0][0], 'd'))

        else:
            non_indisp = []  # Liste des cartes non indispensables

            for b in range(len(cards)):
                card = cards[b]
                if status[b] == 3:
                    non_indisp.append((b, card.number))

            if non_indisp:
                max_card_number = non_indisp[0][1]
                card_index = non_indisp[0][0]
                for c in range(len(non_indisp)):
                    if non_indisp[c][1] > max_card_number:
                        card_index = non_indisp[c][0]
                # Carte non_indispensable de plus haute valeur
                self.actions.append((card_index, 'd'))

            else:
                # On défausse c1 par défaut
                self.actions.append((0, 'd'))

    def update_recommendations(self, player_name, actions_total, hint_id):
        '''Met à jour les recommandations pour chaque joueur'''

        current_player_index = self.game.players.index(player_name)

        for j in range(4):
            player = self.game.players[(current_player_index + j + 1) % 5]

            if self.actions[j][1] == 'p':
                sum_actions = actions_total - self.actions[j][0]
            else:
                sum_actions = actions_total - (self.actions[j][0] + 4)

            sum_actions = sum_actions % 8
            recommandation_id = ((hint_id - sum_actions) % 8)
            recommandation_action = 'p' if recommandation_id <= 3 else 'd'
            recommandation = recommandation_action + str(recommandation_id % 4)

            self.recommendation_list[player] = recommandation
            self.played_cards[player] = 0

    def give_hint(self, current_player_name):
        '''Donne un indice suivant les règles établies par la stratégie'''
        s = 0
        for i in range(len(self.actions)):
            # S'il faut jouer la carte, le numéro de l'action correspond à
            # l'indice de la carte
            if self.actions[i][1] == 'p':
                s += self.actions[i][0]

            # S'il faut défausser une carte, il faut ajouter 4 à l'indice
            # de la carte en question
            else:
                s += self.actions[i][0] + 4

        # Numéro donnant le joueur concerné par l'indice, ainsi que le type
        # de ce dernier (couleur ou valeur)
        t = s % 8

        # Il s'agit d'un indice de valeur
        if t <= 3:
            first_card = self.other_hands[t].cards[0]
            res = 'c' + str(first_card.number) + str(t + 1)
            for card in self.other_hands[t].cards:
                if not card.number_clue:
                    clue = card.number
                    res = 'c' + str(clue) + str(t + 1)
        else:
            first_card = self.other_hands[t-4].cards[0]
            res = 'c' + str(first_card.number) + str(t - 3)
            for card in self.other_hands[t-4].cards:
                if not card.color_clue:
                    clue = card.color
                    res = 'c' + str(clue)[0] + str(t - 3)

        self.update_recommendations(current_player_name, s, t)
        return res

    def play(self):
        game = self.game
        self.update_card_status()
        self.other_players_actions()

        current_player_name = game.current_player_name[4:-4]
        recommendation = self.recommendation_list[current_player_name]
        played_cards = self.played_cards[current_player_name]

        allow_error = game.red_coins <= 1 and played_cards == 1

        reset_recommendation = True

        # jouer une carte est recommandé et possible
        if recommendation[0] == 'p' and (played_cards == 0 or allow_error):
            card_to_play = int(recommendation[1]) + 1

            for player_name in game.players:
                if player_name != current_player_name:
                    self.played_cards[player_name] += 1

            action = "p" + str(card_to_play)
        elif game.blue_coins != 0:
            action = self.give_hint(current_player_name)
        elif self.recommendation_list[current_player_name][0] == 'd':
            action = "d" + str(int(recommendation[1]) + 1)
            self.recommendation_list[current_player_name] = " "
        else:
            reset_recommendation = False
            action = "d1"

        if reset_recommendation:
            self.recommendation_list[current_player_name] = " "

        return action
