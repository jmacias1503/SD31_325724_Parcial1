import argparse
import platform
import subprocess
import hashlib
import socket
import time
import json
from common import is_valid_ip_address, Student
from maskpass import askpass
def is_host_reachable(ip_address: str) -> bool:
    TIMEOUT_SECONDS: int = 5
    is_windows_os = platform.system().lower() == 'windows'
    ping_count_param = '-n' if is_windows_os else '-c'
    command = ['ping', ping_count_param, '4', '-q', '-W', str(TIMEOUT_SECONDS),
               ip_address]
    has_pinged_succesfully = subprocess.call(command, stdout=subprocess.DEVNULL) == 0
    return has_pinged_succesfully
def check_socket_connection(socket_client):
    try:
        socket_client.send(b'')
    except socket.error():
        raise Exception("Socket connection failed")
def hash_password(unhashed_password: str) -> str:
    return hashlib.md5(unhashed_password.encode()).hexdigest()
def add_student(client_socket):
    name: str = input("Enter student's name: ")
    password: str = hash_password(
            askpass(prompt="Enter student's password: ", mask="*")
            )
    gender: str = input("Enter student's gender: ")
    age: int = int(input("Enter student's age: "))
    email: str = input("Enter student's email: ")
    major: str = input("Enter student's major: ")
    student = Student(name, password, gender, age, email, major)
    payload = {
        "query_type": "insert",
        "timestamp": float(time.time()),
        "payload": student
    }
    serialized_data = json.dumps(payload).encode('utf-8')
    check_socket_connection(client_socket)
    client_socket.send(serialized_data)
def print_menu():
    print("DISTRIBUTED SYSTEMS SIMPLE DATABASE CLIENT\n
          SDBDSC  Copyright (C) 2025  Alejandro Macías
          This program comes with ABSOLUTELY NO WARRANTY.
          This is free software, and you are welcome to redistribute it
          under certain conditions.\n
          1. Add student to database
          2. Search by name
          3. Search by age
          4. Quit
          ")
def select_option() -> int:
    VALID_OPTIONS = range(1,5)
    try:
        option_selected: int = int(input("Select an option: "))
    except TypeError:
        print(f"Not valid input")
        select_option()
    if option_selected not in VALID_OPTIONS:
        print("Option not valid. Try again")
        select_option()
    return option_selected
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('--host', default='127.0.0.1', nargs='?', type=str, help=
                        'DB host to connect (must be valid IPV4 address. Default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=3000, nargs='?', help=
                        'Port number to use for connection (Default: 3000)')
    args = parser.parse_args()
    HOST: str = args.host
    PORT_NUMBER: int = args.port
    if not is_valid_ip_address(HOST):
        raise argparse.ArgumentTypeError("Invalid IP address")
    print("Attempting communication with host...")
    if not is_host_reachable(HOST):
        raise Exception("Unreachable host. Connection timeout")
    client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
            )
    client_socket.connect(HOST, PORT_NUMBER)
    check_socket_connection(client_socket)
