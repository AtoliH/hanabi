
import hanabi

import my_new_smart_ai


game = hanabi.Game(2)  # 2 players

ai = my_new_smart_ai.RandomAI(game)

# pour jouer toute une partie
game.ai = ai
game.run()
