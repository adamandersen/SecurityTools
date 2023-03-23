#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import pydig

debug = 1
filepath ="./hosts_csv"
manual_hosts = [
    #"google.com",
    "dr.dk"
]


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

        with open('output.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file, dialect="excel", delimiter=";")
            writer.writerow(["url_host", "a_record", "ns_record", "mx_record", "txt_record"])

            for hosts in csvImport(filepath):
                a_record = pydig.query(listToString(hosts), "A")
                ns_record = pydig.query(listToString(hosts), "NS")
                mx_record = pydig.query(listToString(hosts), "MX")
                txt_record = pydig.query(listToString(hosts), "TXT")      
                writer.writerow([hosts, a_record, ns_record, mx_record, txt_record]) 
            
            output_file.close()
    except Exception as e:
        print(f"DANGER WILL ROBINSON: {e}")