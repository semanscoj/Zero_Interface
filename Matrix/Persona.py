from Matrix.Agent import Agent
from Matrix.Deck import Deck


class Persona:
    def __init__(self, state):
        #  self.agent = Agent(self, self.decks[5])
        self.state = state
        self.deck = self.state.decks[5]
        self.agent = Agent(self)
        self.setup()

    def update(self):
        if self.agent:
            self.agent.update()
        if self.deck:
            self.deck.update()

    def view(self, cb):
        cb(self.deck)
        cb(self.agent)

    def setup(self):
        print('print')