import socket
import termcolor
import threading
import tqdm
import argparse
import ipaddress

# Function to log results to a file
def log_result(message):
    with open("scan_results.txt", "a") as f:
        f.write(message + "\n")

# Function to scan a single TCP port
def scan_port(ip_add, port):
    try:
        sock = socket.socket()
        sock.settimeout(0.5)
        sock.connect((ip_add, port))
        try:
            banner = sock.recv(1024).decode().strip()
            result = f"[+] Port {port} is open: {banner}"
        except:
            result = f"[+] Port {port} is open"
        print(termcolor.colored(result, "green"))
        log_result(result)
        sock.close()
    except:
        pass

# Function to scan a single UDP port
def scan_udp_port(ip_add, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b"", (ip_add, port))
        sock.recvfrom(1024)
        result = f"[+] UDP Port {port} is open"
        print(termcolor.colored(result, "blue"))
        log_result(result)
        sock.close()
    except:
        pass

# Function to scan ports for a target
def scan(target, port_range, protocol="tcp"):
    print(f"\nStarting scan for {target}")
    threads = []
    for p in tqdm.tqdm(range(1, port_range + 1), desc="Scanning"):
        if protocol == "tcp":
            t = threading.Thread(target=scan_port, args=(target, p))
        elif protocol == "udp":
            t = threading.Thread(target=scan_udp_port, args=(target, p))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Main function
def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("target", help="Target IP or domain (comma-separated for multiple targets)")
    parser.add_argument("port", type=int, help="Port range to scan (e.g., 1000 for 1-1000)")
    parser.add_argument("--protocol", choices=["tcp", "udp"], default="tcp", help="Protocol to scan (default: TCP)")
    parser.add_argument("--common", action="store_true", help="Scan only common ports")
    args = parser.parse_args()

    targets = args.target.split(',')
    port_range = args.port
    protocol = args.protocol

    # Validate IP addresses
    for target in targets:
        try:
            ipaddress.ip_address(target.strip())
        except ValueError:
            print(termcolor.colored(f"Invalid IP address: {target}", "red"))
            return

    # Common ports
    common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
    if args.common:
        port_range = len(common_ports)

    # Scan targets
    for target in targets:
        target = target.strip()
        if args.common:
            print(f"\nScanning common ports for {target}")
            for port in common_ports:
                if protocol == "tcp":
                    scan_port(target, port)
                elif protocol == "udp":
                    scan_udp_port(target, port)
        else:
            scan(target, port_range, protocol)

if __name__ == "__main__":
    main()

