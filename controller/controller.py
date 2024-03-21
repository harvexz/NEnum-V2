import socket
import json
from typing import List, Dict, Any
from gui import main_gui as G

class Controller:
    def __init__(self, ip_address, port: int):
        self.ip_address = ip_address
        self.port = port

    def send_command_to_client(self, client_address: str, command: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((client_address, self.port))
            s.sendall(command.encode())
            response = s.recv(1024).decode()
        return response

    def send_command_to_multiple_clients(self, command: str, client_addresses: List[str]) -> Dict[str, str]:
        responses = {}
        for address in client_addresses:
            response = self.send_command_to_client(address, command)
            responses[address] = response
        return responses

    def send_different_commands_to_clients(self, command_map: Dict[str, str]) -> Dict[str, str]:
        responses = {}
        for address, command in command_map.items():
            response = self.send_command_to_client(address, command)
            responses[address] = response
        return responses

    def get_client_info(self, client_address: str) -> Dict[str, Any]:
        # Implement logic to receive configurable information about a client machine
        pass


def main():
    gui = G.MainGUI()
    gui.run()


if __name__ == "__main__":
    main()