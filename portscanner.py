import socket
import termcolor
# import time


def scan(target,port):
    print('\n'+"Starting scan for "+target)
    for p in range(1,port):
        scan_port(target,p)

def scan_port(ip_add,port):
    try:
        sock = socket.socket()
        sock.connect((ip_add, port))
        print(f"[+]Port {port} is open")
        sock.close()
    except:
        print(f"[-]Port {port} is closed")


target = input("Enter target IP:")
port = int(input("Enter port to scan:"))
if  ","  in target:
    print(termcolor.colored(("[+]Scanning mutliple targets"),green))
    for ip_addr in target.split(','):
        scan(ip_addr.strip(' '),port)
else:
    print("[+]Scanning single target")
    scan(target,port)
