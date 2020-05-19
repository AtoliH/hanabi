import hanabi
from hanabi.deck import Color, Card


class InformationAi(hanabi.ai.AI):

    

    def __init__(self, game):
        hanabi.ai.AI.__init__(self, game)

        self.tables = {}

        for player_name in game.players :  #Création d'une table par joueur
            self.tables[player_name] = 5*[5*[5*[True]]]

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


    
    def count(self, liste, param):
        s = 0

        for i in range(len(liste)):
            for j in range (len(liste[0])):
                if liste[i][j] == param :
                    s += 1

        return(s)




    def targeted_card(self, player_table) :
        '''Retourne l'indice de la carte du joueur qui a la plus grande probabilité d'être jouable'''

        n = len(player_table)
        num_playable = 0
        num_possible = count(self, player_table, True)
        prob=[]

        for i in range(n):
            for color in self.colors :
                for j in range(5) :
                    if player_table[i][color][j]:

                        card = Card(color, j+1)
                        if card_status(self, card) == 1:
                             num_playable += 1

            prob.append(num_playable/num_possible)

            best_playable_card = prob.index(max(prob))
            return(best_playable_card)



    def partition_table(self, table) :
        


















            









        
