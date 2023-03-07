#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket, ssl
import csv
from colorama import Style
from colorama import Fore


######## Configuration ###########
#
# SSL/TLS port
# Adjust socket connection timeout
timeout = 0.01
# Output debug information to console
debug = 1
# Path to csv [True or 1] - [False or 0]
fileimport = False
filepath ="c:\\temp\hosts_csv"
# Use single or multiple hosts without fileimport
manual_hosts = [
    'cloudflare.com',
    'google.com',
    'duckduckgo.com',
    'bing.com'
]
# Match certificate name [True or 1] - [False or 0]
cert_match = False
cert_name = 'google.com'
#
######## Configuration ###########

def csvImport(path):
    hosts = []
    try:
        with open(path, 'r') as importfile:
            readhosts = csv.reader(importfile)
            for host in readhosts:
                hosts.append(host)
        
    except Exception as e:
        match debug:
            case 1:
                textInfo(f"DANGER WILL ROBINSON: {e}",1)
    return hosts

def textInfo(text, category):
    match category:
        case 0 | "info":
            print(f'{Style.BRIGHT}{Fore.BLUE}[*] INFO....: {text}{Style.RESET_ALL}')
        case 1 | "warning":
            print(f'{Style.BRIGHT}{Fore.YELLOW}[#] WARNING.: {text}{Style.RESET_ALL}')
        case 3 | "alert":
            print(f'{Style.BRIGHT}{Fore.RED}[!] Alert...: {text}{Style.RESET_ALL}')

def sslConnections(host, port=443):    

    context = ssl.create_default_context()
    # Use Python3.10 > PROTOCOL_TLS_CLIENT
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Hostname certificate verify for mismatch True|False
    context.check_hostname = False
    context.load_default_certs()
    
    # Create connection socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Socket timeout
    sock.settimeout(timeout) 
    # SSL Wrap
    sslsock = context.wrap_socket(sock, server_hostname=host)
    
    # Certificate infromation list
    certInfo = []
    try:
        
        # Request SSL socket connection
        sslsock.connect((host, port))
        # Request SSL certificate 
        cert = sslsock.getpeercert()
        
        # Request IPaddresse information
        hostaddr = socket.getaddrinfo(host, port)[0][4][0]
        
        # Grab the first CN/CommonName from the SSL certificate
        for cn in cert['subject']:
                if debug == 2:
                    print(f'Host:{host} \tCommonName:{cn[0][1]}')
                # Appened only first CommonName to list
                cnname = cn[0][1]
                match cert_match:
                    case 0 | False:
                        certInfo.append(cn[0][1])
                    case 1 | True:
                        if cnname == cert_name:
                            certInfo.append(cn[0][1])           
        # Close connection
        sslsock.close
        # Return the live information   
        for info in certInfo:
            textInfo(f'URL: {host} CommonName: {info},  IPaddress: {hostaddr} CertificateExpire: {cert.get("notAfter")}', 0)

    except socket.timeout:
        match debug:
            case 1:
                textInfo(f'DANGER WILL ROBINSON Socket timeout for {host} port {port} timeout {sock.gettimeout()}', 3)
        return None
    except Exception as e:
        match debug:
            case 1:
                textInfo(f'DANGER WILL ROBINSON {e} AFFECTED HOST:: {host}', 1)


if __name__ == "__main__":

    try:      

        match fileimport:
            case 1 | True:
                host_csvimport = csvImport(filepath)
                for host in host_csvimport:
                    sslConnections(host[0])
                textInfo(f'Noting more to do..', 0)
            case 0 | False:
                host_import = manual_hosts
                for host in host_import:
                    sslConnections(host)
                textInfo(f'Noting more to do..', 0)

    except KeyboardInterrupt:
        textInfo(f'User interrupted Exiting ...', 1)        
    except Exception as e:
        match debug:
            case 1:
                textInfo(f"DANGER WILL ROBINSON: {e}",1)
