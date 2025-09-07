import argparse
import platform
import subprocess
import hashlib
import socket
import pickle
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
def hash_password(unhashed_password: str) -> str:
    return hashlib.md5(unhashed_password).hexdigest()
def has_socket_connection(socket_client) -> bool:
    try:
        socket_client.send(b'')
        return True
    except socket.error():
        return False
def add_student(client_socket) -> str:
    name: str = input("Enter student's name: ")
    password: str = hash_password(askpass(prompt="Enter student's password: ", mask="*"))
    gender: str = input("Enter student's gender: ")
    age: int = int(input("Enter student's age: "))
    email: str = input("Enter student's email: ")
    major: str = input("Enter student's major: ")
    student = Student(name, password, gender, age, email, major)
    serialized_data = pickle.dumps(student)
    client_socket.send(serialized_data)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('--host', default='127.0.0.1', nargs='?', type=str, help=
                        'DB host to connect (must be valid IPV4 address. Default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=3000, nargs='?', help=
                        'Port number to use for connection (Default: 3000)')
    args = parser.parse_args()
    HOST: str = args.host
    PORT_NUMBER: int = args.port
    if not is_valid_ip_address(host):
        raise argparse.ArgumentTypeError("Invalid IP address")
    print("Attempting communication with host...")
    if not is_host_reachable(host):
        raise Exception("Unreachable host. Connection timeout")
    client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
            )
    client_socket.connect(HOST, PORT_NUMBER)
    if not has_socket_connection(client_socket):
        raise Exception("Socket connection failed")
