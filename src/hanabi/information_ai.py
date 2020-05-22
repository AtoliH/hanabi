import hanabi
from hanabi.deck import Color, Card
import numpy as np


class InformationAi(hanabi.ai.AI):



    def __init__(self, game):
        hanabi.ai.AI.__init__(self, game)

        self.tables = {}


        for player_name in game.players :  #Création d'une table par joueur
            self.tables[player_name] = np.ones((4, 5, 5))

        self.colors = {}
        self.colors[Color.Blue] = 0
        self.colors[Color.Green] = 1
        self.colors[Color.Red] = 2
        self.colors[Color.White] = 3
        self.colors[Color.Yellow] = 4






    def card_status(self, card):
        game = self.game

        # self.list_status = np.zeros((4, 4)) #Liste qui va contenir à l'indice i, j le statut de la jème carte du ième joueur

        """0 : défaussable
           1 : jouable
           2 : indispensable
           3 : non-indispensable"""


        if card.number == game.piles[card.color] + 1: #La carte peut être posée sur le dessus d'une pile
            # self.list_status[i, j] = 1
            return(1)

        elif card.number <= game.piles[card.color]:  #La carte ne peut plus être posée et peut donc être défaussée
            # self.list_status[i, j] = 0
            return(0)

        elif game.deck.card_count[card.number] == game.discard_pile.cards.count(card) + 1:
            #La carte est la dernière de son type (les autres ont été défaussées), il faut donc absolument la conserver
            # self.list_status[i, j] = 2
            return(2)

        else:  #La carte est non-indispensable
            # self.list_status[i, j] = 3
            return(3)



    def deduce(self, card_table):

        """ Mise à jour des informations privées en voyant les mains des autres joueurs"""

        self.game = game
        other_hands = self.other_players_cards
        # (sum_blue, sum_green, sum_red, sum_white, sum_yellow) = (0, 0, 0, 0, 0)
        number_card_color = 10

        sum_card_color = {Color.Blue : 0, Color.Green : 0, Color.Red : 0, Color.White : 0, Color.Yellow : 0}
        sum_card_number = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}



        for card in other_hands:

            if game.deck.card_count[card.number] == game.discard_pile.cards.count(card) + other_hands.count(card):
                card_table[card.color][card.number] = False

            sum_card_color[card.color] += 1
            sum_card_number[card.number] += 1



        for card in game.discard_pile.cards :

            sum_card_color[card.color] += 1
            sum_card_number[card.number] += 1


        for color in sum_card_color:

            sum_card_color[color] += game.piles[color]

            if sum_card[color] == number_card_color:
                card_table[color] = 5*[False]

            for number in sum_card_number:
                if game.piles[color] >= number:
                    sum_card_number[number] += 1

                if sum_card_number[number] == game.deck.card_count[number] :
                    for k in range(card_table):
                        card_table[k][number] = 5*[False]




    def targeted_card(self, player, position) :
        '''Retourne l'indice de la carte du joueur qui a la plus grande probabilité d'être jouable'''

        player_table = self.tables[player]
        n = len(self.other_hands[position])
        prob=[]

        for i in range(n):
            num_possible = self.count_possibilities(player_table[i])
            prob.append(self.num_status_card(player_table[i], 1) / num_possible)

        best_playable_card = prob.index(max(prob))
        return(best_playable_card)


    def count_possibilities(self, table) :
        '''Retourne le nombre de possibilités pour une carte, à partir de sa table'''

        # n = len(table)
        # s = 0

        # for i in range(n):
        #     for color in self.colors:
        #         if table[self.colors[color]][i] == 1:
        #             s += 1

        return(int(np.sum(table)))

    def num_status_card(self, table, status):
        '''Retourne le nombre de possibilités qui ont le statut status (en l'occurence 1 pour jouable, 0 pour morte)'''

        n = len(table)
        num_status = 0

        for i in range(n):
            for color in self.colors :
                    if table[self.colors[color]][i] == 1:

                        card = Card(color, i+1)
                        if self.card_status(card) == status:
                             num_status += 1

        return(num_status)




    def partition_table(self, table) :
        '''Retourne un tableau contenant la partition de la table'''


        num_dead = self.num_status_card(table, 0)  #Nombre de possibilités qui correspondent à des cartes mortes
        num_possibilities = self.count_possibilities(table) #Nombre de possibilités pour la carte considérée
        partition = np.zeros((5, 5))

        for i in range(len(table)):
            for k in range(len(table)):

                if table[i][k]:
                    partition[i][k] = table[i][k]
                else :
                    partition[i][k] = 9




        num_dead_sets = 0
        if num_dead > 0:
            num_dead_sets = 1

        #Calcul du nombre de singletons qu'on peut réaliser
        num_singletons = 8
        while (num_possibilities - num_dead - num_singletons) - 8 * (8 - num_dead_sets - num_singletons) > 0:
            num_singletons -= 1

        self.singletons = num_singletons




        remaining_hint_sets = 8 - num_singletons - num_dead_sets  #Nombre de sets de cartes utilisables (donc pas mortes) contenant plusieurs cartes


        self.rest = remaining_hint_sets

        hint_set = 0
        hint_dead_cards = 0
        first_dead_card = True
        j = 0

        for i in range(len(table)):  #On parcourt la table en colonnes (et pas en lignes)
            for color in self.colors:

                self.hint = hint_set

                if partition[self.colors[color]][i] == 1:
                    card = Card(color, i+1)

                    status = self.card_status(card)


                    if status == 0 : #Détection d'une carte morte
                        if first_dead_card: #Détection de la première carte morte
                            first_dead_card = False
                            hint_dead_cards = hint_set
                            hint_set += 1

                        partition[self.colors[color]][i] = hint_dead_cards #Toutes les cartes mortes portent le même numéro d'indice


                    else :
                        if hint_set <= num_singletons:
                            partition[self.colors[color]][i] = hint_set
                            hint_set += 1

                        else :
                            partition[self.colors[color]][i] = hint_set
                            j += 1

                            if j % 8 == 0 :
                                hint_set += 1  # Hors des singletons, les sets contiennent huuit cartes, et le dernier complète la table.
        return(partition)



    def give_hint(self):
        '''Retourne l'indice selon la stratégie de l'information et met à jour les tables des autres joueurs'''

        other_hands = self.other_hands
        game = self.game

        current_player_name = game.current_player_name[4:-4]
        current_player_index = game.players.index(current_player_name)

        hand_values = []
        list_targeted_cards = [] # Liste qui va contenir l'indice de chaque carte ciblée pour chaque joueur
        s = 0

        for j in range(4):

            player = game.players[(current_player_index + j + 1) % 5]
            list_targeted_cards.append(self.targeted_card(player, j))

            card = other_hands[j].cards[list_targeted_cards[j]]  # Carte ciblée dans la main du joueur j

            self.target = list_targeted_cards

            partition = self.partition_table(self.tables[player][list_targeted_cards[j]]) # Partition de la table de la carte ciblée

            hand_values.append(partition[self.colors[card.color]][card.number - 1]) # Valeur qui a été attribuée par la partition à la carte ciblée
            s += hand_values[j]

        t = s % 8

        t = int(t)

        if t <= 3:  # Il s'agit d'un indice de valeur
                first_card = self.other_hands[t].cards[0]
                res = 'c' + str(first_card.number) + str(t + 1)
                for card in self.other_hands[t].cards :
                    if not card.number_clue:
                        clue = card.number
                        res = 'c' + str(clue) + str(t + 1)


        else: # Indice de couleur
            first_card = self.other_hands[t-4].cards[0]
            res = 'c' + str(first_card.number) + str(t - 3)
            for card in self.other_hands[t-4].cards:
                if not card.color_clue:
                    clue = card.color
                    res = 'c' + str(clue)[0] + str(t - 3)



        #Mise à jour des tables de possibilités

        self.hints = [False, False, False, False]

        for i in range(4):

            player = game.players[(current_player_index + i + 1) % 5] # Nom du joueur situé à la position i par rapport au joueur courant

            sum_actions = (s - hand_values[i]) % 8
            hint = (t - sum_actions) % 8

            partition = self.partition_table(self.tables[player][list_targeted_cards[i]])

            # card = other_hands[i].cards[list_targeted_cards[i]]
            # hint_cheat = partition[self.colors[card.color]][card.number - 1]

            if hint in partition :
                self.hints[i] = True


            for k in range(len(partition)):
                for l in range(len(partition)):


                    if int(partition[k][l]) != hint:
                        self.tables[player][list_targeted_cards[i]][k][l] = 0 #Toutes les cartes qui ne sont pas dans le set visé ne sont plus possibles


        return(res)


    def play(self):
        '''Méthode globale pour faire jouer le robot'''

        game = self.game
        current_player_name = game.current_player_name[4:-4]
        table = self.tables[current_player_name]

        playable_found = False
        dead_found = False
        dispensable_found = False
        duplicate_found = False

        print(table)

        for i in range(len(table)):
            playable = True
            dead = True
            dispensable = True
            duplicate = True
            for color in self.colors:
                for k in range(len(table[0])):

                    if table[i][self.colors[color]][k] == 1:

                        card = Card(color, k+1)

                        if self.card_status(card) != 1:
                            playable = False  # Il existe une possibilité de la carte i qui n'est pas jouable

                        if self.card_status(card) != 0:
                            dead = False

                        if self.card_status(card) != 3 :
                            dispensable = False

                        if card not in self.other_players_cards :
                            duplicate = False



            if playable and not playable_found :
                index_playable = i
                playable_found = True

            if dead and not dead_found:
                index_dead = i
                dead_found = True

            if dispensable and not dispensable_found :
                index_dispensable = i
                dispensable_found = True

            if duplicate and not duplicate_found :
                index_duplicate = i
                duplicate_found = True




        if playable_found :
            index = index_playable
            action = "p" + str(index_playable + 1)

        elif dead_found and len(game.discard_pile) <= 5 :
            index = index_dead
            action = "d" + str(index_dead + 1)

        elif game.blue_coins != 0 :
            hint = self.give_hint()
            action = hint

        elif dead_found :
            index = index_dead
            action = "d" + str(index_dead + 1)

        elif duplicate_found :
            index = index_duplicate
            action = "d" + str(index_duplicate + 1)

        elif dispensable_found :
            index = index_dispensable
            action = "d" + str(index_dispensable + 1)

        else :
            index = 0
            action = "d1"


        new_table = np.ones((4, 5, 5))

        if action[0] != 'c' :

            for a in range(3):

                if a < index :
                    new_table[a] = self.tables[current_player_name][a]
                else :
                    new_table[a] = self.tables[current_player_name][a + 1]

            self.tables[current_player_name] = new_table.copy()


        return(action)









