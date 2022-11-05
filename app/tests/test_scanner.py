from unittest import TestCase, TestLoader
import app.scanner

raw_data=b'\x00\x00\x00\x00\x00\x00\x11\x11\x11\x11\x11\x11\x08\x00E\x00\x02\x043f@\x00@\x06M\x99y\x00\x00\x01\x79\x00\x00\x02\x98D\x13\x88l\xd7\xd7\xc2Pi`\x89\x80\x18\x02\x00\xb9\xf3\x00\x00\x01\x01\x08\nn\xcf"X\xf0d\xd7\xcdGET / HTTP/1.0\r\nHost: appcluster\r\nConnection: close\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-GB,en-US;q=0.9,en;q=0.8\r\n\r\n'
class TestScanner(TestCase):
    def test_ethernet_frame(self):
        dest_mac, src_mac, eth_proto, _ = app.scanner.ethernet_frame(raw_data)
        self.assertEqual(dest_mac, '00:00:00:00:00:00')
        self.assertEqual(src_mac, '11:11:11:11:11:11')
        self.assertEqual(eth_proto, 8)

    def test_ipv4_packet(self):
        _, _, _, data = app.scanner.ethernet_frame(raw_data)
        version, header_length, ttl, proto, src, target, _ = app.scanner.ipv4_packet(data)
        self.assertEqual(header_length, 20)
        self.assertEqual(proto, 6)
        self.assertEqual(src, '121.0.0.1')
        self.assertEqual(target, '121.0.0.2')

    def test_tcp_segment(self):
         _, _, _, data = app.scanner.ethernet_frame(raw_data)
         _, _, _, _, _, _, data = app.scanner.ipv4_packet(data)
         src_port, dest_port, _, _, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, content = app.scanner.tcp_segment(data)
         self.assertEqual(src_port, 38980)
         self.assertEqual(dest_port, 5000)
         self.assertEqual(flag_urg, 0)
         self.assertEqual(flag_ack, 64)
         self.assertEqual(flag_psh, 24)
         self.assertEqual(flag_rst, 0)
         self.assertEqual(flag_syn, 0)
         self.assertEqual(flag_fin, 0)
         content_str = str(content)
         self.assertIn('GET', content_str)
         self.assertIn('Host: appcluster',content_str)