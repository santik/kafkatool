from tkinter.ttk import Style

from views import configuration_window

from tkinter import Tk

class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("BSE Kafka Tool")
        self.set_window_center(900, 500)
        self.resizable(True, True)
        self.win_success = None

        # Treeview style
        style = Style()
        style.element_create("Custom.Treeheading.border", "from", "default")
        style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky': 'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky': 'nswe', 'children': [
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        style.configure("Custom.Treeview.Heading",
                        background="grey", foreground="white", relief="flat")

        configuration_window.ConfigurationWindow()

    def set_window_center(window, width, height):
        w_s = window.winfo_screenwidth()
        h_s = window.winfo_screenheight()
        x_co = (w_s - width) / 2
        y_co = (h_s - height) / 2 - 50
        window.geometry("%dx%d+%d+%d" % (width, height, x_co, y_co))
        window.minsize(width, height)

if __name__ == "__main__":
    APP_INIT = Main()
    APP_INIT.mainloop()
