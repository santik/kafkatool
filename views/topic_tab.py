from tkinter import Frame, Button, Label, PhotoImage, StringVar, Scrollbar, Entry
from tkinter.constants import *
from tkinter.ttk import Treeview

import pandas as pd

from service.main_kafka import get_kafka_consumer, reset_offset
from service.search_box import SearchBox
from views.message_dialog import MessageDialog


class TopicTab:
    separator = '-----------------------' + '\n'
    col_names = ['Timestamp', 'Data']
    width = 600
    height = 500

    def __init__(self, master, server_url, topic_name):
        self.topicName = topic_name
        self.server_url = server_url
        self.messagesBox = None
        self.messageList = []
        self.element = None
        self.parent = None
        self.master = master
        self.consumer = None
        self.consuming_job = None
        self.dataFrame = None
        self.messagesCounter = StringVar()
        self.messages_limit = 100
        self.limit_entry = None
        self.messagesCounter.set(0)
        self.init_data_frame()

    def init_data_frame(self):
        self.dataFrame = pd.DataFrame(columns = self.col_names)

    def __output_messages(self, topicName):
        self.cancel_consuming()
        consumer = get_kafka_consumer(topicName, self.server_url)
        self.consumer = reset_offset(consumer, topicName, self.messages_limit)
        self.consume_messages()

    def cancel_consuming(self):
        if self.consuming_job is not None:
            self.element.after_cancel(self.consuming_job)
            self.consuming_job = None
        try:
            self.consumer.close()
        except:
            pass

    def consume_messages(self):
        message = self.consumer.poll(0.01)
        if message is not None:
            self.add_message(message)
            self.print_messages(self.dataFrame)

        self.limit_consumer()

    def limit_consumer(self):
        if len(self.dataFrame) < self.messages_limit:
            self.consuming_job = self.element.after(50, self.consume_messages)
        else:
            print("Consuming stopped")

    def add_message(self, message):
        print("Consumed message from " + self.topicName + "with offset " + str(message.offset()))
        self.dataFrame = self.dataFrame.append(
            {'Data': message.value().decode('utf-8'), 'Timestamp': str(message.timestamp()[1])},
            ignore_index=True)
        self.messagesCounter.set(len(self.dataFrame.Data))

    def show(self, tabs):
        self.parent = tabs
        root = Frame(tabs, width=self.width, height=self.height-50)
        root.pack_propagate(0)

        self.make_controls(root)

        self.element = root

        self.make_messages_box(root)

        self.__output_messages(self.topicName)

    def make_messages_box(self, root):
        self.messagesBox = Frame(root)
        self.messagesBox.pack(side=RIGHT, fill=BOTH)

    def make_controls(self, root):
        controls = Frame(root, background=root.cget("background"))
        SearchBox(controls, command=self.__on_search_request, placeholder="Type and press enter",
                  entry_highlightthickness=0).pack(side=LEFT, ipady=1, padx=1)

        Label(controls, text="Cnt:").pack(side=LEFT, ipady=1, padx=1)
        Label(controls, textvariable=self.messagesCounter, width=5).pack(side=LEFT)

        Label(controls, text="Limit:").pack(side=LEFT, ipady=1, padx=1)
        self.limit_entry = Entry(controls, width=5)
        self.limit_entry.insert(0, self.messages_limit)
        self.limit_entry.pack(side=LEFT, ipady=1, padx=1)

        close_image = PhotoImage(file="resources/images/cancel.png")
        close_button = Button(controls, image=close_image, command=lambda: self.master.destroyTab(self.topicName))
        close_button.image = close_image
        close_button.pack(side=RIGHT, ipady=1, padx=1)

        refresh_image = PhotoImage(file="resources/images/reload.png")
        refresh_button = Button(controls, image=refresh_image, command=self.refresh)
        refresh_button.image = refresh_image
        refresh_button.pack(side=RIGHT, ipady=1, padx=1)

        controls.pack(fill=BOTH, ipady=1, padx=1)

    def __on_search_request(self, search):
        filtered = self.dataFrame[self.dataFrame.Data.str.contains(search.lower())]
        self.messagesCounter.set(len(filtered.Data))
        self.print_messages(filtered)

    def print_messages(self, dataFrame):
        list_box = Treeview(self.messagesBox, columns=self.col_names, show='headings', height=19) #height is in number of rows:)
        for col in self.col_names:
            list_box.heading(col, text=col)
        list_box.grid(row=0, column=0, sticky='nsew', in_=self.messagesBox)
        list_box.tag_configure('odd', background='#f9f9f9')
        list_box.tag_configure('even', background='#DFDFDF')
        list_box.column("Timestamp", width=150)
        list_box.column("Data", width=400)
        scroll_bar = Scrollbar(self.messagesBox, orient="vertical", command=list_box.yview)
        scroll_bar.grid(row=0, column=1, sticky='ns')
        list_box.configure(yscrollcommand=scroll_bar.set)

        for index, row in dataFrame.iterrows():
            type = 'even'
            if (len(list_box.get_children()) % 2 == 1):
                type = 'odd'

            list_box.insert("", "end", values=(row.Timestamp, row.Data), tags=(type,))

        list_box.bind("<<TreeviewSelect>>", lambda event, t=list_box: self.message_click(event, t))

    def refresh(self):
        self.messages_limit = int(self.limit_entry.get())
        self.init_data_frame()
        self.__output_messages(self.topicName)


    def message_click(self, event, tree):
        item = tree.item(tree.focus()).values()
        MessageDialog(self.element, title='Message', text=list(item)[2][1])
