from tkinter import Frame, END, LabelFrame, Scrollbar, Entry
from tkinter.ttk import Treeview, Style


class ListWidget:

    def __init__(self, command=None):
        self.topic_list=None;
        outsideFrame = Frame();
        outsideFrame.config(padx=10, pady=10)
        outsideFrame.grid(row=1, column=0, sticky="wn")

        self.frame = LabelFrame(outsideFrame, text="Topics")
        self.frame.config(font=("Arial", 14), padx=10, pady=10)
        self.frame.grid(row=0, column=0)
        self._command = command

        self.topic_filter_input = Entry(self.frame, width=33)
        self.topic_filter_input.grid(row=0, column=0, pady=10)
        self.topic_filter_input.bind("<KeyRelease>", self.filter_topic)

        treeFrame = Frame(self.frame)
        treeFrame.grid(row=1, column=0)
        self.tree = Treeview(treeFrame, style="Custom.Treeview")
        self.tree.heading('#0', text='Topic')
        self.tree.pack()
        self.tree.bind("<ButtonRelease-1>", self.OnClick)
        self.tree.tag_configure('odd', background='#f9f9f9')
        self.tree.tag_configure('even', background='#DFDFDF')

        scroll_bar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scroll_bar.grid(row=1, column=1, sticky='nsew')
        self.tree.configure(yscrollcommand=scroll_bar.set)

    def filter_topic(self, *args):
        inputed_topic = self.topic_filter_input.get();
        list = filter(lambda k: inputed_topic.lower() in k.lower(), self.topic_list)
        self.prepare_list(list)

    def OnClick(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item == '':
            return;
        selectedItem = self.tree.item(item, "text")
        self._command(selectedItem)

    def prepare_list(self, sorted_topic_list):
        self.clean()
        for topic in sorted_topic_list:
            self.insert(topic)

    def insert(self, line):
        type = 'even'
        if(len(self.tree.get_children())%2 ==1):
            type = 'odd'
        self.tree.insert("", "end", text=line, tags=(type,))

    def clean(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def destroy(self):
        self.frame.destroy()