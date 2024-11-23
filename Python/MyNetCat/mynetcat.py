import shlex
import socket
import subprocess
import sys
import threading
import argparse

class MyNetCat:
    def __init__(self, args, buffer=None):
        """
            This function initializes some parameters
        """
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
            This function runs MyNetCat 
        """
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def execute(self, command):
        """
            This function is used for executing commands on target
        """
        command = command.strip()
        response = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
        return response.decode()

    def handle(self, client_socket):
        """
            This function creates tasks for arguments
        """
        if self.args.execute:
            response = self.execute(self.args.execute)
            client_socket.send(response.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as file:
                file.write(file_buffer)
            message = f"File {self.args.upload} saved"
            client_socket.send(message.encode())
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b"user:> ")
                    while b'\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = self.execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as ex:
                    print("Server killed:", ex)
                    self.socket.close()
                    sys.exit()

    def listen(self):
        """
            This function describes listener for incoming clients
        """
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"Listening on {self.args.target}:{self.args.port}")

        while True:
            client_socket, address = self.socket.accept()
            print(f"Connection from {address} established.")
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def send(self):
        """
            This function describes sender to MyNetCat
        """
        self.socket.connect((self.args.target, self.args.port))

        if self.buffer:
            self.socket.send(self.buffer)

        recv_length = 1
        response = ""
        try:
            while recv_length:
                data = self.socket.recv(4096)
                recv_length = len(data)
                response += data.decode()
                if recv_length < 4096:
                    break
                
            if response:
                print(response)
                buffer = input("> ") + "\n"
                self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("User terminated\n")
            self.socket.close()
            sys.exit()