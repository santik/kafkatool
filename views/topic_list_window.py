from tkinter import ttk, messagebox

from service.list_widget import ListWidget
from service.main_kafka import getTopicList
from views import topic_tab

class KafkaWindow:
    tabsElement = None
    list = None
    server_url = None
    tabsList = dict()
    max_tabs = 5

    def printTopicList(self, topic_list):
        self.list = ListWidget(command=self.onTopicNameClick)
        sorted_topic_list=sorted(topic_list)
        self.list.topic_list=sorted_topic_list;
        self.list.prepare_list(sorted_topic_list)

    def onTopicNameClick(self, topicName):
        if topicName in self.tabsList:
            self.focusTab(topicName)
        else:
            self.createTabForTopic(topicName)

    def open_window(self, zookeeper_host, zookeeper_port):
        self.server_url = zookeeper_host + ':' + zookeeper_port

        self.initTopicTabs()

        topic_list = getTopicList(self.server_url)
        self.printTopicList(topic_list)

    def initTopicTabs(self):
        tabs = ttk.Notebook()
        tabs.grid(row=0, column=1, rowspan=2)
        tabs.pack_propagate(0)
        self.tabsElement = tabs

    def focusTab(self, topicName):
        self.stop_consuming_not_active_tabs(topicName)
        self.tabsElement.select(self.tabsList[topicName].element)

    def destroyTab(self, topicName):
        self.tabsElement.forget(self.tabsList[topicName].element)
        self.tabsList[topicName].cancel_consuming()
        del self.tabsList[topicName]

    def createTabForTopic(self, topicName):
        if len(self.tabsList.keys()) >= self.max_tabs :
            messagebox.showinfo("Tabs limit reached", "Only " + str(self.max_tabs) + " open tabs are allowed. Please close some to open new.")
            return

        tab = topic_tab.TopicTab(self, self.server_url, topicName)
        tab.show(self.tabsElement)

        tab_name = (tab.topicName[:15] + '..') if len(tab.topicName) > 17 else tab.topicName

        self.tabsElement.add(tab.element, text=tab_name)  # Add the tab
        self.tabsElement.select(tab.element)
        self.tabsList[topicName] = tab
        self.stop_consuming_not_active_tabs(topicName)

    def stop_consuming_not_active_tabs(self, active_tab_name):
        for not_active_tabs in self.tabsList.keys():
            if not_active_tabs != active_tab_name:
                self.tabsList[not_active_tabs].cancel_consuming()

    def destroy(self):
        for tabs in self.tabsList.keys():
            self.tabsList[tabs].cancel_consuming()
        self.tabsElement.destroy()
        self.list.destroy()
        self.tabsList.clear()
