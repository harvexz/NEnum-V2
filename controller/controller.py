import socket
import threading
import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
from threading import Thread
import time

# Defult Project Settings
font = "Arial"

colour1 = "#0C0C0C"
colour2 = "#31363F"
colour3 = "#810CA8"
colour4 = "#C147E9"

class Controller:
    #def __init__(self, ip_address, port: int):
    def __init__(self):
        self.ip_address = "192.168.0.33"
        self.port = 12345
        self.connections = {} # formatted as such: {(ip of client, port): socket}
        self.ip_options = ["None"]

        self.setup_gui()
        self.add_widgets()

        # Start a thread to run server
        self.server = threading.Thread(target=self.run_server)
        #self.server.daemon = True # thread will close when program closes, doesn't have to complete
        self.server.start()


    def setup_gui(self):
        """
        Function to simply setup the GUI window and set default settings

        :return:
        """
        # GUI setup
        self.root = ctk.CTk()
        self.root.title("Client")
        self.root.geometry(f"{900}x{700}")

        # Grid configure
        self.root.grid_rowconfigure((0), weight=0)
        self.root.grid_rowconfigure((2,4), weight=1, minsize=250)

        self.root.grid_columnconfigure((2), weight=1)
        self.root.grid_columnconfigure((1), minsize=300)


    def add_widgets(self):
        """
        Function to add widgits to GUI window
        :return:
        """
        self.title = ctk.CTkLabel(self.root, text="Controller Pannel", font=(font, 20))
        self.title.grid(row=0, column=0, columnspan=3, pady=(20, 0), padx=(0, 0), sticky="nwe")

        self.connected_label = ctk.CTkLabel(self.root, text="Clients Connected:")
        self.connected_label.grid(row=1, column=0, pady=(0,10) , padx=(20, 0), sticky="nws")

        self.edit_label = ctk.CTkLabel(self.root, text="Manage and view:")
        self.edit_label.grid(row=1, column=1, pady=(10, 10), padx=(0, 0), sticky="nsw")

        self.view_option = ctk.CTkOptionMenu(self.root, values=self.ip_options, fg_color=colour2, button_color=colour4,
                                             button_hover_color=colour3, dropdown_fg_color=colour2, dropdown_hover_color= colour4)
        self.view_option.grid(row=1, column=1, pady=10, padx=(10, 0), sticky="nse")

        self.connected_list = CTkListbox(self.root, multiple_selection=False, height=500, width=250)
        self.connected_list.grid(row=2, column=0, padx=10, pady=10, sticky="nws")

        self.connection_output = ctk.CTkTextbox(self.root, fg_color=colour2)
        self.connection_output.grid(row=2, column=2, padx=(0,10), pady=(0, 10), sticky="nswe")
        self.connection_output.configure(state="disabled")

        self.checkvar = ctk.StringVar(value="off")
        self.allow_multi = ctk.CTkCheckBox(self.root, text="Alow selecton of multiple clients", variable=self.checkvar, onvalue="on",
                                           offvalue="off", fg_color=colour4, hover_color=colour3, command=self.allow_multiple)
        self.allow_multi.grid(row=3, column=0, sticky="nswe", padx=40, pady=(0, 20))

        self.main_output = ctk.CTkTextbox(self.root, fg_color=colour2)
        self.main_output.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nswe")
        self.main_output.configure(state="disabled")


    def allow_multiple(self):
        if self.checkvar.get() == "on":
            self.connected_list.configure(multiple_selection=True)
        elif self.checkvar.get() == "off":
            self.connected_list.configure(multiple_selection=False)


    def update_connections(self):
        """
        Used to update all lists, drop downs etc to contain only current connections
        :return:
        """

        self.update_connected_list()
        self.update_dropdown_options()


    def update_connected_list(self):

        self.connected_list.delete(0, tk.END)  # clear list

        for connection in self.connections:
            self.connected_list.insert(tk.END, connection)


    def update_dropdown_options(self):
        self.ip_options = []  # reset variable for drop down

        for connection in self.connections:
            self.ip_options.append(connection[0])

        if not self.ip_options: self.ip_options = ["None"] # if empty set to a none option

        self.view_option.configure(values=self.ip_options) # updates drop down menu options from amended list
        self.view_option.set(self.ip_options[0]) # selects first item in list


    def main_screen_output(self, output_message):

        print(output_message) # Display to terminal

        self.main_output.configure(state="normal")
        self.main_output.insert(tk.END, output_message + "\n") # Display to GUI
        self.main_output.configure(state="disabled")


    def client_screen_output(self, output_message, client_ip):

        print(output_message) # Display to terminal

        f = open(client_ip[0], "a")
        f.write(output_message)
        f.close()

        self.update_client_screen(client_ip[0])


    def update_client_screen(self, client_ip):

        self.connection_output.delete(0, tk.END) # clear output screen

        self.connection_output.configure(state="normal") # makes text field editable
        f = open(client_ip, "r")  # open and read file
        lines = f.readlines() # read lines
        f.close()

        for line in lines:
            self.connection_output.insert(tk.END, line) # write lines to text field
        self.connection_output.configure(state="disabled") # make text filed un-editable


    def handle_client(self, client_socket, client_ip):
        try:
            while True:
                response = client_socket.recv(4096).decode()
                if response:
                    self.client_screen_output(response, client_ip)

        except ConnectionResetError:
            self.main_screen_output(f"Client: {client_ip[0]}:{client_ip[1]} disconnected")
        except Exception as e:
            output_message = f"An error occurred with {client_ip}: {e}\n"
            print(output_message)
        finally:
            client_socket.close()
            del self.connections[client_ip]
            self.update_connections()


    def run_server(self):
        """
        Start the server, listen for incomming connection, and create new thread for each connection
        :return:
        """

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip_address, self.port))
            server_socket.listen()

            self.main_screen_output("Listening for connections")

            while True:
                # wait for connection from client
                client_socket, client_ip = server_socket.accept()
                self.main_screen_output(f"Connection from: {client_ip[0]}:{client_ip[1]}")

                # Create/clear output file
                f = open(client_ip[0], "w")
                f.write("")
                f.close()

                self.connections[client_ip] = client_socket
                self.update_connections()
                self.example_send_command(client_ip)
                threading.Thread(target=self.handle_client, args=(client_socket, client_ip)).start() # call function to listen to return from client connection
        except Exception as error:
            self.main_screen_output(f"Error: {error}")


    def example_send_command(self, client_ip):
        client_socket = self.connections[client_ip]
        client_socket.sendall("Hello".encode())



def main():
    controller = Controller()
    controller.root.mainloop()


if __name__ == '__main__':
    main()
