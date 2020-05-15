import hanabi


def InformationAi(hanabi.ai.AI):

	

def __init__(self, game):
		hanabi.ai.AI.__init__(self, game)

		self.tables = {}

		for player_name in game.players :  #Création d'une table par joueur
			self.tables[player_name] = 5*[5*[5*[True]]]

		


	def card_status(self, card):
		game = self.game

		self.list_status = np.zeros((4, 4)) #Liste qui va contenir à l'indice i, j le statut de la jème carte du ième joueur

		"""0 : défaussable
		   1 : jouable
		   2 : indispensable
		   3 : non-indispensable"""


		if card.number == game.piles[card.color] + 1: #La carte peut être posée sur le dessus d'une pile
			self.list_status[i, j] = 1

		elif card.number <= game.piles[card.color]:  #La carte ne peut plus être posée et peut donc être défaussée
			self.list_status[i, j] = 0

		elif game.deck.card_count[card.number] == game.discard_pile.cards.count(card) + 1: 
			#La carte est la dernière de son type (les autres ont été défaussées), il faut donc absolument la conserver
			self.list_status[i, j] = 2

		else:  #La carte est non-indispensable
			self.list_status[i, j] = 3



	def 
