import socket
import threading
from threading import Thread
import time

class Controller:
    #def __init__(self, ip_address, port: int):
    def __init__(self):
        self.ip_address = "192.168.0.33"
        self.port = 12345
        self.connections = {}


        # Start a thread to run server
        self.server = threading.Thread(target=self.run_server)
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
                print(f"Connection from: {client_ip}")

                self.connections[client_ip] = client_socket
                threading.Thread(target=self.handle_client, args=(client_socket)).start() # call function to listen to return from client connection
        except Exception as error:
            print(f"Error: {error}")

    def accept_connections(self, server_socket):
        while True:
            client_socket, client_address = server_socket.accept()
            self.connections.append(client_address[0])  # Add client IP to the list of connections
            # Update the GUI with the new list of connections
            gui.update_connections(self.connections)
            # Start a new thread to handle communication with the client
            Thread(target=self.handle_client, args=(client_socket,)).start()

    # def send_command_to_client(self, client_address: str, command: str) -> str:
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((client_address, self.port))
    #         s.sendall(command.encode())
    #         response = s.recv(1024).decode()
    #     return response
    #
    # def send_command_to_multiple_clients(self, command: str, client_addresses: List[str]) -> Dict[str, str]:
    #     responses = {}
    #     for address in client_addresses:
    #         response = self.send_command_to_client(address, command)
    #         responses[address] = response
    #     return responses
    #
    # def send_different_commands_to_clients(self, command_map: Dict[str, str]) -> Dict[str, str]:
    #     responses = {}
    #     for address, command in command_map.items():
    #         response = self.send_command_to_client(address, command)
    #         responses[address] = response
    #     return responses
    #
    # def get_client_info(self, client_address: str) -> Dict[str, Any]:
    #     # Implement logic to receive configurable information about a client machine
    #     pass


def main():
    controller = Controller()


if __name__ == '__main__':
    main()
