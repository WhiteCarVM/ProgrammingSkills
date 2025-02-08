import argparse
import os
import socket
import subprocess
import shlex
import sys
import threading


def parser():
    """
    Parses command-line arguments and displays help information.
    """
    args = argparse.ArgumentParser(
        prog="python3 mynetcat.py",
        description='Enhanced Netcat Tool'
    )

    args.add_argument('-c', '--command', action='store_true', help='Enable command shell')
    args.add_argument('-e', '--execute', type=str, help='Execute specified command')
    args.add_argument('-l', '--listen', action='store_true', help='Enable listening mode')
    args.add_argument('-p', '--port', type=int, required=True, help="Port number")
    args.add_argument('-t', '--target', type=str, required=True, help='Target IP address')
    args.add_argument('-u', '--upload', type=str, help='Upload file')

    return args.parse_args()


class MyNetCat:
    def __init__(self, args):
        self.args = args
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
        Runs the MyNetCat instance based on the specified arguments.
        """
        try:
            if self.args.listen:
                print("[INFO] Starting in listen mode...")
                self.listen()
            else:
                print(f"[INFO] Connecting to {self.args.target}:{self.args.port}...")
                self.send()
        except KeyboardInterrupt:
            print("\n[INFO] Exiting...")
            self.socket.close()
            sys.exit()

    def execute(self, command):
        """
        Executes a shell command and returns the output.
        """
        print(f"[INFO] Executing command: {command}")
        command = command.strip()
        try:
            response = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
            return response.decode()
        except subprocess.CalledProcessError as ex:
            return f"[ERROR] Command failed: {ex.output.decode()}"

    def handle(self, client_socket):
        """
        Handles incoming connections and processes the requested action.
        """
        print("[INFO] Handling new connection...")
        if self.args.execute:
            response = self.execute(self.args.execute)
            client_socket.send(response.encode())
            client_socket.close()
        
        elif self.args.upload:
            print(f"[INFO] Receiving file: {self.args.upload}")
            file_size = int(client_socket.recv(16).decode().strip())
            print(f"[INFO] Expected file size: {file_size} bytes")
            received_size = 0
            
            with open(self.args.upload, 'wb') as file:
                while received_size < file_size:
                    data = client_socket.recv(min(4096, file_size - received_size))
                    if not data:
                        break
                    file.write(data)
                    received_size += len(data)
                    print(f"[INFO] Received {received_size}/{file_size} bytes")

            print(f"[SUCCESS] File {self.args.upload} saved successfully.")
            client_socket.send(f"[INFO] File {self.args.upload} uploaded successfully.".encode())
            client_socket.close()
    
        elif self.args.command:
            print("[INFO] Command shell started.")
            while True:
                client_socket.send(b"user: @> ")
                cmd_buffer = b""
                while b"\n" not in cmd_buffer:
                    data = client_socket.recv(1024)
                    if not data:
                        print("[INFO] Client disconnected.")
                        return
                    cmd_buffer += data
                response = self.execute(cmd_buffer.decode().strip())
                client_socket.send(response.encode())

    def listen(self):
        """
        Starts a server and listens for incoming connections.
        """
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"[INFO] Listening on {self.args.target}:{self.args.port}")

        while True:
            client_socket, address = self.socket.accept()
            print(f"[INFO] Connection from {address[0]}:{address[1]} established.")
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def send(self):
        """
        Connects to a remote host and sends data.
        """
        try:
            self.socket.connect((self.args.target, self.args.port))
            print(f"[INFO] Connected to {self.args.target}:{self.args.port}")

            if self.args.upload:
                file_path = self.args.upload
                if not os.path.isfile(file_path):
                    print(f"[ERROR] File {file_path} not found.")
                    return
                
                file_size = os.path.getsize(file_path)
                self.socket.send(f"{file_size:<16}".encode())
                
                with open(file_path, "rb") as file:
                    sent_size = 0
                    while chunk := file.read(4096):
                        self.socket.send(chunk)
                        sent_size += len(chunk)
                        print(f"[INFO] Sent {sent_size}/{file_size} bytes")

                print(f"[SUCCESS] File {file_path} sent successfully.")
                response = self.socket.recv(4096)
                print(response.decode())
            else:
                while True:
                    response = self.socket.recv(4096)
                    if not response:
                        break
                    print(response.decode())
                    buffer = input("> ") + "\n"
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("\n[INFO] User terminated")
        finally:
            self.socket.close()


if __name__ == "__main__":
    args = parser()
    MyNetCat(args).run() 