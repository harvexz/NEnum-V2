import client
import controller


def main():
    option = int(input("You have not chosen a specific mode to run the progam in\n" \
                      "Please choose from the following\n" \
                      "1: Controller\n" \
                      "2: Client\n" \
                      "> "))
    if option == 1:
        controller_process = controller.Controller()
    if option == 2:
        client_process = client.Client("192.168.0.33", 12345)

if __name__ == '__main__':
    main()