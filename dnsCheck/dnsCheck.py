#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LICENSED under GPLv3 - Copyright (C) 2023 Adam Andersen, adam.andersen[at]pm.me
# check domain DNS records and explort the results

# TODO:
#

import csv
import pydig

importfile ="hosts.csv"
exportfile ='export.csv'
debug = 1

def csvImport(path):
    hosts = []
    try:
        with open(path, 'r') as importfile:
            readhosts = csv.reader(importfile)
            for host in readhosts:
                hosts.append(host)

            importfile.close()
        
    except Exception as e:
        match debug:
            case 1:
                print(f"DANGER WILL ROBINSON: {e}")
    return hosts

def listToString(s):
    string = ""
    for element in s:
        string += element

    return string


if __name__ == "__main__":  
    
    try:

        with open(exportfile, 'w', newline='') as output_file:
            writer = csv.writer(output_file, dialect="excel", delimiter=";")
            writer.writerow(["url_host", "a_record", "cname_record", "ns_record", "mx_record", "txt_record"])

            for hosts in csvImport(importfile):
                a_record = pydig.query(listToString(hosts), "A")
                cname_record = pydig.query(listToString(hosts), "CNAME")
                ns_record = pydig.query(listToString(hosts), "NS")
                mx_record = pydig.query(listToString(hosts), "MX")
                caa_record = pydig.query(listToString(hosts), "CAA")
                txt_record = pydig.query(listToString(hosts), "TXT")
                soa_record = pydig.query(listToString(hosts), "SOA") 
                writer.writerow([hosts, a_record, cname_record, ns_record, mx_record, caa_record,txt_record, soa_record]) 

                print(hosts, a_record, cname_record, ns_record, mx_record, caa_record, txt_record, soa_record)
            
            
            output_file.close()
    except Exception as e:
        print(f"DANGER WILL ROBINSON: {e}")