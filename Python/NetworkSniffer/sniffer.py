import icmp_decoder
import ip_decoder
import socket
import os
import sys

from termcolor import colored

OS = os.name

def sniff(host):
    if OS == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol) as sniffer:
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if OS == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        try:
            while True:
                ip_buffer = sniffer.recvfrom(65535)[0]

                if len(ip_buffer) < 20:
                    print(f"Received packet is too small (length {len(ip_buffer)}). Ignoring.")
                    continue

                ip_header = ip_decoder.IP(ip_buffer[:20])
                print(f"\n{ip_header.src_ip_address}/{ip_header.protocol} -> {ip_header.dst_ip_address}/{ip_header.protocol}")

                if ip_header.protocol == "ICMP":
                    print(f"IP version: {ip_header.version}, Header length: {ip_header.ihl}, Time to live: {ip_header.ttl}")
                    offset = ip_header.ihl * 4
                    if len(ip_buffer) < offset + 8:
                        print(colored(f"Error: ICMP Buffer is too small (available length is {len(ip_buffer) - offset}).", "red"))
                        continue

                    icmp_buffer = ip_buffer[offset:offset + 8]

                    try:
                        icmp_header = icmp_decoder.ICMP(icmp_buffer)
                        print(f"ICMP type: {icmp_header.type}, ICMP code: {icmp_header.code}")
                    except ValueError as ve:
                        print(colored(f"Error parsing ICMP header: {ve}", "red"))
                        continue
        except KeyboardInterrupt:
            if OS == 'nt':
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            print(colored("\nSniffer stopped.", "green"))
            sys.exit()
