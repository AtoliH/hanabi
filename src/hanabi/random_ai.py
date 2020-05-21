import hanabi

import random as rd

class Random(hanabi.ai.AI):


	def play(self):
		index = rd.randint(0, 3)
		return("d" + str(index))


