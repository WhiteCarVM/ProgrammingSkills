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
            ip_buffer = sniffer.recvfrom(65565)[0]
            ip_header = ip_decoder.IP(ip_buffer[:20])
            print(f"\n{ip_header.src_ip_address}/{ip_header.protocol} -> {ip_header.dst_ip_address}/{ip_header.protocol}")
            if ip_header.protocol == "ICMP":
                print(f"IP version: {ip_header.version}, Header length: {ip_header.size_of_header}, Time to live: {ip_header.ttl}")

                offset = ip_header.size_of_header
                icmp_buffer = ip_buffer[offset:offset+8]      
                #Здесь проблема, связанная с буфером
                icmp_header = icmp_decoder.ICMP(icmp_buffer)
                print(f"ICMP type: {icmp_header.type}, ICMP code: {icmp_header.code}")
    except KeyboardInterrupt:
        if OS == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close()
        sys.exit()