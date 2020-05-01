import hanabi
import numpy as np

class Recommandation(hanabi.ai.AI):

	def card_status(self):
		game = self.game

		self.list_status = np.zeros((4, 4)) #Liste qui va contenir à l'indice i, j le statut de la jème carte du ième joueur

		"""0 : défaussable
		   1 : jouable
		   2 : indispensable
		   3 : non-indispensable"""

		other_hands = self.other_hands  

		for i in range(len(other_hands)):
			for j in range(len(other_hands[0])):


				card = other_hands[i].cards[j]

				if card.number == game.piles[card.color] + 1: #La carte peut être posée sur le dessus d'une pile
					self.list_status[i, j] = 1

				elif card.number <= game.piles[card.color]:  #La carte ne peut plus être posée et peut donc être défaussée
					self.list_status[i, j] = 0

				elif game.deck.card_count[card.number] == game.discard_pile.cards.count(card) + 1: 
					#La carte est la dernière de son type (les autres ont été défaussées), il faut donc absolument la conserver
					self.list_status[i, j] = 2

				else:  #La carte est non-indispensable
					self.list_status[i, j] = 3


	def other_players_actions(self):

		#Retourne une liste de couples, un pour chaque joueur, comprenant l'indice de la carte (en commençant à 0) et une lettre 
		#déterminant s'il faut la jouer ou la défausser
		
		game = self.game

		other_hands = self.other_hands  

		self.actions = []



		for i in range(len(other_hands)):

			#Liste des cartes jouables par le joueur i
			playable = []
			for k in range(len(other_hands[0])):
				card = other_hands[i].cards[k]
				if self.list_status[i][k] == 1 :
					playable.append((k, card.number))

		
			(j, l) = (0, 0)


			if playable :

				
				while j < len(playable) and l == 0:
					card_number = playable[j][1]
					if card_number == 5 :
						self.actions.append((playable[j][0], 'p')) #Indice de la carte trouvée et lettre déterminant si elle doit être jouée ou défaussée
						l = 1
					j += 1


				if l == 0: #On a pas trouvé de carte de valeur 5 qui soit jouable
					max_card_number = playable[0][1]
					card_index = playable[0][0]
					for p in range(len(playable)):
						if playable[p][1] > max_card_number:
							card_index = playable[p][0]
					l = 1
					self.actions.append((card_index, 'p'))

			else :

				discardable = [] #Liste des cartes défaussables

				for a in range(len(other_hands[0])):
					card = other_hands[i].cards[a]
					if self.list_status[i][a] == 0:
						discardable.append((a, card.number))

				if discardable :
					self.actions.append((discardable[0][0], 'd')) #Défausser la carte inutile de plus petit indice

				else :

					non_indisp = [] #Liste des cartes non-indispensables

					for b in range(len(other_hands[0])):
						card = other_hands[i].cards[b]
						if self.list_status[i][b] == 3:
							non_indisp.append((b, card.number))

					if non_indisp :
						max_card_number = non_indisp[0][1]
						card_index = non_indisp[0][0]
						for c in range(len(non_indisp)):
							if non_indisp[c][1] > max_card_number :
								card_index = non_indisp[c][0]
						self.actions.append((card_index, 'd')) #Carte non_indispensable de plus haute valeur

					else :
						self.actions.append((0, 'd'))  #Aucune carte n'a vérifié les conditions, on défausse c1 par défaut


	def play(self) :

		game = self.game
		self.card_status()
		self.other_players_actions()

		

				














		

		


