from tkinter import *
from tkinter import ttk

class PopWindow(object):
    def __init__(self, master, header, label_text_array, default_values=None, call_back=None):
        self.top = self.top = Toplevel(master)
        self.call_back = call_back
        self.pair = []
        self.header = header
        self.label_text_array = label_text_array
        self.default_values = default_values
        self.setup(self.label_text_array)
        self.values = None
        self.ok = None

    def setup(self, text_array):
        label = Label(self.top, text=self.header)
        label.pack()
        self.ok = Button(self.top,text='Ok', command=self.cleanup)
        self.ok.bind('<Return>', self.cleanup_cb)

        if self.default_values == 0 or self.default_values:
            has_defaults = True
            if hasattr(self.default_values, '__len__'):
                has_many = (len(text_array) == len(self.default_values))
            else:
                has_many = False
        else:
            has_defaults = False

        if type(text_array) == str:
            if has_defaults:
                default = self.default_values
            else:
                default = None
            self.pair.append(self.EntryPair(self.top, text_array, call_back=self.cleanup_cb, default_value=default))
            self.pair[0].entry.focus()
        else:
            for i in text_array:

                if has_defaults:
                    if has_many:
                        default = self.default_values[i]
                    else:
                        default = self.default_values
                else:
                    default = None

                self.pair.append(self.EntryPair(self.top, i, call_back=self.cleanup_cb, default_value=default))

                self.pair[0].entry.focus()
        self.ok.pack()

    def cleanup_cb(self, event):
        self.cleanup()

    def cleanup(self):
        d = {}
        for i in self.pair:
            k, v = i.get()
            d[k] = v
        self.top.destroy()
        self.call_back(d)



    class EntryPair:
        def __init__(self, parent, label_text, call_back=None, default_value=None):
            self.container = ttk.Frame(parent)
            self.label_text = label_text
            self.call_back = call_back
            self.default_value = default_value
            self.label = Label(self.container, text=label_text)
            self.entry = Entry(self.container)
            self.setup()

        def setup(self):

            if self.call_back:
               self.entry.bind('<Return>', self.call_back)

            if self.default_value == 0 or self.default_value:
                self.entry.delete(0, END)
                self.entry.insert(0, self.default_value)

            self.label.pack(side=LEFT)
            self.entry.pack(side=LEFT)
            self.container.pack()

        def get(self):
            return self.label_text, self.entry.get()