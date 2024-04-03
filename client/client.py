import socket
import threading
import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
from tkinter import messagebox
import time

# Defult Project Settings
font = "Arial"

colour1 = "#0C0C0C"
colour2 = "#31363F"
colour3 = "#810CA8"
colour4 = "#C147E9"

class Client:
    def __init__(self, ip_address: str, port: int):
        self.ip_address = ip_address
        self.port = port

        self.setup_gui()
        self.add_widgets()

        # thread to connect to client
        self.connect_thread = threading.Thread(target=self.connect)
        self.connect_thread.daemon = True
        self.connect_thread.start()


    def setup_gui(self):
        """
        Function to simply setup the GUI window and set default settings

        :return:
        """
        # GUI setup
        self.root = ctk.CTk()
        self.root.title("Client")
        self.root.geometry(f"{500}x{500}")

        # Grid configure
        self.root.grid_rowconfigure((0), weight=0)
        self.root.grid_rowconfigure((2), weight=1)
        self.root.grid_columnconfigure((0), weight=1)


    def add_widgets(self):
        """
        Function to add widgits to GUI window
        :return:
        """
        self.title = ctk.CTkLabel(self.root, text="Client Pannel", font=(font, 20))
        self.title.grid(row=0, column=0, pady=(20, 0), padx=(0, 0), sticky="nwe")

        self.indicator = ctk.CTkLabel(self.root, text="Disconnected", text_color="red")
        self.indicator.grid(row=1, column=0, pady=(0,10) , padx=(20, 0), sticky="nws")

        self.textbox = ctk.CTkTextbox(self.root, fg_color=colour2)
        self.textbox.grid(row=2, column=0, columnspan=1, padx=20, pady=(0, 20), sticky="nswe")
        self.textbox.configure(state="disabled")

        self.settings_button = ctk.CTkButton(self.root, text="Settings", fg_color=colour4, hover_color=colour3)
        self.settings_button.grid(row=3, column=0, sticky="nswe", padx=40, pady=(0, 20))


    def screen_output(self, output_message):
        try:
            output_message = output_message.decode()
        except (UnicodeDecodeError, AttributeError):
            pass

        print(output_message) # Display to terminal

        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, output_message + "\n") # Display to GUI
        self.textbox.configure(state="disabled")


    def connect_status(self, connected: bool):
        if connected:
            self.indicator.configure(text="Connected", text_color="green")
        else:
            self.indicator.configure(text="Disconnected", text_color="red")


    def connect(self):

        while True:
            connected = False

            while not connected:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip_address, self.port))
                    self.screen_output(f"Connected to controller: {self.ip_address}:{self.port}\n")
                    self.connect_status(True)
                    connected = True
                except ConnectionRefusedError:
                    self.screen_output("Connection failed: Ensure controller running - Waiting...")
                    time.sleep(4)

            self.get_command(s)


    def handle_command(self, command: bytes):
        """
        Function to handle and return result from command received

        :param command:
        :return:
        """

        command = command.decode()

        output_message = f"Actioned command: {command}"
        self.screen_output(output_message)


    def get_command(self, s: socket.socket):
        """
        Function to receive command

        :param s:
        :return:
        """
        while True:

            try:
                command = s.recv(4096)
            except ConnectionResetError:
                break

            if not command: break

            output_message = f"Command received: {command.decode()}"
            self.screen_output(output_message)

            output = self.handle_command(command)

        self.screen_output("\n!! Disconnected from controller !!\n")
        self.connect_status(False)


if __name__ == '__main__':
    client = Client("192.168.0.33", 12345)
    client.root.mainloop()