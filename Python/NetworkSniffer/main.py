import socket
import sys

from sniffer import sniff
from termcolor import colored

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))

            local_ip = sock.getsockname()

        return local_ip[0]
    except Exception as ex:
        print(colored(f"Error: {ex}", "red"))
        print(colored("\nSniffer stoped", "green"))
        sys.exit()

def main():
    host = get_local_ip() 
    print(colored(f"Start of sniffing on {host}", "green"))
    sniff(host)

if __name__ == "__main__":
    main()