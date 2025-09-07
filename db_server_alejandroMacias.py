import pandas
import argparse
from common import is_valid_ip_address
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple Database server")
    parser.add_argument('--address', default='127.0.0.1', nargs='?', type=str, help=
                        'IP address for serving the database (default 127.0.0.1)')
    parser.add_argument('--port', default=3000, nargs='?', type=int, help=
                        'Port number to use (default 3000)')
    args = parser.parse_args()
    if not is_valid_ip_address(args.address):
        raise argparse.ArgumentTypeError("Invalid IP address")
    IP_ADDRESS: str = args.address
    PORT_NUMBER: int = args.port
