import dnslib
import socket
from dnslib import DNSRecord, CLASS, QTYPE
from Message_DNS import *

BUFF_SIZE = 4096
ROOT_IP = "192.33.4.12"
DNS_PORT = 53

def dns_parser(dns_message : bytes) -> Message_DNS:
    """ Parsea el mensaje DNS en bytes recibido y retorna una representación del mensaje en un objeto de la clase Message_DNS. """
    dnslib_parsed_message = DNSRecord.parse(dns_message)

    # Se parsea el header
    header_dict = dict()
    header_dict["ANCOUNT"] = dnslib_parsed_message.header.a
    header_dict["NSCOUNT"] = dnslib_parsed_message.header.auth
    header_dict["ARCOUNT"] = dnslib_parsed_message.header.ar

    # Se parsea la sección Question
    first_query = dnslib_parsed_message.get_q()
    qname = str(first_query.get_qname())

    # Se parsea la sección Answer 
    answer_list = list()
    if header_dict["ANCOUNT"] > 0:
        for answer in dnslib_parsed_message.rr:
            answer_dict = dict()
            answer_dict["NAME"] = str(answer.get_rname())
            answer_dict["TTL"] = int(answer.ttl)
            answer_dict["RCLASS"] = str(CLASS.get(answer.rclass))
            answer_dict["RTYPE"] = str(QTYPE.get(answer.rtype))
            answer_dict["RDATA"] = str(answer.rdata)
            answer_list.append(answer_dict)

    # Se parsea la sección Authority
    auth_list = list()
    if header_dict["NSCOUNT"] > 0:
        for auth in dnslib_parsed_message.auth:
            auth_dict = dict()
            auth_dict["NAME"] = str(auth.get_rname())
            auth_dict["TTL"] = int(auth.ttl)
            auth_dict["RCLASS"] = str(CLASS.get(auth.rclass))
            auth_dict["RTYPE"] = str(QTYPE.get(auth.rtype))
            auth_dict["RDATA"] = str(auth.rdata)
            auth_list.append(auth_dict)

    # Se parsea la sección Additional
    add_list = list()
    if header_dict["ARCOUNT"] > 0:
        for add in dnslib_parsed_message.ar:
            add_dict = dict()
            add_dict["TTL"] = int(add.ttl)
            add_dict["RCLASS"] = str(CLASS.get(add.rclass))
            add_dict["RTYPE"] = str(QTYPE.get(add.rtype))
            if add_dict["RTYPE"] == 'A':
                add_dict["NAME"] = str(add.rname)
                add_dict["RDATA"] = str(add.rdata)
            add_list.append(add_dict)

    return Message_DNS(header_dict, qname, answer_list,auth_list, add_list)


def resolver(mensaje_consulta : bytes) -> bytes:
    
    address = (ROOT_IP, DNS_PORT)
    resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        resolver_socket.sendto(mensaje_consulta, address)
        root_answer, _ = resolver_socket.recvfrom(BUFF_SIZE)
        dns_message = dns_parser(root_answer)

        if dns_message.has_type_A_answer():
            resolver_socket.close()
            return root_answer

        type_NS_auth = dns_message.first_type_NS_auth()
        if type_NS_auth is not None:
            type_A_add = dns_message.first_type_A_add()

            if type_A_add is not None:
                address = (type_A_add["RDATA"], DNS_PORT)
            
            else:
                ns_query = DNSRecord.question(type_NS_auth["RDATA"])
                ns_answer_bytes = resolver(bytes(ns_query.pack()))
                dns_NS_response = dns_parser(ns_answer_bytes)
                ns_answer = dns_NS_response.get_resolved_answer()
                address = (ns_answer["RDATA"], DNS_PORT)

        else:
            return None
        
