import chime
import os, requests
import math
import time
import ecdsa
import sys
import smtplib
import binascii
import multiprocessing
import ssl
from bitcoinlib.keys import HDKey
from bitcoinlib.services.services import Service
import numpy as np
chime.theme('sonic')

def check_balance(i, address):
    confirmed = 0
    unconfirmed = 0
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = '{"jsonrpc":"2.0","id":"curltext","method":"getaddressbalance","params":["%s"]}' % (address)
    response = requests.post('http://127.0.0.1:7777', headers=headers, data=data, auth=('user', 'LEOJYI0ZHq9cjHMDGCEGAw=='))
    print(response.text)
    try:
        confirmed = float(response.json()['result']['confirmed'])
        unconfirmed = float(response.json()['result']['unconfirmed'])
        res = str(response.json()['result'])
    except KeyError:
        print("Error in Result, Wait 30 seconds")
        res = str(response.json()['error'])
        time.sleep(30)
    except: 
        print("Error occured ...., Wait 30 seconds")
        time.sleep(30)
    if confirmed>0 or unconfirmed>0:
        chime.success()
        print("Found ",address)
        fl = open("./Wallets_balance.txt", "a")
        fl.write(address+","+str(confirmed)+"\n")
        fl.close()            
    print(str(i)+" ---- "+address+"---"+ str(confirmed)+"  --- "+str(unconfirmed)+'---'+res+"\n")

# Path to the text file containing Bitcoin addresses (one address per line)
file_path = "found.txt"
# b = np.loadtxt(file_path, dtype=str)
i = 1
cnt=0
while True:
    filename = 'found.txt'
    with open(file_path, 'r') as f:
        addresses = f.read().splitlines()
        for address in addresses:
            if('Address' in address):
                cnt+=1
                d = address.split(' ')[1]
                print(d)
                check_balance(cnt, d)
    i = i + 1


# with open(file_path, "r") as file:
#     addresses = file.read().splitlines()
# i=0
# for address in addresses:
#     i+=1
#     check_balance(i, address)