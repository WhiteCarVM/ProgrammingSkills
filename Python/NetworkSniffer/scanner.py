import icmp_decoder
import ipaddress
import ip_decoder
import os
import socket
import scapy.all as scapy
import sys
import threading

from termcolor import colored

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception as ex:
        print(colored(f"Error getting local IP: {ex}", "red"))
        sys.exit(1)

def get_subnet():
    subnet_mask = '24' # CHANGE IT
    local_ip = get_local_ip().split('.')
    local_ip[3] = '0'
    return '.'.join(local_ip) + "/" + subnet_mask

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answer:
        return answer[0][1].hwsrc
    return "Unknown"

def get_os(ttl):
    if ttl <= 64:
        return "Linix/Unix"
    elif ttl <= 128:
        return "Windows"
    elif ttl <= 225:
        return "Cisco/Network device"
    return "Unkmown"

def arp_scan(subnet):
    arp_request = scapy.ARP(pdst=subnet)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    hosts = []
    for answer in answered_list:
        hosts.append({"ip": answer.psrc, "mac": answer.hwsrc})

    return hosts


HOST = get_local_ip()
OS = os.name
SUBNET = get_subnet()
TEST_MESSAGE = "TEST_HOST"

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sock.sendto(bytes(TEST_MESSAGE, 'utf-8'), (str(ip), 65212))

"""
def udp_sender():
    def send_udp(ip):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(bytes(TEST_MESSAGE, 'utf-8'), (str(ip), 65212))

        threads = []
        for ip in ipaddress.ip_network(SUBNET).hosts():
            th = threading.Thread(target=send_udp, args=(ip,))
            th.start()
            threading.append(th)

        for thread in threads:
            thread.join()
"""

class Scanner:
    def __init__(self, host):
        self.host = host

        if OS == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
            self.socket.bind((host, 0))
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            if OS == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except PermissionError:
                print(colored("Error: Permission denied. Run program as administrator"), "red")
                sys.exit(1)
        except Exception as ex:
                print(colored(f"Error:{ex}"),"red")
                sys.exit(1)

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
                                        mac_address = get_mac(target)
                                        os_name = get_os(ip_header.ttl)
                                        hosts_up.add(target)
                                        print(f"{target}: {os_name}, {mac_address}")
                    except ValueError as ve:
                        print(colored(f"Error parsing ICMP header: {ve}", "red"))
                        continue
        except KeyboardInterrupt:
            if OS == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print(colored("\nSniffer stopped.", "green"))
            sys.exit()
