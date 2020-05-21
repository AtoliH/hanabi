import hanabi
import recommandation_ai
import numpy as np
import matplotlib.pyplot as plt




score = np.zeros(1000)

for i in range(1000) :

	game = hanabi.Game(players = 5)
	ai = recommandation_ai.Recommandation(game)

	game.ai = ai
	game.quiet = True
	game.run()

	score[i] = game.score


moy = sum(score)/len(score)


bins = [x + 0.5 for x in range(10, 26)]
plt.hist(score, edgecolor = 'red', bins = bins, rwidth = 0.8, density = True)



plt.show()
print("Moyenne =", moy)


