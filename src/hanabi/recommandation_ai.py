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
		game = self.game

		other_hands = self.other_hands  

		self.actions = []



		for i in range(len(other_hands)):

			#Liste des cartes jouables par le joueur i
			self.playable = [(k, card.number) for (k, card)
			in enumerate(self.other_hands.cards)
			if self.list_status[i][k] == 1 ]



			for j in range(len (other_hands[0])):

				card = other_hands[i].cards[j]

				if card.number == 5 and self.list_status[i][j] == 1: # 5 jouable immédiatement
					self.actions.append(j)

				elif self.list_status[i][j] == 0: # Carte inutile de plus petit indice
					self.actions.append(j+3)

				else:
					pass
					








		

		


