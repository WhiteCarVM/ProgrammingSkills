import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading
import time

def parser():
    """
        This function is using as a help menu
    """
    
    args = argparse.ArgumentParser(
        prog="python3 mynetcat.py",
        description='This is my netcat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
            python3 mynetcat.py -t 8.8.8.8 -p 4444 # connect to target server
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l #target server listens connections
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l -c # target server listens connections, after connection client can use command shell
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l -u=test.txt # target server listens connections, after connection client can upload file "test.txt"
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l -e="cat /etc/passwd" # target server listens connections, after connection client can execute command "cat /etc/passwd"
    '''))

    
    args.add_argument('-c', '--command', action='store_true', help='use command shell')
    args.add_argument('-e', '--execute', type=str, help='execute specified command')
    args.add_argument('-l', '--listen', action='store_true', help='listen mode')
    args.add_argument('-p', '--port', type=int, default=10000, required=True, help="target port to connection")
    args.add_argument('-t', '--target', type=str, default="0.0.0.0", required=True, help='target IP address to connection')
    args.add_argument('-u', '--upload', help='upload file to target')

    return args.parse_args()

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

        try:
            if self.args.listen:
                self.listen()
            else:
                self.send()
        except KeyboardInterrupt:
            time.sleep(1)
            print("\nExiting...")
            time.sleep(1)
            self.socket.close()
            sys.exit()

    def execute(self, command):
        """
            This function is used for executing commands on target
        """

        command = command.strip()

        try:
            response = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
            return response.decode()
        except subprocess.CalledProcessError as ex:
            return f"Command failed: {ex.output.decode()}"

    def handle(self, client_socket):
        """
        This function creates tasks for arguments.
        """

        if self.args.execute:
            response = self.execute(self.args.execute)
            try:
                client_socket.send(response.encode())
            except Exception as e:
                print(f"Error sending response: {e}")
            client_socket.close()
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file_buffer += data
                except Exception as e:
                    print(f"Error receiving data: {e}")
                    break
        
            if file_buffer:
                with open(self.args.upload, 'wb') as file:
                    file.write(file_buffer)
                message = f"File {self.args.upload} saved successfully."
                try:
                    client_socket.send(message.encode())
                except Exception as e:
                    print(f"Error sending response: {e}")
            client_socket.close()
    
        elif self.args.command:
            try:
                while True:
                    client_socket.send(b"user: @> ")
                    cmd_buffer = b''

                    while b'\n' not in cmd_buffer:
                        try:
                            data = client_socket.recv(1024)
                            if not data:
                                print("Client disconnected.")
                                return
                            cmd_buffer += data
                        except Exception as e:
                            print(f"Error receiving command: {e}")
                            return
                
                    if cmd_buffer:
                        response = self.execute(cmd_buffer.decode().strip())
                        if response:
                            try:
                                client_socket.send(response.encode())
                            except BrokenPipeError:
                                print("Client disconnected while sending response.")
                            except Exception as e:
                                print(f"Error sending response: {e}")
            except Exception as ex:
                print("Error occurred:", ex)
            finally:
                client_socket.close()


    def listen(self):
        """
            This function describes listener for incoming clients
        """

        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"Listening on {self.args.target}:{self.args.port}")

        while True:
            client_socket, address = self.socket.accept()
            print(f"Connection from {address[0]}:{address[1]} established.")
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def send(self):
        """
        This function describes sender to MyNetCat
        """

        try:
            self.socket.connect((self.args.target, self.args.port))

            if self.buffer:
                self.socket.send(self.buffer)

            while True:
                recv_length = 1
                response = ""
                while recv_length:
                    data = self.socket.recv(4096)
                    recv_length = len(data)
                    response += data.decode()
                    if recv_length < 4096:
                        break
            
                if response:
                    print(response)

                try:
                    buffer = input("> ") + "\n"
                    self.socket.send(buffer.encode())
                except EOFError:
                    print("Exiting.")
                    break
        except KeyboardInterrupt:
            print("\nUser terminated")
        finally:
            self.socket.close()

if __name__ == "__main__":
    args = parser()
    buffer = None

    MyNetCat(args, buffer).run()
