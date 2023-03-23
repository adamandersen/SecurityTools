#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import pydig

debug = 1
filepath ="./hosts_csv"
manual_hosts = [
    "google.com",
    "dr.dk",
    "tv2.dk"
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
    
    for hosts in csvImport(filepath):
        a_record = pydig.query(listToString(hosts), "A")
        txt_record = pydig.query(listToString(hosts), "TXT")
        mx_record = pydig.query(listToString(hosts), "MX")
        ns_record = pydig.query(listToString(hosts), "NS")
        print(f'{hosts};{a_record};{txt_record},{mx_record},{ns_record} \n\n')
