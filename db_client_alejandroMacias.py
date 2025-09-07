import argparse
import platform
import subprocess
import hashlib
from common import is_valid_ip_address
def is_host_reachable(ip_address: str) -> bool:
    TIMEOUT_SECONDS: int = 5
    is_windows_os = platform.system().lower() == 'windows'
    ping_count_param = '-n' if is_windows_os else '-c'
    command = ['ping', ping_count_param, '4', '-q', '-W', str(TIMEOUT_SECONDS),
               ip_address]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
def hash_password(unhashed_password: str) -> str:
    return hashlib.md5(unhashed_password).hexdigest()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('--host', required=True, type=str, help=
                        'DB host to connect (must be valid IPV4 address)')
    parser.add_argument('--port', type=int, default=3000, nargs='?', help=
                        'Port number to use for connection')
    args = parser.parse_args()
    host = args.host
    if not is_valid_ip_address(host):
        raise argparse.ArgumentTypeError("Invalid IP address")
    print("Attempting communication with host...")
    if not is_host_reachable(host):
        raise Exception("Unreachable host. Connection timeout")
