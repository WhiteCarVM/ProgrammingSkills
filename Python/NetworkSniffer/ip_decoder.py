import ipaddress
import struct

class IP:
    def __init__(self, buffer=None):
        if buffer is None or len(buffer) < 20:
            raise ValueError("Buffer for IP packet must be at least 20 bytes long")

        header = struct.unpack("<BBHHHBBH4s4s", buffer)

        self.version = header[0] >> 4
        self.ihl = header[0] & 0x0f
        self.type_of_service = header[1]
        self.size_of_packet = header[2]
        self.id = header[3]
        self.offset = header[4] & 0x1FFF
        self.more_fragments = bool(header[4] & 0x2000)
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src_ip = header[8]
        self.dst_ip = header[9]

        self.src_ip_address = ipaddress.ip_address(self.src_ip)
        self.dst_ip_address = ipaddress.ip_address(self.dst_ip)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as ex:
            print(f"{ex}: No protocol for {self.protocol_num}")
            self.protocol = str(self.protocol_num)

    def is_fragmented(self):
        return self.more_fragments or self.offset > 0
