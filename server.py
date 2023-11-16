from socket import *
import struct

dns_mapping = {
    "example.com": "192.168.1.1",
    "google.com": "8.8.8.8",
    "yahoo.com": "98.138.219.231",
    "github.com": "192.30.255.113",
    "openai.com": "52.44.42.29",
}

def resolve_dns(query_domain):
    return dns_mapping.get(query_domain, "Domain not found")

def handle_dns_request(transaction_id, query_domain):
    ip_address = resolve_dns(query_domain)
    return transaction_id, ip_address

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

