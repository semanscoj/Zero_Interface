import json
from Utils.Attributes import AttributeInterface


class Agent(AttributeInterface):
    def __init__(self, state):
        self.state = state
        self.skills = ["Cybercombat", "Electronic Warfare", "Hacking", "Computer", "Hardware", "Software", "Logic",
                       "Int", "Will"]
        AttributeInterface.__init__(self, 'attributes', self.skills)
        self.setup()

    def setup(self):
        print('loading skills..')
        with open('Resources/skills.json', 'r') as f:
            data = json.loads(f.read())

        for k, v in data.items():
            self.set_attribute(k, 'Base', v)
