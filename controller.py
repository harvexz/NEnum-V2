import socket
import json
from typing import List, Dict, Any

class Controller:
    def __init__(self, controller_ip: str):
        self.controller_ip = controller_ip

    def send_command_to_client(self, client_address: str, command: str) -> str:
        # Implement logic to send command to a single client/receive response
        pass

    def send_command_to_multiple_clients(self, command: str, client_addresses: List[str]) -> Dict[str, str]:
        # Implement logic to send command to multiple clients/receive responses
        pass

    def send_different_commands_to_clients(self, command_map: Dict[str, str]) -> Dict[str, str]:
        # Implement logic to send different commands to each connected client/receive responses
        pass

    def get_client_info(self, client_address: str) -> Dict[str, Any]:
        # Implement logic to receive configurable information about a client machine
        pass
