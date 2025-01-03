import icmp_decoder
import ip_decoder
import os
import sys
import socket

OS = os.name

def sniff(host):
    """
        Функция отвечает за создание сокета и получение ответа
    """

    if OS == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if OS == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    try:
        while True:
            buffer = sniffer.recvfrom(65565)[0]
            ip_header = ip_decoder.IP(buffer[:20])
            print(f"{ip_header.src_ip_address}/{ip_header.protocol} -> {ip_header.dst_ip_address}/{ip_header.protocol}")
    except KeyboardInterrupt:
        if OS == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close()
        sys.exit()