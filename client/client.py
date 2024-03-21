import socket

class Client:
    def __init__(self, ip_address, port: int):
        self.ip_address = ip_address
        self.port = port

    def receive_command(self, command: str) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip_address, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data.upper())  # Echo back received data in uppercase
