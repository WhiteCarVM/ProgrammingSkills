import icmp_decoder
import ip_decoder
import ipaddress
import socket
import os
import sys
import time

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

def get_subnet():
    subnet_mask = '24' # CHANGE IT
    local_ip = get_local_ip().split('.')
    local_ip[3] = '0'
    return '.'.join(local_ip) + "/" + subnet_mask

HOST = get_local_ip()
OS = os.name
SUBNET = get_subnet()
TEST_MESSAGE = "TEST_HOST"

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sock.sendto(bytes(TEST_MESSAGE, 'utf-8'), (str(ip), 65212))

class Scanner:
    def __init__(self, host):
        self.host = host

        if OS == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if OS == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    def sniff(self):
        hosts_up = set([f'{str(self.host)} *'])
        print(f"\tHosts up on {SUBNET}:")
        print(f"{self.host} *")
        try:
            while True:
                ip_buffer = self.socket.recvfrom(65535)[0]

                if len(ip_buffer) < 20:
                    print(f"Received packet is too small (length {len(ip_buffer)}). Ignoring.")
                    continue

                ip_header = ip_decoder.IP(ip_buffer[:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    if len(ip_buffer) < offset + 8:
                        print(colored(f"Error: ICMP Buffer is too small (available length is {len(ip_buffer) - offset}).", "red"))
                        continue

                    icmp_buffer = ip_buffer[offset:offset + 8]

                    try:
                        icmp_header = icmp_decoder.ICMP(icmp_buffer)

                        if icmp_header.code == 3 and icmp_header.type == 3:
                            if ipaddress.ip_address(ip_header.src_ip_address) in ipaddress.IPv4Network(SUBNET):
                                if ip_buffer[len(ip_buffer) - len(TEST_MESSAGE):] == bytes(TEST_MESSAGE, 'utf-8'):
                                    target = str(ip_header.src_ip_address)
                                    if target != self.host and target not in hosts_up:
                                        hosts_up.add(target)
                                        print(f"{target}")
                    except ValueError as ve:
                        print(colored(f"Error parsing ICMP header: {ve}", "red"))
                        continue
        except KeyboardInterrupt:
            if OS == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print(colored("\nSniffer stopped.", "green"))
            sys.exit()
