import socket

from sniffer import sniff

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))

    local_ip = sock.getsockname()

    return local_ip[0]

HOST = get_local_ip()

def main():
    """
        Функция отвечает за пользовательский ввод
    """

    # добавить фильтрацию входных данных
    global HOST
    HOST = input("Enter target host\n> ")


if __name__ == "__main__":
    main()
    sniff(HOST)