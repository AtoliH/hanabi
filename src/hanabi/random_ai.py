import ai
import random as rd

class Random(ai.AI):


	def play(self):

		index = rd.randint(0, 3)
		return("p" + str(index))


