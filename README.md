# NEnum
This project implements a network controller and client system in Python, allowing users to control multiple client machines remotely over a network. The controller provides a graphical user interface (GUI) through which users can send commands to connected client machines and receive the returned results. The client application receives instructions from the controller and executes them on the client machine.


## Table of  Contents

- [NEnum](#nenum)
   * [Table of  Contents](#table-of-contents)
   * [Overveiw](#overveiw)
   * [Features](#features)
      + [Basic Functionality](#basic-functionality)
      + [Advanced Functionality](#advanced-functionality)
   * [Usage](#usage)
      + [Controller](#controller)
      + [Client](#client)
   * [Installation](#installation)

## Overveiw
The system consists of two main components:

1. Controller: The controller is a GUI application built using CustomTkinter. It allows users to connect to multiple client machines over a network, send commands to them, and receive relevant feedback.
2. Client: The client GUI application runs on each client machine. It listens for commands from the controller, executes them, and sends back the results to the controller.


## Features

### Basic Functionality

* Controller:
    * Connects to client machines over a network
    * Sends commands to individual client machines
    * Receives feedback from client machines
* Client:
    * Listens for commands from the controller
    * Executes commands
    * Sends results back to the controller

### Advanced Functionality

* Controller:
    * Can send commands to multiple clients simultaneously
    * Can send different commands to each connected client
    * Options to gather various system information from clients (e.g. network information, processor information, user accounts)
* Client:
    * Allows configuration of controller IP address
    
## Usage

The user should decide what program they would like to run and complete the following for their choice:

### Controller
Running the following will start the controller program and will bring up the GUI

```
$ cd controller
$ python3 controller.py
```

### Client
Running the following will start the client program and will bring up the GUI

```
$ cd client
$ python3 client.py
```


## Installation
1. Clone repository to your local machine
    ```
    git clone <repo.url>
    ```
2. Navigate to project directory
    ```
    cd NEnum
    ```
3. Optional but recommended: Create and start virtual environment
    ```
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install requirements
    ```
   pip install -r requirements.txt
   ```
5. Run Controller or Client as described in [usage](#usage) section


