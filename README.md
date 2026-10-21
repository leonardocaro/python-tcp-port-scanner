# Python Port Scanner

A simple TCP port scanner written in Python using the built-in `socket` module.

## Features

- Accepts a hostname, IPv4 or IPv6 address as input.
- Scans a user-defined range of TCP ports.
- Identifies and displays open ports.
- Reports how long the scan took.
- Handles invalid input and keyboard interruption.

## Requirements

- Python 3
- No external dependencies

## Usage

Run the script from your terminal:

```bash
python3 port_scanner.py
```

Enter the hostname or IP address you want to scan, followed by the port range. For example, `1-1024` scans ports 1 through 1024.

Example output:

```text
Enter the hostname or IP address of the machine you want to scan: 127.0.0.1
Enter port range (e.g. 60-120): 1-1024

Open ports:
Port 22: open.
Port 80: open.

Scan completed in 0:00:01.234567.
```

*The example output is illustrative; results and scan duration will vary.*

## Limitations

- Scans ports sequentially.
- Uses a fixed connection timeout of 0.5 seconds per port.
- Uses only the first resolved address out of all possible IPv4 and IPv6 addresses. 

## Disclaimer

This project is intended for educational purposes only. Scan only systems you own or have explicit permission to test. Unauthorized scanning may violate applicable laws or policies.
