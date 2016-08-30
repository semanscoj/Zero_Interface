class AttributeInterface:
    def __init__(self, name, keys):
        AttributeInterface.name = name
        setattr(self, name, {})
        self._attributes = getattr(self, name)
        self._attributes = {i : AttributeState(i) for i in keys}

    def del_mod(self, key, name):
        self._attributes[key].del_mod(name)

    def update(self, *args, key=None):
        if key and key in self._attributes:
            self._attributes[key].update()
        else:
            try:
                [i.update() for i in self._attributes.values()]
            except Exception as e:
                print(e)

    def set_attribute(self, key, name, val):
        self._attributes[key].set(name=name, val=val)

    def sum(self, key):
        if key in self._attributes:
            return self._attributes[key].calc_val()
        else:
            return 0

    def get_attribute(self, key):
        if key in self._attributes:
            self._attributes[key].get()

    def clear_binds(self):
        for key in self._attributes.keys():
            self._attributes[key].clear_binds()

    def bind_attribute(self, key, cb):
        if key in self._attributes:
            self._attributes[key].listen(cb)


class AttributeState:
    def __init__(self, key):
        self.key = key
        self.to_update = []
        self.modifiers = {}

    def set(self, name=None, val=0):
        if name:
            self.modifiers[name] = val
            self.update()

    def get(self, name=None):
        if name:
            return self.modifiers[name]
        elif 'Base' in self.modifiers:
            return self.modifiers['Base']
        else:
            return None

    def del_mod(self, key):
        del (self.modifiers[key])
        self.update()

    def listen(self, cb):
        self.to_update.append(cb)

    def clear_binds(self):
        del self.to_update[:]

    def update(self, *args):
        for i in self.to_update:
            i(self.key, self.calc_val())

    def calc_val(self):
        val = 0

        for v in self.modifiers.values():
            try:
                val += int(v)
            except:
                print('non int value', self.key)
                pass
        return val