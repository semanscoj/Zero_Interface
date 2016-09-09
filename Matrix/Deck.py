import json, os
from Utils.Attributes import AttributeInterface


class DeckManager:
    def __init__(self, state):
        self.state = state
        self._decks = None
        self.programs = []

    def deck_names(self, print_now=False, pre='', post=''):
        for i in self.state.decks:
            name = i.get("DECK")
            if print_now:
                print(pre, name, post)
        return [pre + i.get("DECK") + post for i in self.state.decks]

    def get_by_name(self, name):
        for i in self.state.decks:
            if str(i) == name:
                return i
        return self.state.decks[0]


class Deck(AttributeInterface):
    def __init__(self, state, dict):
        self.state = state
        self.stats = ['Sleaze', 'Attack', 'Firewall', 'Data Processing']
        AttributeInterface.__init__(self, 'attributes', self.stats)
        self.dict = dict
        self.array = []
        self.assigned_array = []
        self.setup()

    def setup(self):
        for key, value in self.dict.items():
            try:
                setattr(self, key, value)
            except:
                print('Dict pair not set in deck object')
                pass

        if 'ARRAY' in self.dict:
            try:
                self.array = [int(i.strip()) for i in self.dict['ARRAY'].split(' ')]
            except:
                print('Got non number in array')
                self.array = range(1, 5)

        with open('Resources/deck_mods.json', 'r') as f:
            mods = json.loads(f.read())

        for mod in mods:
            name = mod['name']
            changes = mod['mods']
            for k, v in changes.items():
                self.set_attribute(k, name, v)


    def get(self, key):
        if key in self.dict.keys():
            return getattr(self, key)
        else:
            return None

    def show_info(self):

        str = ''
        for k,v in self.dict.items():
            str += '%s: %s\n' % (k,v)
        print(str)
        return str

    def __str__(self):
        return str(self.get('DECK'))

if __name__ == '__main__':
    manager = DeckManager()
    deck = manager.decks[0]

    print(deck)
