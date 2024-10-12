import sys
import time
import socket
import datetime

def parse_ports(port_range):
    try:
        if "-" in port_range:
            start, end = map(int, port_range.split("-"))
            return list(range(start, end+1))
        else:
            return [int(port_range)]
    except Exception as ex:
        print(f"Exception: {ex}")

def TCPscan(target_ips, target_ports):
    target_results = dict()
    
    try:
        for target in target_ips.split(","):
            try:
                results = []
                ports = parse_ports(target_ports)
                for port in ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((target, port))
                        service = socket.getservbyport(port)
                        results.append([f"{port}\\tcp", "open", service])
                        sock.close()
                    except Exception as ex:
                        print(f"Exception1: {ex}")
                target_results[target] = results
            except Exception as ex:
                print(f"Exception2: {ex}")
    except Exception as ex:
        print(f"Exveption3: {ex}")
    
    return target_results

def UDPscan(target_ips, target_ports):
    target_results = dict()
    
    for target in target_ips.split(","):
        try:
            results = []
            ports = parse_ports(target_ports)
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.connect((target, port))
                    service = socket.getservbyport(port)
                    results.append([f"{port}\\udp", "open", service])
                    sock.close()
                except Exception as ex:
                    print(f"Exception: {ex}")
            target_results[target] = results
        except:
            pass
    
    return target_results
