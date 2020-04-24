import hanabi
import random as rd

class Random(hanabi.AI):


	def play(self):

		index = rd.randint(0, 3)
		return("p" + str(index))


