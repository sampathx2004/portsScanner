import os
import subprocess
import sys

# Function to install missing modules
def install_missing_modules(module_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"[+] Successfully installed {module_name}")
    except Exception as e:
        print(f"[-] Failed to install {module_name}. Error: {e}")

# Ensure required modules are installed
try:
    import socket
    import termcolor
    import threading
    import argparse
except ModuleNotFoundError as e:
    missing_module = str(e).split("'")[1]
    print(f"[-] Module '{missing_module}' not found. Attempting to install...")
    install_missing_modules(missing_module)
    print("[+] Restart the script after installation.")
    sys.exit()

# Function to scan a single TCP port
def scan_port(ip_add, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Increased timeout
        sock.connect((ip_add, port))
        print(f"[DEBUG] Successfully connected to port {port}")
        try:
            banner = sock.recv(1024).decode().strip()
            result = f"[+] Port {port} is open: {banner}"
        except:
            result = f"[+] Port {port} is open"
        print(termcolor.colored(result, "green"))
        sock.close()
    except socket.timeout:
        print(f"[DEBUG] Port {port} is closed or unreachable. Error: timeout")
    except Exception as e:
        print(f"[DEBUG] Port {port} is closed or unreachable. Error: {e}")

# Function to scan a range of ports for a target
def scan(target, port_range):
    print(termcolor.colored(f"\nStarting scan for {target}", "cyan"))
    threads = []
    for port in range(1, port_range + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Main function to handle user input and initiate scanning
def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address or domain name")
    parser.add_argument("port_range", type=int, help="Range of ports to scan (e.g., 1000 for 1-1000)")
    args = parser.parse_args()

    target = args.target
    port_range = args.port_range

    # Validate the target
    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print(termcolor.colored(f"[-] Invalid target: {target}", "red"))
        return

    # Start scanning
    scan(target, port_range)

if __name__ == "__main__":
    main()
