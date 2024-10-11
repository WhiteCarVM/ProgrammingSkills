import sys
import time
import socket
import datetime

def PortScanner(target_ips, target_ports):
    """
        Функиця реализации сканера портов. Я бы хотел добавить больше функций. ДОПИСАТЬ!!!
    """
    results = []
    
    for target in target_ips.split(","):
        try:
            ScanPort(target, target_ports, results)
        except:
            pass
        
    return results

def ScanPort(target:str, ports:str, results):
    """
        Функция сканирования одного порта и вывода результатов сканирования.
    """
    if "-" in ports:
        ports = ports.split("-")
        for port in range(int(ports[0]), int(ports[1])+1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, port))
                service = socket.getservbyport(port)
                results.append([port, "open", service])
                sock.close()
            except:
                pass
    else:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target, int(ports)))
            service = socket.getservbyport(int(ports))
            results.append([int(ports), "open", service])
            sock.close()
        except:
            pass