#!/usr/bin/env python3

import socket
import re
import time
import sys


def get_ip_address():
    while True:
        host = input(
            "Enter the hostname or IP address of the machine you want to scan: "
        ).strip()

        if not host:
            print("Hostname or IP address cannot be empty. Try again.")
            continue

        # Remove optional brackets around IPv6 addresses.
        if host.startswith("[") and host.endswith("]"):
            host = host[1:-1]

        try:
            results = socket.getaddrinfo(
                host, None, socket.AF_UNSPEC, socket.SOCK_STREAM
            )

            family, _, _, _, address = results[0]
            return family, address

        except socket.gaierror:
            print("Hostname could not be resolved. Try again.")


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


def scan(address_family, address, port_min, port_max):
    open_ports = []

    for port in range(port_min, port_max + 1):
        try:
            # Preserve the address structure, including IPv6 scope information.
            target = list(address)
            target[1] = port

            with socket.socket(address_family, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)

                if s.connect_ex(tuple(target)) == 0:
                    open_ports.append(port)

        except OSError as error:
            print(f"Socket error on port {port}: {error}")

    return open_ports


def display_results(open_ports):
    if open_ports:
        print("\nOpen ports:")
        for port in open_ports:
            print(f"Port {port}: open.")
    else:
        print("\nNo open ports found.")


def display_duration(start_time):
    elapsed = time.perf_counter() - start_time
    print(f"\nScan completed in {elapsed:.2f} seconds.\n")


def main():
    try:
        print("\033[2J\033[H", end="")

        print("\nPYTHON PORT SCANNER")
        print("-" * 40)

        address_family, address = get_ip_address()
        port_min, port_max = get_port_range()

        print(
            f"\nScanning {address[0]} "
            f"from port {port_min} to {port_max}..."
        )

        start_time = time.perf_counter()

        open_ports = scan(
            address_family, address, port_min, port_max
        )

        display_results(open_ports)
        display_duration(start_time)

    except KeyboardInterrupt:
        print("\n\nYou pressed Ctrl+C. Exiting...\n")
        sys.exit(130)


if __name__ == "__main__":
    main()