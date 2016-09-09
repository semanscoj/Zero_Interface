class Program:
    def __init__(self, detail_dict):
        self.detail_dict = detail_dict
        self.name = None
        self.effect = None
        self.avail = None
        self.cost = None
        self.source = None
        self.attribute_mod = {}
        self.running_in = None
        self.setup()

    def setup(self):
        try:
            self.name = self.detail_dict['name']
            self.effect = self.detail_dict['effect']
            self.avail = self.detail_dict['avail']
            self.cost = self.detail_dict['cost']
            self.source = self.detail_dict['source']
        except Exception as e:
            print(e)

    def load(self, deck_obj):
        if self.running_in:
            self.unload()

        for k, v in self.attribute_mod.items():
            deck_obj.set_attribute(k, self.name, v)
        self.running_in = deck_obj

    def unload(self):
        if self.running_in:
            for k, v in self.attribute_mod.items():
                self.running_in.del_mod(k, self.name)
            self.running_in = None