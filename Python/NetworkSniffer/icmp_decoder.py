import struct

class ICMP:
    def __init__(self, buffer=None):
        if buffer is None or len(buffer) < 8:
            raise ValueError("Buffer must be at least 8 bytes long")

        header = struct.unpack("<BBHHH", buffer)
        
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]
