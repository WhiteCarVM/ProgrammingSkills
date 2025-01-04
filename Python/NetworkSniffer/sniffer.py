def sniff(host):
    if OS == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if OS == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    try:
        while True:
            ip_buffer = sniffer.recvfrom(65535)[0]
            ip_header = ip_decoder.IP(ip_buffer[:20])
            print(f"\n{ip_header.src_ip_address}/{ip_header.protocol} -> {ip_header.dst_ip_address}/{ip_header.protocol}")
            if ip_header.protocol == "ICMP":
                print(f"IP version: {ip_header.version}, Header length: {ip_header.ihl}, Time to live: {ip_header.ttl}")

                offset = ip_header.ihl * 4
                icmp_buffer = ip_buffer[offset:offset+8]
                
                if len(icmp_buffer) < 8:
                    print(f"Error: ICMP Buffer is too small(length is {len(icmp_buffer)}), possibly due to fragmentation or an incomplete packet.")
                    continue
                
                try:
                    icmp_header = icmp_decoder.ICMP(icmp_buffer)
                    print(f"ICMP type: {icmp_header.type}, ICMP code: {icmp_header.code}")
                except ValueError as ve:
                    print(f"Error: {ve}")
                    continue
    except KeyboardInterrupt:
        if OS == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close()
        sys.exit()
