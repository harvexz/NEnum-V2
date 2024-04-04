import platform
import socket
import threading
import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
import platform
import time
import uuid
try:
    import netifaces
except ModuleNotFoundError:
    print("Module 'netifaces' not installed")


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
        uname = platform.uname()
        self.os = uname.system

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
        self.textbox.see(tk.END)  # auto scroll to bottom


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
                    s.sendall("Connection acknowledged".encode())
                    self.connect_status(True)
                    connected = True
                except ConnectionRefusedError:
                    self.screen_output("Connection failed: Ensure controller running - Waiting...")
                    time.sleep(4)

            self.get_command(s)


    def get_users(self) -> list:
        """
        Function to handle get user command

        Reads from /etc/shadow and will only return users with a home directory or root directory (root)

        :return: -> List: users
        """
        users = []

        try:
            f = open("/etc/passwd", "r")
            contents = f.readlines()
            f.close()
        except FileNotFoundError:
            return ["File not found, ensure readable and on a linux system"]
        except PermissionError:
            return ["Error with permissions, ensure file readable"]

        for line in contents:
            if "/home" in line or "/root" in line: # used to get real users
                line = line.split(":")
                if line[1] != "x":
                    usr_info = f"User: {line[0]} Password: {line[1]} GID: {line[3]} Home dir: {line[5]}"
                else:
                    usr_info = f"User: {line[0]} GID: {line[3]} Home dir: {line[5]} Shell: {line[6]}"
                users.append(usr_info)

        return users


    def processor_info(self):
        results = {}

        try:
            file = open('/proc/cpuinfo', 'r')
            cpu_info = file.readlines()
            file.close()
        except FileNotFoundError:
            return ["File not found, ensure readable and on a linux system"]
        except PermissionError:
            return ["Error with permissions, ensure file readable"]

        results = {"Vendor" : cpu_info[1].split(":")[1], "Model" : cpu_info[4].split(":")[1], "MHz" :cpu_info[7].split(":")[1], "Cache size" : cpu_info[8].split(":")[1]}

        return results


    def network_info(self):
        results = {}

        if self.os == "Linux":
            try:
                interfaces = netifaces.interfaces()
                results["Network interfaces"] = ", ".join(interfaces)
                for x in range(len(interfaces)):
                    address_for = f"\nMacAddress for {interfaces[x]}"
                    results[address_for] = ''.join((netifaces.ifaddresses(interfaces[x])[netifaces.AF_LINK][0]["addr"]))
                print(results)
                results[interfaces[-1]] = ''.join((results[f"\nMacAddress for {interfaces[-1]}"], "\n"))
            except NameError:
                self.screen_output("Module 'netifaces' not found")
                return {"Error": "Module not installed on client"}

        elif self.os == "Windows":
            macaddr = hex(uuid.getnode())[2:]
            print(macaddr)
            results["MacAddress"] = ':'.join(macaddr[i:i + 2] for i in range(0, len(macaddr), 2))

        return results


    def handle_command(self, command: bytes, s: socket.socket):
        """
        Function to handle and return result from command received

        :param command:
        :return:
        """
        response = [] # initialising variable

        command = command.decode()

        if command == "usrs":
            s.sendall("\nReturn for: Get Users ->\n".encode())
            response = self.get_users()
        elif command == "processor":
            s.sendall("\nReturn for: Processor Information ->\n".encode())
            response = self.processor_info()
        elif command == "netinfo":
            s.sendall("\nReturn for: Network Information ->\n".encode())
            response = self.network_info()

        # return the results of command
        if response:
            if type(response) is list:
                for value in response:
                    s.sendall(value.encode())
            elif type(response) is dict:
                for value in response:
                    s.sendall(f"{value}: {response[value]}".encode())

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

            self.handle_command(command, s)

        self.screen_output("\n!! Disconnected from controller !!\n")
        self.connect_status(False)


if __name__ == '__main__':
    client = Client("192.168.0.33", 12345)
    client.root.mainloop()