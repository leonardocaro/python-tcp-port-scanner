#!/usr/bin/env python3

import socket
import re
import datetime
import sys

def get_ip_address():
    while True:
        host = input("Enter the hostname or IP address of the machine you want to scan: ").strip()

        if host == "":
            print("Hostname or IP address cannot be empty. Try again.")
            continue

        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            print("Hostname could not be resolved. Try again.")
            continue


def get_port_range():
    pattern = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")

    while True:
        port_range = input("Enter port range (e.g. 60-120): ")
        match = pattern.fullmatch(port_range)

        if not match:
            print("Invalid format. Use MIN-MAX, e.g. 60-120.")
            continue

        port_min, port_max = map(int, match.groups())

        if not (1 <= port_min <= 65535 and 1 <= port_max <= 65535):
            print("Ports must be between 1 and 65535.")
            continue

        if port_min > port_max:
            print("The minimum port must not exceed the maximum.")
            continue

        return port_min, port_max


def scan(ip_address, port_min, port_max):
    open_ports = []

    for port in range(port_min, port_max + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                
                if s.connect_ex((ip_address, port)) == 0:
                    open_ports.append(port)

        except OSError as error:
            print(f"Socket error on port {port}: {error}")
            continue

    return open_ports


def display_results(open_ports):
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"Port {port}: open.")
    else:
        print("\nNo open ports found.")


def display_duration(start_time):
    elapsed = datetime.datetime.now()
    print(f"\nScan completed in {elapsed - start_time}.")


def main():
    try: 
        print("\033[2J\033[H", end="")

        print("PORT SCANNER v0.1.0")
        print("-" * 40)

        ip_address = get_ip_address()
        port_min, port_max = get_port_range()

        start_time = datetime.datetime.now()
        open_ports = scan(ip_address, port_min, port_max)

        display_results(open_ports)
        display_duration(start_time)

    except KeyboardInterrupt:
        print("\nYou pressed Ctrl+C. Exiting...")
        sys.exit(130)


if __name__ == "__main__":
    main()
