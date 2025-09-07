import argparse
import platform
import subprocess
import hashlib
import socket
import time
import json
from common import is_valid_ip_address, Student
from maskpass import askpass
MENU_OPTIONS = ["Add student to database", "Search student", "Quit"]
OPTION_COUNT: int = len(MENU_OPTIONS)
SEARCH_OPTIONS = ["name", "email", "age", "gender"]
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
def print_main_menu():
    print("DISTRIBUTED SYSTEMS SIMPLE DATABASE CLIENT\n",
          "SDBDSC  Copyright (C) 2025  Alejandro Macías\n"
          "This program comes with ABSOLUTELY NO WARRANTY.\n"
          "This is free software, and you are welcome to redistribute it\n"
          "under certain conditions.\n"
          )
    for option in MENU_OPTIONS:
        option_index: str = MENU_OPTIONS.index(option)
        print(option_index + ". " + option)
def print_search_menu():
    for option in SEARCH_OPTIONS:
        option_index: str = SEARCH_OPTIONS.index(option)
        print(option_index + ". Search by " + option)
def select_option() -> int:
    VALID_OPTIONS = range(1, OPTION_COUNT + 1)
    try:
        option_selected: int = int(input("Select an option: "))
    except TypeError:
        print(f"Not valid input")
        select_option()
    if option_selected not in VALID_OPTIONS:
        print("Option not valid. Try again")
        select_option()
    return option_selected
def hash_password(unhashed_password: str) -> str:
    return hashlib.md5(unhashed_password.encode()).hexdigest()
def create_payload(query_type: str, payload):
    QUERY_TYPE_LIST = ("insert", "search")
    if query_type not in QUERY_TYPE_LIST:
        raise TypeError("Query type not valid")
    template = {
        "query_type": query_type,
        "timestamp": float(time.time()),
        "payload": payload
    }
    return template
def send_payload(payload, client_socket, host: str, port_number: int):
    serialized_data = json.dumps(payload).encode('utf-8')
    len_payload = len(serialized_data)
    client_socket.connect(host, port_number)
    check_socket_connection(client_socket)
    client_socket.send(len_payload.to_bytes(4, 'big'))
    client_socket.send(serialized_data)
    client_socket.close()
def add_student(client_socket):
    name: str = input("Enter student's name: ")
    password: str = hash_password(
            askpass(prompt="Enter student's password: ", mask="*")
            )
    gender: str = input("Enter student's gender (M: male, F: female, O: other): ")
    match gender:
        case 'M':
            gender = "male"
        case 'F':
            gender = "female"
        case 'O':
            gender = "other"
    age: int = int(input("Enter student's age: "))
    email: str = input("Enter student's email: ")
    major: str = input("Enter student's major: ")
    student = Student(name, password, gender, age, email, major)
    payload = create_payload("insert", student)
    send_payload(payload, client_socket)
def search_student(argument: str, value, client_socket):
    VALID_ARGUMENTS = ["name", "age", "email", "gender"]
    if argument not in VALID_ARGUMENTS:
        raise TypeError("Argument not valid")
    search_payload = {
        "argument": argument,
        "value": value
    }
    payload = create_payload(insert, search_payload)
    send_payload(payload, client_socket)
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
