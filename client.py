from socket import *
import struct
import random

sname='127.0.0.1'
sport=8001

def make_dns_request(transaction_id, query_domain):
    server_address = (sname,sport)
    client_socket = socket(AF_INET, SOCK_DGRAM)

    dns_request_packet = struct.pack('!H{}s'.format(len(query_domain)), transaction_id, query_domain.encode())
    client_socket.sendto(dns_request_packet, server_address)

    dns_response_packet, _ = client_socket.recvfrom(2048)
    transaction_id, ip_address = struct.unpack('!H{}s'.format(len(dns_response_packet) - 2), dns_response_packet)

    return transaction_id, ip_address.decode()


transaction_id = random.randint(1,10000)
query_domain = "google.com"

response_transaction_id, response_ip = make_dns_request(transaction_id, query_domain)

print(f"Transaction ID: {response_transaction_id}")
print(f"IP Address for {query_domain}: {response_ip}")
