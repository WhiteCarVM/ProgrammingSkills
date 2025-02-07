import sys
import socket
import logging
import ipaddress
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_ips(ip_range):
    """
    Парсинг IP адресов, возвращение списка адресов.
    """
    ip_list = []
    try:
        if "/" in ip_range:
            network = ipaddress.ip_network(ip_range, strict=False)
            ip_list = [str(ip) for ip in network.hosts()]
        elif "-" in ip_range:
            start, end = ip_range.split("-")
            fourth_octet1 = list(map(int, start.split(".")))
            fourth_octet2 = list(map(int, end.split(".")))
            for i in range(fourth_octet1[3], fourth_octet2[3] + 1):
                ip_list.append(f"{fourth_octet1[0]}.{fourth_octet1[1]}.{fourth_octet1[2]}.{i}")
        elif "," in ip_range:
            ip_list = [ip.strip() for ip in ip_range.split(",")]
        else:
            ip_list.append(ip_range.strip())
    except ValueError as val_err:
        logging.error(f"Invalid format of IP addresses input: {val_err}")
        return []

    return ip_list

def parse_ports(port_range):
    """
    Парсинг портов, возвращение списка.
    """
    try:
        if "-" in port_range:
            start, end = map(int, port_range.split("-"))
            return list(range(start, end + 1))
        elif "," in port_range:
            return list(map(int, port_range.split(",")))
        else:
            return [int(port_range)]
    except ValueError as val_err:
        logging.error(f"Invalid format of ports input: {val_err}")
        return []

def scan_port(target, port, protocol):
    """
    Функция, реализующая сканирование одного порта.
    """
    result = []
    try:
        if protocol == 'tcp':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.connect((target, port))
                service = socket.getservbyport(port)
                result = [f"{port}\\tcp", "open", service]
        elif protocol == 'udp':
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(b'', (target, port))
                sock.recv(1024)
                service = socket.getservbyport(port)
                result = [f"{port}\\udp", "open", service]
    except socket.timeout:
        result = [f"{port}\\{protocol}", "closed", "N/A"]
    except (ConnectionRefusedError, OSError):
        result = [f"{port}\\{protocol}", "closed", "N/A"]
    except Exception as ex:
        logging.error(f"Error scanning {protocol} port {port} on {target}: {ex}")

    return target, result

def scan_ports(target_ips, target_ports, protocol):
    """
    Функция, реализующая многопоточность в приложении при сканировании.
    """
    target_ips = parse_ips(target_ips)

    ports = [target_ports]
    target_results = defaultdict(list)
    ports = parse_ports(target_ports)

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(scan_port, str(target), port, protocol): target
            for target in target_ips for port in ports
        }

        for future in as_completed(futures):
            target, result = future.result()
            target_results[target].append(result)
    return {target: results for target, results in target_results.items() if results}

def TCPscan(target_ips, target_ports):
    """
    Функция реализующая TCP сканирование.
    """
    return scan_ports(target_ips, target_ports, "tcp")

def UDPscan(target_ips, target_ports):
    """
    Функция реализующая UDP сканирование.
    """
    return scan_ports(target_ips, target_ports, "udp")