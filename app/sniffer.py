import socket
import struct
import textwrap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '

def main():
    conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(3))
    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print('\n Ethernet Frame:')
        print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'. format(dest_mac, src_mac, eth_proto))
        if eth_proto == 8:
            (version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
            print(TAB_1 + 'IPv4 Packet:')
            print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {}'.format(version, header_length, ttl))
            print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
            if proto == 1:
                icmp_type, code, check_sum, content = icmp_packet(data)
                print(TAB_1 + 'ICMP Packet:')
                print(TAB_2 + 'Type: {}, Code: {}, Checksum: {}'.format(icmp_type, code, check_sum))
                print(TAB_2 + 'Data: {}')
                print(format_multi_line(DATA_TAB_3, data))
            elif proto == 6:
                (src_port, dest_port, seq, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, content) = tcp_segment(data)
                print(TAB_1 + 'TCP Segment:')
                print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
                print(TAB_2 + 'Sequence: {}, Acknowledgement: {}'.format(seq, ack))
                print(TAB_2 + 'Flags:')
                print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, , FIN: {}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
                print(TAB_2 + 'Data:')
                print(format_multi_line(DATA_TAB_3, content))
            elif proto == 17:
                src_port, dest_port, size, content = udp_segment(data)
                print(TAB_1 + 'UDP Segment:')
                print(TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, size))
            else:
                print(TAB_1 + 'Data:')
                print(format_multi_line(DATA_TAB_2, content))
        else:
            print('Data:')
            print(format_multi_line(DATA_TAB_1, data))

def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]

def get_mac_addr(bytes_addr):
    return ':'.join(map('{:02x}'.format, bytes_addr)).upper()

def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15)  * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]

def ipv4(addr):
    return '.'.join(map(str, addr))

def icmp_packet(data):
    icmp_type, code, check_sum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, check_sum, data[4:]

def tcp_segment(data):
    (src_port, dest_port, seq, ack, off_flag) = struct.unpack('! H H L L H', data[:14])
    offset = (off_flag >> 12) * 4
    flag_urg = (off_flag & 32) * 5
    flag_ack = (off_flag & 16) * 4 
    flag_psh = (off_flag & 8) * 3
    flag_rst = (off_flag & 4) * 2 
    flag_syn = (off_flag & 2) * 1 
    flag_fin = (off_flag & 1)
    return src_port, dest_port, seq, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]

def udp_segment(data):
    src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
    return src_port, dest_port, size, data[8:]

def format_multi_line(prefix, data, size=80):
    size -= len(prefix)
    if isinstance(data, bytes):
        content = ''.join(bytes.fromhex(r'{:02x}'.format(byte)).decode() for byte in data)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(content, size)])

if __name__ == "__main__":
    main()