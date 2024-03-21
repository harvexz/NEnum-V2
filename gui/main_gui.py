from tkinter import *
import tkinter as tk
from tkinter import ttk, MULTIPLE, END, SINGLE

class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Controller GUI")

        self.connections= ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

        self.setup_ui()


    def setup_ui(self):
        """
        Implement GUI layout and components here

        :return:
        """
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Tab 1: Send Command to One Client
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Send Command to One Client")
        self.setup_single_client_tab()

        # Tab 2: Send Same Command to Multiple Clients
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Send Same Command to Multiple Clients")
        self.setup_multiple_clients_tab()

        # Tab 3: Send Different Commands to Different Clients
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Send Different Commands to Different Clients")
        self.setup_different_commands_tab()


    def setup_single_client_tab(self):

        connections_label = tk.Label(self.tab1, text="Select a single connection to send command")
        connections_label.pack()

        lb = tk.Listbox(self.tab1, selectmode=SINGLE, height=len(self.connections), width=50)
        for x in self.connections:
            lb.insert(END, x)
        lb.pack()


        label = tk.Label(self.tab1, text="Enter command:")
        label.pack()

        self.single_client_entry = tk.Entry(self.tab1)
        self.single_client_entry.pack()

        send_button = tk.Button(self.tab1, text="Send Command", command=self.send_single_client_command)
        send_button.pack()

        self.single_client_result_label = tk.Label(self.tab1, text="")
        self.single_client_result_label.pack()


    def setup_multiple_clients_tab(self):

        connections_label = tk.Label(self.tab2, text="Select multiple connections to send command")
        connections_label.pack()

        lb = tk.Listbox(self.tab2, selectmode=MULTIPLE, height=len(self.connections), width=50)
        for x in self.connections:
            lb.insert(END, x)
        lb.pack()

        label = tk.Label(self.tab2, text="Enter command:")
        label.pack()

        self.multiple_clients_entry = tk.Entry(self.tab2)
        self.multiple_clients_entry.pack()

        send_button = tk.Button(self.tab2, text="Send Command", command=self.send_multiple_clients_command)
        send_button.pack()

        self.multiple_clients_result_label = tk.Label(self.tab2, text="")
        self.multiple_clients_result_label.pack()


    def setup_different_commands_tab(self):

        self.commands_frame = ttk.Frame(self.tab3)
        self.commands_frame.pack()

        self.command_entries = []
        self.results_labels = []

        for i in range(len(self.connections)):  # Number of clients
            label = tk.Label(self.commands_frame, text=f"Enter command for Client {self.connections[i]}:")
            label.grid(row=i, column=0)

            entry = tk.Entry(self.commands_frame)
            entry.grid(row=i, column=1)
            self.command_entries.append(entry)

            result_label = tk.Label(self.commands_frame, text="")
            result_label.grid(row=i, column=2)
            self.results_labels.append(result_label)

        send_button = tk.Button(self.tab3, text="Send Commands", command=self.send_different_commands)
        send_button.pack()


    def send_single_client_command(self):
        command = self.single_client_entry.get()
        # Placeholder for sending command to one client
        # For now, just display the command in the GUI
        self.single_client_result_label.config(text="Command sent to one client: {}".format(command))


    def send_multiple_clients_command(self):
        command = self.multiple_clients_entry.get()
        # Placeholder for sending command to multiple clients
        # For now, just display the command in the GUI
        self.multiple_clients_result_label.config(text="Command sent to multiple clients: {}".format(command))


    def send_different_commands(self):
        # Placeholder for sending different commands to different clients
        for i, entry in enumerate(self.command_entries):
            command = entry.get()
            if not command: command = "No Command Sent"
            self.results_labels[i].config(text=f"Command sent to Client {self.connections[i]}: {command}")


    def update_connections(self, connections):

        self.connections = connections
        print(connections)


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = MainGUI()
    gui.run()
