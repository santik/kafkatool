import tkinter as tk
import tkinter.simpledialog as simpledialog


class MessageDialog(simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):
        self.text = tk.Text(self, width=100, height=5)
        self.text.pack(fill="both", expand=True)

        self.text.insert("1.0", self.data)
        self.text.config(state=tk.DISABLED)

        return self.text

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.bind("<Return>", self.ok)

        box.pack()
