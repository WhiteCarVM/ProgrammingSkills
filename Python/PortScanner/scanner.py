import sys
import socket
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - $(message)s")

def parse_ports(port_range):
    """
        Парсинг портов, возвращение списка

        СОЗДАТЬ ТАКУЮ ЖЕ ДЛЯ IP АДРЕССОВ!!!
    """
    try:
        if "-" in port_range:
            start, end = map(int, port_range.split("-"))
            return list(range(start, end+1))
        elif "," in port_range:
            port_range = list(map(int, port_range.split(",")))
            return port_range
        else:
            return [int(port_range)]
    except ValueError as val_err:
        logging.error(f"Invalid format of ports input: {val_err}")
        return []

def TCPscan(target_ips, target_ports):
    """
        Функция реализующая TCP сканирование
    """
    target_results = dict()
    
    for target in target_ips.split(","):
        results = []
        ports = parse_ports(target_ports)
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target, port))
                service = socket.getservbyport(port)
                results.append([f"{port}\\tcp", "open", service])
                sock.close()
            except (socket.timeout, ConnectionRefusedError):
                continue
            except Exception as ex:
                logging.warning("Scanning error: {ex}")
        target_results[target] = results
    
    return target_results

def UDPscan(target_ips, target_ports):
    """
        Функция, реализующая UDP сканирование 
    """
    target_results = dict()
    
    for target in target_ips.split(","):
        target = target.strip()
        results = []
        ports = parse_ports(target_ports)
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.connect((target, port))
                sock.sendto(b'', (target, port))
                sock.recv(1024)
                service = socket.getservbyport(port)
                results.append([f"{port}\\udp", "open", service])
                sock.close()
            except socket.timeout:
                continue
            except Exception as ex:
                logging.warning(f"Scanning error: {ex}")
        target_results[target] = results
    
    return target_results