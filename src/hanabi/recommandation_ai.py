import hanabi
import numpy as np

class Recommandation(hanabi.ai.AI):


	def __init__(self, game):
		hanabi.ai.AI.__init__(self, game)

		self.recommandation_list = {}
		self.played_cards = {}

		for player_name in self.game.players :
			self.recommandation_list[player_name] = " "
			self.played_cards[player_name] = 0





	def card_status(self):
		game = self.game

		self.list_status = np.zeros((4, 4)) #Liste qui va contenir à l'indice i, j le statut de la jème carte du ième joueur

		"""0 : défaussable
		   1 : jouable
		   2 : indispensable
		   3 : non-indispensable"""

		other_hands = self.other_hands  

		for i in range(len(other_hands)):
			for j in range(len(other_hands[i])):  #Quand il n'y a plus de cartes dans la pioche, les joueurs n'ont pas forcément
			#le même nombre de cartes


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
			for k in range(len(other_hands[i])):
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

				for a in range(len(other_hands[i])):
					card = other_hands[i].cards[a]
					if self.list_status[i][a] == 0:
						discardable.append((a, card.number))

				if discardable :
					self.actions.append((discardable[0][0], 'd')) #Défausser la carte inutile de plus petit indice

				else :

					non_indisp = [] #Liste des cartes non-indispensables

					for b in range(len(other_hands[i])):
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


		current_player_name = game.current_player_name[4:-4]


		# Premier cas : il a été recommandé de jouer une carte, et aucune carte n'a été posée depuis
		if self.recommandation_list[current_player_name][0] == 'p' and self.played_cards[current_player_name] == 0: 


			card_to_play = str(int(self.recommandation_list[current_player_name][1]) + 1)
			self.recommandation_list[current_player_name] = " "  # On réinitialise la recommandation une fois qu'on l'a jouée
			
			for player_name in game.players:
				if player_name != current_player_name:
					self.played_cards[player_name] += 1  #On mémorise le fait qu'une carte a été jouée

			return("p" + card_to_play)


		#Deuxième cas : il a été recommandé de jouer une carte, mais un autre joueur a posé une carte depuis.
		#On vérifie alors que les joueurs peuvent se permettre une erreur
		elif self.recommandation_list[current_player_name][0] == 'p' and game.red_coins <= 1 and self.played_cards[current_player_name] <= 1:

			card_to_play = str(int(self.recommandation_list[current_player_name][1]) + 1)
			self.recommandation_list[current_player_name] = " "  # On réinitialise la recommandation une fois qu'on l'a jouée
			
			for player_name in game.players:
				if player_name != current_player_name:
					self.played_cards[player_name] += 1
			return("p" + card_to_play)


		#Troisième cas : on va donner un indice
		elif game.blue_coins != 0:

			s = 0
			for i in range(len(self.actions)):
				if self.actions[i][1] == 'p':
					s += self.actions[i][0]   # S'il faut jouer la carte, le numéro de l'action correspond à l'indice de la carte

				else:
					s += self.actions[i][0] + 4  # S'il faut défausser une carte, il faut ajouter 4 à l'indice de la carte en question

			t = s % 8  #Numéro donnant le joueur concerné par l'indice, ainsi que le type de ce dernier (couleur ou valeur)

			if t <= 3:  # Il s'agit d'un indice de valeur
				first_card = self.other_hands[t].cards[0]
				res = 'c' + str(first_card.number) + str(t + 1)
				for card in self.other_hands[t].cards :
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

			# La partie qui suit met à jour les recommandations pour chaque joueur

			current_player_index = game.players.index(current_player_name)

			for j in range(4):

				player = game.players[(current_player_index + j + 1) % 5]
				"""Permet de retrouver le nom du joueur qui est en position j par rapport au joueur courant"""

				if self.actions[j][1] == 'p':
					sum_actions = s - self.actions[j][0]
				else :
					sum_actions = s - (self.actions[i][0] + 4)

				sum_actions = sum_actions % 8
				recommandation_number = (t - sum_actions) % 8

				if recommandation_number <= 3:
					self.recommandation_list[player] = 'p' + str(recommandation_number)
				else :
					self.recommandation_list[player] = 'd' + str(recommandation_number % 4)


				self.played_cards[player] = 0
			

			return(res)

		elif self.recommandation_list[current_player_name][0] == 'd':
			return("d" + str(int(self.recommandation_list[current_player_name][1]) + 1))

		else : 
			return("d1")








				














		

		


