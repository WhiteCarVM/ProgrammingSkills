import sys
import time
import socket
import datetime

def TCPscan(target_ips, target_ports):
    """
        Функция, реализующая TCP сканнирование
    """
    target_results = dict()
    
    for target in target_ips.split(","):
        try:
            results = []
            def scan_port(target:str, ports:str, results):
                """
                    Функция сканирования одного порта и вывода результатов сканирования.
                """
                if "-" in ports:
                    ports = ports.strip().split("-")
                    for port in range(int(ports[0]), int(ports[1])+1):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.connect((target, port))
                            service = socket.getservbyport(port)
                            results.append([f"{port}\\tcp", "open", service])
                            sock.close()
                        except Exception as ex:
                            print(f"Exception: {ex}")
                else:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((target, int(ports)))
                        service = socket.getservbyport(int(ports))
                        results.append([f"{ports}\\tcp", "open", service])
                        sock.close()
                    except:
                        pass
            scan_port(target, target_ports, results)
            target_results[target] = results
        except:
            pass
    
    return target_results

def UDPscan(target_ips, target_ports):
    """
        Функция, реализующая UDP сканнирование
    """
    target_results = dict()
    
    for target in target_ips.split(","):
        try:
            results = []
            def scan_port(target:str, ports:str, results):
                """
                    Функция сканирования одного порта и вывода результатов сканирования.
                """
                if "-" in ports:
                    ports = ports.strip().split("-")
                    for port in range(int(ports[0]), int(ports[1])+1):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.connect((target, port))
                            service = socket.getservbyport(port)
                            results.append([f"{port}\\udp", "open", service])
                            sock.close()
                        except Exception as ex:
                            print(f"Exception: {ex}")
                else:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.connect((target, int(ports)))
                        service = socket.getservbyport(int(ports))
                        results.append([f"{ports}\\udp", "open", service])
                        sock.close()
                    except:
                        pass
            scan_port(target, target_ports, results)
            target_results[target] = results
        except:
            pass
    
    return target_results