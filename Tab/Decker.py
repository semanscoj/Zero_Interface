from tkinter import *
import tkinter as tk
from tkinter import ttk
from Matrix.Deck import DeckManager
from Utils.Attributes import AttributeInterface
import json
from tkinter import messagebox


class Decker(ttk.Frame):
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        ttk.Frame.__init__(self, self.parent)
        self.manager = DeckManager(self.state)
        self.display_template = '%s (%s)'
        self.interface_binds = []
        self.command_data = {}
        self.device_selector = None
        self.labels = {}
        self.deck_array_options = {}
        self.setup()
        self.pack()

    def setup(self):
        self.deck_selector()
        self.deck_limit_view()
        self.matrix_skills()
        self.matrix_commands()

        but = Button(self, text="test", command=self.test)
        but.pack()
        self.bind_to_selection()

    def test(self):
        self.bind_to_selection()

    def bind_to_selection(self, new=None):
        if new:
            self.state.agent.deck.clear_binds()
            self.state.agent.deck = new

        for i in self.interface_binds:
            i(self.state.agent)
            i(self.state.agent.deck)
        self.state.agent.update()

    def deck_selector(self):
        top = Frame(self, relief=RAISED, borderwidth=3)
        top.pack(side=TOP, fill=X)

        label = Label(top, text='Select Device:')
        label.pack(side=LEFT, expand=True)

        base = StringVar()
        self.device_selector = OptionMenu(top, base, *self.manager.deck_names(), command=lambda e, base=base: self.change_device(base.get()))
        self.device_selector.pack(side=LEFT, expand=True)

    def change_device(self, name):
        device = self.manager.get_by_name(name)
        self.bind_to_selection(device)
        for k, tup in self.deck_array_options.items():

            menu = tup[0]['menu']
            value_variable = tup[1]

            menu.delete(0, 'end')
            for j in device.array:
                menu.add_command(label=j,
                            command=tk._setit(value_variable, j, lambda e, k=k, variable=value_variable: self.set_base(k, variable)))
                value_variable.set('')
            self.set_base(k, 0)

    def matrix_commands(self):

        command_frame = Frame(self, relief=RAISED, borderwidth=3)

        with open('Matrix/commands.json', 'r') as f:
            data = json.loads(f.read())

        data = sorted(data, key=lambda k: k['Complex Action'])

        for x, i in enumerate(data):
            if x == 0 or x % 3 == 0:
                temp = Frame(command_frame)
                temp.pack(fill=BOTH)

            name = i['Complex Action']

            self.command_data[name] = i

            label = Label(temp, text=name)
            label.bind('<1>', lambda e, name=name: self.show_info(name))
            label.pack(side=LEFT, expand=True)
            self.labels[name] = label
            self.interface_binds.append(lambda e, name=name: self.calc_command(name))

        remainder = len(data) % 3

        if remainder > 0:
            for i in range(remainder):
                label = Label(temp, text='')
                label.pack(side=LEFT, expand=True)

        command_frame.pack(side=TOP, fill=X)

    def show_info(self, key):
        print('showing info for', key)
        if key in self.command_data:
            output = ''
            order = ['Complex Action', 'Marks', 'Limit', 'Function', 'Note', 'Test']
            for i in order:
                try:
                    v = self.command_data[key][i]
                    output += "%s: %s\n" % (i, v)
                except KeyError:
                    pass
            messagebox.showinfo(key, output)
        else:
            print(key, 'not found in')

    def calc_command(self, key):
        agent_value = 0
        deck_value = 0

        checks = self.command_data[key]['checks']

        for i in checks:
            agent_value += self.state.agent.sum(i)
            deck_value += self.state.agent.deck.sum(i)

        self.update_label(key, agent_value + deck_value)


    def matrix_skills(self):
        skills = ["Cybercombat", "Electronic Warfare", "Hacking", "Computer", "Hardware", "Software", "Logic",
                  "Int", "Will"]

        skills = sorted(skills)

        skill_frame = Frame(self, relief=RAISED, borderwidth=3)

        for x, i in enumerate(skills):
            if x == 0 or x % 2==0:
                temp = Frame(skill_frame)
                temp.pack(fill=BOTH)
            label = Label(temp, text=i)
            label.pack(side=LEFT, expand=True)
            self.labels[i] = label
            self.interface_binds.append(lambda e, i=i: e.bind_attribute(i, self.update_label))

        if len(skills) % 2 > 0:
            label = Label(temp, text='')
            label.pack(side=LEFT, expand=True)

        skill_frame.pack(side=TOP, fill=X)

    def deck_limit_view(self):
        top = Frame(self, relief=RAISED, borderwidth=3)
        top.pack(side=TOP, fill=X)

        deck_label_frame = Frame(top)
        deck_label_frame.pack(fill=X)

        attributes = ['Attack', 'Sleaze', 'Data Processing', 'Firewall']

        attributes = sorted(attributes)

        for i in attributes:
            temp_frame = Frame(deck_label_frame)
            temp = Label(temp_frame, text=i)
            self.labels[i] = temp
            temp.pack(side=LEFT, expand=True)
            self.interface_binds.append(lambda e, i=i: e.bind_attribute(i, self.update_label))
            temp_frame.pack(side=LEFT, expand=True)

        deck_info_frame = Frame(top)
        deck_info_frame.pack(fill=X)

        for i in attributes:
            temp_frame = Frame(deck_info_frame)
            temp = Label(temp_frame, text=i)
            temp.pack(side=LEFT, expand=True)

            variable = StringVar()
            option = OptionMenu(temp_frame, variable, ())
            option.pack(side=LEFT)

            self.deck_array_options[i] = (option, variable)

            temp_frame.pack(side=LEFT, expand=True)

    def set_base(self, key, svar):
        if type(svar) == OptionMenu:
            print('got option menu item')
        elif type(svar) == StringVar:
            print('get')
            value = svar.get()
            svar.set(value)
        elif type(svar) == int:
            value = svar
        else:
            print('error in set_base', key, svar)
            return
        self.state.agent.deck.set_attribute(key, 'Base', value)

    def update_label(self, key, val):
        if key in self.labels:
            self.labels[key]['text'] = self.display_template % (key, val)


class Agent(AttributeInterface):
    def __init__(self, state, deck):
        self.state = state
        self.skills = ["Cybercombat", "Electronic Warfare", "Hacking", "Computer", "Hardware", "Software", "Logic",
                       "Int", "Will"]
        AttributeInterface.__init__(self, 'attributes', self.skills)
        self.deck = deck
        self.setup()

    def setup(self):
        print('loading skills..')
        with open('Matrix/skills.json', 'r') as f:
            data = json.loads(f.read())

        for k, v in data.items():
            self.set_attribute(k, 'Base', v)
        #self.listen(self.deck.update)

    def equip(self):
        print('equiping')