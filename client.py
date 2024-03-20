import socket

class Client:
    def __init__(self, client_ip: str):
        self.client_ip = client_ip

    def receive_command(self, command: str) -> str:
        # Implement logic to receive command from the controller and execute it, returning the result
        pass
