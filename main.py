from controller.controller import Controller
from gui.main_gui import MainGUI


def main():
    controller_ip = "127.0.0.1"  # IP address to connect to
    controller = Controller(controller_ip)

    gui = MainGUI()
    gui.run()


if __name__ == "__main__":
    main()
