import hanabi

Game = hanabi.Game


def GamePlus(Game):
    def run(self):
        try:
            last_players = list(self.players)
            while last_players:
                if len(self.deck.cards) == 0:
                    self.log()
                    self.log("--> Last turns:",
                                " ".join(last_players),
                                "may still play once.")
                    try:
                        last_players.remove(self.players[self.current_player])
                    except ValueError:
                        pass  # if Alice 'x', she is removed but plays again
                self.turn(self.ai)
                if self.score == 25:
                    raise StopIteration("it is perfect!")
        # self.log("Game finished because deck exhausted")
        except (KeyboardInterrupt, EOFError, StopIteration) as e:
            self.log('Game finished because of', e)
            pass
        self.save('autosave.py')

        self.log("\nOne final glance at the table:")
        self.log(self.starting_deck)
        self.print_piles()
