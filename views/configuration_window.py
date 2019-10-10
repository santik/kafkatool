from functools import partial
from tkinter import Frame, Label, Button, PhotoImage, Entry, LabelFrame

from db.configuration_database import get_all_clusters, get_cluster, update_configuration, \
    insert_configuration, delete_configuration
from views import topic_list_window


class ConfigurationWindow:
    clusterName = "CLUSTER_NAME"
    zookeeperHost = "ZOOKEEPER_HOST"
    zookeeperPort = "ZOOKEEPER_PORT"

    def __init__(self):
        self.cluster_name = None
        self.zookeeper_host = None
        self.zookeeper_port = None
        self.kafka_window = None
        self.frame = Frame()
        self.frame.config(padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="wn")

        self.cluster_frame = LabelFrame(self.frame, text="Clusters")
        self.cluster_frame.config(font=("Arial", 14), padx=10, pady=10)
        self.cluster_frame.grid(row=1, column=0)

        self.list_clusters_frame()

    def save(self, old_cluster_name):
        if(old_cluster_name == ""):
            insert_configuration(self.cluster_name.get(), self.zookeeper_host.get(), self.zookeeper_port.get())
        else:
            update_configuration(self.cluster_name.get(), self.zookeeper_host.get(), self.zookeeper_port.get(), old_cluster_name)
        self.clean_frame(self.cluster_frame)
        self.list_clusters_frame()

    def delete(self, cluster_name):
        delete_configuration(cluster_name)
        self.clean_frame(self.cluster_frame)
        self.list_clusters_frame()

    def disconnect(self):
        self.clean_frame(self.cluster_frame)
        self.list_clusters_frame()
        self.kafka_window.destroy()

    def connect(self, cluster_name):
        self.clean_frame(self.cluster_frame)
        self.disconnect_cluster_frame(cluster_name)
        configuration = get_cluster(cluster_name)
        self.kafka_window = topic_list_window.KafkaWindow()
        self.kafka_window.open_window(configuration[0][1], configuration[0][2])

    def settings(self, new_cluster_name=None):
        self.clean_frame(self.cluster_frame)
        cluster_name = ""
        cluster_host = ""
        cluster_port = ""

        if(new_cluster_name!=None):
            configuration = get_cluster(new_cluster_name)
            cluster_name = configuration[0][0]
            cluster_host = configuration[0][1]
            cluster_port = configuration[0][2]

        # Cluster Name Fields
        Label(self.cluster_frame, text="Cluster Name").grid(row=0, column=0)

        self.cluster_name = Entry(self.cluster_frame, width=40)
        self.cluster_name.grid(row=0, column=1)
        self.cluster_name.insert('0', cluster_name)

        # Zookeeper Host Fields
        Label(self.cluster_frame, text="Zookeeper Host").grid(row=1, column=0)

        self.zookeeper_host = Entry(self.cluster_frame, width=40)
        self.zookeeper_host.grid(row=1, column=1)
        self.zookeeper_host.insert('0', cluster_host)

        # Zookeeper Port Fields
        Label(self.cluster_frame, text="Zookeeper Port").grid(row=2, column=0)

        self.zookeeper_port = Entry(self.cluster_frame, width=40)
        self.zookeeper_port.grid(row=2, column=1)
        self.zookeeper_port.insert('0', cluster_port)

        # Button Group
        Button(self.cluster_frame, text="Save & Close", command=lambda: self.save(cluster_name)).grid(row=3, column=1)

    def list_clusters_frame(self):
        configurations = get_all_clusters()
        connect_image = PhotoImage(file="resources/images/connect.gif")
        settings_image = PhotoImage(file="resources/images/settings.gif")
        delete_image = PhotoImage(file="resources/images/delete.gif")

        counter = 0
        for configuration in configurations:
            configuration_cluster_name = configuration[0]
            cluster_name_label = Label(self.cluster_frame, text=configuration_cluster_name)
            cluster_name_label.config(font=("Arial", 12))
            cluster_name_label.grid(row=counter, column=1)

            connect_button = Button(self.cluster_frame, text = "connect",
                                    image=connect_image,
                                    command=partial(self.connect, configuration_cluster_name))
            connect_button.image = connect_image
            connect_button.grid(row=counter, column=2)

            settings_button = Button(self.cluster_frame, text = "settings",
                                     image=settings_image,
                                     command=partial(self.settings, configuration_cluster_name))
            settings_button.image = settings_image
            settings_button.grid(row=counter, column=3)

            delete_button = Button(self.cluster_frame, text = "delete",
                                   image=delete_image,
                                   command=partial(self.delete, configuration_cluster_name))
            delete_button.image = delete_image
            delete_button.grid(row=counter, column=4)

            counter += 1

        add_image = PhotoImage(file="resources/images/add.gif")
        add_button = Button(self.cluster_frame, text = "add",
                            image=add_image,
                            command=lambda: self.settings())
        add_button.image = add_image
        add_button.grid(row=counter, column=4, pady=10)

    def disconnect_cluster_frame(self, cluster_name):
        self.cluster_frame.pack_forget()
        disconnect_image = PhotoImage(file="resources/images/disconnect.gif")
        cluster_name_label = Label(self.cluster_frame, text=cluster_name)
        cluster_name_label.config(font=("Arial", 12))
        cluster_name_label.grid(row=0, column=1)

        connect_button = Button(self.cluster_frame, text = "disconnect",
                                image=disconnect_image,
                                command=lambda: self.disconnect())
        connect_button.image = disconnect_image
        connect_button.grid(row=0, column=2)

    @staticmethod
    def clean_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()
