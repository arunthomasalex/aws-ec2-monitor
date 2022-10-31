import os
import socket
import struct
import time
from . import logging

def main(monitor_file, options):
    sel_src_port, sel_dest_port, log, sel_time = options.values()
    logger = logging.get_logger("scanner", log)
    
    with open(monitor_file, 'w') as fp:
        pass
    
    def perform_action(content):
        os.utime(monitor_file, (time.time(), time.time()))
        logger.info(content)

    no_ports = not sel_src_port and not sel_dest_port
    logger.info(f"Source: {sel_src_port}, Destination: {sel_dest_port}")
    logger.info(f"Service will monitor traffic for: {int(sel_time * 3600)} seconds")

    conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(3))
    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        if eth_proto == 8:
            (version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
            if proto == 6:
                (src_port, dest_port, seq, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, content) = tcp_segment(data)
                if no_ports:
                    perform_action(content)
                else:
                    if sel_src_port and src_port == sel_src_port:
                        perform_action(content)
                    if sel_dest_port and dest_port == sel_dest_port:
                        perform_action(content)
                


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

if __name__ == "__main__":
    main('/tmp/.monitor')