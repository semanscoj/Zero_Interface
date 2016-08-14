from tkinter import *
from tkinter import ttk


class StatusBar(ttk.Frame):

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
        self.pack(side=BOTTOM, fill=X)

    def setup(self):
        label = Label(self, text='Status')
        label.pack()
