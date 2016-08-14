from tkinter import *
import os

class MenuBar:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.setup()

    def setup(self):
        menu = Menu(self.parent)
        self.parent.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Reload', command=self.state.reload)
        file.add_command(label='Quit', command=self.state.root.destroy)
        menu.add_cascade(label='File', menu=file)


        help = Menu(menu)
        help.add_command(label='Open Config Folder', command=self.show_conf)
        menu.add_cascade(label='Help', menu=help)

    def show_conf(self):
        root = os.getcwd() + '\config'
        os.system('explorer %s' % root)
