from tkinter import *
from tkinter import ttk
from Tab.Initiative import Initiative
from Tab.Decker import Decker
from Gui.MenuBar import MenuBar
from Gui.StatusBar import StatusBar
import json
from tkinter import messagebox


class State:
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.config = {}
        self.reloadable = []
        self.setup()

    def setup(self):
       self.reload_config()

    def create_default(self, path):
        default = open(path, 'w')
        d = {'pc': 'Player 1, Player2'}
        default.write(json.dumps(d))
        default.close()

    def reload_config(self):


        try:
            file = open(self.path, 'r')
            self.config = json.loads(file.read())
            file.close()
            print('Loaded Config')
        except FileNotFoundError:
            self.create_default(self.path)


    def add_reloadable(self, item):
        self.reloadable.append(item)

    def reload(self):
        print('Reloading')
        self.reload_config()

        for i in self.reloadable:
            try:
                i.reload()
            except:
                pass


class Main:
    def __init__(self):
        self.root = Tk()
        self.path = 'config/default.json'
        self.state = State(self.root, self.path)
        self.notebook = None
        self.loop = None
        print('Starting Interface')
        self.setup()

    def setup(self):

        self.root.title('Zero Interface')

        MenuBar(self.root, self.state)

        self.notebook = ttk.Notebook(self.root, height=640, width=480)
        self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)

        self.notebook.add(Initiative(self.notebook, self.state), text='Initiative')
        self.notebook.add(Decker(self.notebook, self.state), text='Decker')

        StatusBar(self.root, self.state)

        self.loop = self.root.mainloop()

Main()