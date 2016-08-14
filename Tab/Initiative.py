from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Gui.Pop import PopWindow
from Gui.VerticalScrolledFrame import VerticalScrolledFrame


class Initiative(ttk.Frame):
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.scrolling = None
        self.react_buttons = []
        self.react = None
        self.react_ready = None
        self.button_default = None
        self.turn = 0
        ttk.Frame.__init__(self, self.parent)
        self.setup()
        self.pack()

    def setup(self):
        controls = ttk.Frame(self)
        controls.pack(side=TOP,fill=X)

        self.reaction_frame()
        self.state.add_reloadable(self)
        button1 = Button(controls, text='Add Actor', command=self.add)
        self.button_default = button1.cget('bg')
        button1.pack(side=LEFT)

        button2 = Button(controls, text='Init Call', command=self.get_init)
        button2.pack(side=LEFT)

        button3 = Button(controls, text='Next Actor', command=self.next)
        button3.pack(side=LEFT)

        button4 = Button(controls, text='Reset', command=self.reset)
        button4.pack(side=LEFT)

        self.scrolling = VerticalScrolledFrame(self)
        self.scrolling.pack(fill=BOTH, expand=True)

        self.parent.bind('<Return>', self._next)

        self.load_players()

    def load_players(self):
        if 'pc' in self.state.config:
            for i in self.state.config['pc'].split(','):
                Actor(self, self.scrolling.interior, i)
        else:
            messagebox.showinfo('No player data', 'Consider adding player info to %s or through the config option under file' % self.state.path)

    def reload(self):
        self.clear()
        self.load_players()

    def reaction_frame(self):

        self.react = {'Block' : {"cost": 5, "desc": "Unarmed Combat to next Melee Defense"},
                 'Dodge' : {"cost": 5, "desc": "Gymnastics to next Melee Defense"},
                 'Full Defense' : {"cost": 10, "desc": "Willpower to All Defense until next Round"},
                 'Hit the Dirt' : {"cost": 5, "desc": "Drop Prone to avoid Suppressive Fire"},
                 'Intercept' : {"cost": 5, "desc": "Melee Attack against Passing For within Reach"},
                 'Parry' : {"cost": 5, "desc": "Melee Weapon Skill to next Melee Defense"}}

        reactions = ttk.Frame(self)

        for i in self.react.keys():
            cost = self.react[i]['cost']
            label_string = '%s (%s)' % (i, cost)

            temp = Button(reactions, text=label_string)
            temp.bind('<1>', lambda event, temp=temp, i=i: self.reaction_button(event, temp, i))
            temp.bind('<3>', lambda event, i=i: self.reaction_info_button(event, i))
            self.react_buttons.append(temp)
            temp.pack(side=LEFT)

        reactions.pack(side=TOP, fill=X)

    def reaction_info_button(self, event, key):
        react = self.react[key]
        display = '%s (Cost:%s): %s' % (key, react['cost'], react['desc'])
        messagebox.showinfo(key, display)

    def reaction_button(self, event, button, key):

        if self.react_ready:
            button.config(bg=self.button_default)
            self.react_ready = None
            return
        else:
            for i in self.react_buttons:
                i.config(bg=self.button_default)

        button.config(bg='green', activebackground='green', relief=SUNKEN)

        self.react_ready = (button, key)

    def add(self):
        def _add(names):
            for i in names.values():
                Actor(self, self.scrolling.interior, i, npc=True)

        def _build(number_dict):

            num = [number_dict[i] for i in number_dict.keys()]

            try:
                num = int(num[0])
            except ValueError as e:
                messagebox.showerror('Invalid Input', 'Enter a number!')
                self.add()
                return

            answer = messagebox.askquestion('Defaults', 'Would you like to use default names?')

            if answer == 'yes':
                for i in ['Person: ' + str(i + 1) for i in range(num)]:
                    Actor(self, self.scrolling.interior, i, npc=True)
            else:
                PopWindow(self, 'How Many?', ['Person: ' + str(i + 1) for i in range(num)], call_back=_add)

        PopWindow(self, 'How Many?', 'Number to add?', call_back=_build)

        self.sort()

    def clear(self):
        for i in self.scrolling.interior.winfo_children()[:]:
            self.remove(i)

    def reset(self):
        print('reset')
        self.turn = 0
        for i in self.scrolling.interior.winfo_children()[:]:
            players = self.state.config['pc'].split(',')
            if i.name in players:
                i.set_current(0)
                i.un_active()
            else:
                self.remove(i)

    def remove(self, actor):
        actors = sorted(self.scrolling.interior.winfo_children(), key=lambda actor: int(actor._current_init),
                        reverse=True)
        for i in actors:
            if i == actor:

                if actor == actors[self.turn-1]:
                    if self.turn >= len(actors):
                        actors[0].active()
                    else:
                        actors[self.turn].active()

                i.pack_forget()
                i.destroy()
                self.sort()
                return

    def _next(self, event):
        self.next()

    def next(self):
        actors = sorted(self.scrolling.interior.winfo_children(), key=lambda actor: int(actor._current_init), reverse=True)
        total = len(actors)

        if not total:
            return


        if self.turn + 1 <= total and actors[self.turn]._current_init > 0:
            actors[self.turn].active()
            actors[self.turn-1].un_active()
            self.turn += 1
        else:
            self.round()
            self.turn = 0
            actors[self.turn].active()
            self.deactivate()
            if actors[0]._current_init > 0:
                self.next()
                self.all_idle()
            else:
                self.get_init()

    def all_idle(self):
        for i in self.scrolling.interior.winfo_children():
            i.idle()

    def deactivate(self):
        for i in self.scrolling.interior.winfo_children():
            i.un_active()

    def round(self):
        end = True
        for i in self.scrolling.interior.winfo_children():
            left = i.round()
            if left:
                end = False
        self.sort()
        return end


    def sort(self):
        actor_list = sorted(self.scrolling.interior.winfo_children(), key=lambda actor: int(actor._current_init), reverse=True)

        for i in actor_list:
            i.pack_forget()
            i.repack()

    def get_init(self):
        def set_val(val):
            for i in val.keys():
                i.set_start(val[i])
            self.sort()
            self.next()
        PopWindow(self, 'Enter Init', self.scrolling.interior.winfo_children(), call_back=set_val)


