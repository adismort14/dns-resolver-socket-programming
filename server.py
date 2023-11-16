from socket import *
import struct

def get_ip_from_file(filename, query_domain):
    with open(filename, 'r') as file:
        for line in file:
            domain, ip_address = line.strip().split()
            if domain == query_domain:
                return ip_address
    return "Domain not found"

def handle_dns_request(transaction_id, query_domain):
    ip_address = get_ip_from_file(filename,query_domain)
    return transaction_id, ip_address

filename = "dns_mapping.txt"

sname='127.0.0.1'
sport=8001

ssocket=socket(AF_INET,SOCK_DGRAM)
ssocket.bind((sname,sport))

while True:
    dns_request_packet, client_address = ssocket.recvfrom(1024)
    transaction_id, query_domain = struct.unpack('!H{}s'.format(len(dns_request_packet) - 2), dns_request_packet)

    response_transaction_id, ip_address = handle_dns_request(transaction_id, query_domain.decode())

    dns_response_packet = struct.pack('!H{}s'.format(len(ip_address)), response_transaction_id, ip_address.encode())
    ssocket.sendto(dns_response_packet, client_address)
    break

ssocket.close()

