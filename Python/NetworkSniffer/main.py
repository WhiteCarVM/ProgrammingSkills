import scanner
import socket
import sys
import threading
import time

from termcolor import colored

def main():
    print(colored(f"Start of sniffing on {scanner.SUBNET} (Ctrl+C to exit)", "green"))
    print(colored('You can change subnet mask in scanner.py file\n', 'blue'))
    
    sc = scanner.Scanner(scanner.HOST)
    time.sleep(5)
    th = threading.Thread(target=scanner.udp_sender)
    th.start()
    sc.sniff()

if __name__ == "__main__":
    main()