import socket
import os

OS = os.name
# добавить фильтрацию входных данных
HOST = input("Enter target host\n> ")

def main():
    """
        Функция отвечает за создание сокета и получение ответа
    """

    if OS == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if OS == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    print(sniffer.recvfrom(65565))

    if OS == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    sniffer.close()

if __name__ == "__main__":
    main()