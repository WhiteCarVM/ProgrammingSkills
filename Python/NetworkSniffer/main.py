import socket

from sniffer import sniff

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))

    local_ip = sock.getsockname()

    return local_ip[0]

def main():
    host = get_local_ip() 
    print(f"Start of sniffing on {host}\n")
    sniff(host)

if __name__ == "__main__":
    main()