class Actor(Frame):
    def __init__(self, init, parent, name, npc=False):
        self.init = init
        self.parent = parent
        self.name = name
        self.name_label = None
        self._start_init = 0
        self.reactions = []
        self._current_init = 0
        Frame.__init__(self, self.parent, relief=GROOVE, borderwidth=2)
        self.setup()
        self.repack()

    def set_start(self, num):
        try:
           int(num)
        except ValueError:
            num = 0
            pass

        self._start_init = int(num)
        self._current_init = int(num)
        self.actor_update()

    def set_current(self, num):
        try:
            num = int(num)
        except TypeError as e:
            num = 0
            print(e)

        self._current_init = num
        self.actor_update()


    def active(self):

        if self._current_init == 0:
            return

        canvas = self.init.scrolling.canvas_done
        height = canvas.winfo_height()

        test = canvas.canvasy(height)

        move = self.winfo_y()


        place = height/move


        canvas.yview_moveto(test)
        self.configure(background='green')

    def un_active(self):
        self.configure(background='white')
        self.remove_reactions()

    def idle(self):
        if self._current_init == 0:
            self.configure(background='red')
            self.remove_reactions()

    def repack(self):
        self.actor_update()
        self.pack(fill=X, padx=10, pady=10)

    def setup(self):
        self.un_active()
        self.bind('<1>', self.clicked)

        self.name_label = ttk.Label(self, text=self.name)
        self.name_label.bind('<1>', self.clicked)
        self.name_label.pack(fill=X, side=LEFT)

        button = Button(self, text="remove", command=self.remove)
        button.pack(side=LEFT)
        self.button_default = button.cget('bg')

    def remove(self):
        self.init.remove(self)

    def clicked(self, event):

        if self.init.react_ready:
            self.handle_reaction()

        print(self.name)

    def cancel_reaction(self, label, val):
        print(val)
        self.current(-val)
        self.remove_reaction(label)

    def remove_reaction(self, r):
        r.pack_forget()
        r.destroy()

    def remove_reactions(self):
        for i in self.reactions:
            self.remove_reaction(i)

    def handle_reaction(self):
        button = self.init.react_ready[0]
        key = self.init.react_ready[1]

        val = self.init.react[key]['cost']

        if self._current_init - val < 0:
            messagebox.showerror('Reaction', 'You can\'t apply a reaction\nto an actor with a zero initiative.')
            return

        self.current(val)
        button.config(bg=self.button_default)
        self.init.react_ready = None

        label = Label(self, text=key)
        label.pack(side=LEFT)

        label.bind('<1>', lambda e: self.cancel_reaction(label, val))
        self.reactions.append(label)

    def actor_update(self):
        self.set_name_label()

    def current(self, val):

        current = self._current_init

        self._current_init = (current-val) if current - val >=0 else 0

        self.init.sort()

    def set_name_label(self):
        val = '%s: (%d)' % (self.name, self._current_init)
        self.name_label.config(text=val)

    def round(self):
        self._current_init = self._current_init - 10

        if self._current_init < 0:
            self._current_init = 0

        self.actor_update()
        return self._current_init

    def __str__(self):
        return str(self.name)

