import socket

class Client:
    def __init__(self, ip_address, port: int):
        self.ip_address = ip_address
        self.port = port

        self.connect()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, self.port))
        print(f"Connected to controller: {self.ip_address}:{self.port}")

        self.get_command(s)


    def handle_command(self, command):
        """
        Function to handle and return result from command received

        :param command:
        :return:
        """

        command = command.decode()

        print(f"Actioned command: {command}")


    def get_command(self, s):
        """
        Function to receive command

        :param s:
        :return:
        """
        while True:
            command = s.recv(4096)

            if not command: break

            print(f"Command received: {command.decode()}")

            output = self.handle_command(command)


if __name__ == '__main__':
    client = Client("192.168.0.33", 12345)