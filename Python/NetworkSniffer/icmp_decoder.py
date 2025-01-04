import struct

from termcolor import colored

class ICMP:
    def __init__(self, buffer=None):
        if buffer is None or len(buffer) < 8:
            raise ValueError("Buffer must be at least 8 bytes long")

        try:
            header = struct.unpack("<BBHHH", buffer)
            if len(header) != 5:
                raise ValueError("Unpacked ICMP has incorrect length")
        except Exception as ex:
            print(colored(f"Error: {ex}", "red"))
        
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]
