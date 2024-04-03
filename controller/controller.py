import socket
import threading
from threading import Thread
import time

class Controller:
    #def __init__(self, ip_address, port: int):
    def __init__(self):
        self.ip_address = "192.168.0.33"
        self.port = 12345
        self.connections = {} # formatted as such: {(ip of client, port): socket}


        # Start a thread to run server
        self.server = threading.Thread(target=self.run_server)
        #self.server.daemon = True # thread will close when program closes, doesn't have to complete
        self.server.start()


    def start(self):
        # Start listening for incoming connections
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip_address, self.port))
        server_socket.listen()

        # Start a separate thread to handle incoming connections
        self.server = threading.Thread(target=self.run_server)
        self.server.start()


    def handle_client(self, client_socket):
        pass


    def run_server(self):
        """
        Start the server, listen for incomming connection, and create new thread for each connection
        :return:
        """

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip_address, self.port))
            server_socket.listen()

            print("Listening for connections")

            while True:
                # wait for connection from client
                client_socket, client_ip = server_socket.accept()
                print(f"Connection from: {client_ip[0]}:{client_ip[1]}")

                self.connections[client_ip] = client_socket
                self.example_send_command(client_ip)
                threading.Thread(target=self.handle_client, args=(client_socket)).start() # call function to listen to return from client connection
        except Exception as error:
            print(f"Error: {error}")


    def example_send_command(self, client_ip):
        client_socket = self.connections[client_ip]
        print("a")
        print(f"cs: {client_socket}")
        client_socket.sendall("Hello".encode())



def main():
    controller = Controller()


if __name__ == '__main__':
    main()
