import argparse
import platform
import subprocess
def is_valid_ip_address(ip_address: str) -> bool:
    values = ip_address.split('.')
    if len(values) != 4:
        return False
    for i in values:
        try:
            if int(i) not in range(256):
                return False
        except ValueError:
            return False
    return True
def is_host_reachable(ip_address: str) -> bool:
    TIMEOUT_SECONDS = 5
    ping_count_param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', ping_count_param, '4', '-q', '-W', str(TIMEOUT_SECONDS),
               ip_address]
    return subprocess.call(command) == 0
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('--host', metavar = 'IPV4 address', required=True,
                        type=str, help=
                        'DB host to connect (must be valid IPV4 address)')
    args = parser.parse_args()
    host = args.host
    if not is_valid_ip_address(host):
        raise argparse.ArgumentTypeError("Invalid IP address")
    if not is_host_reachable(host):
        raise Exception("Unreachable host")
