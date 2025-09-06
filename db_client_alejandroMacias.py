import argparse
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
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('--host', metavar = '-H', required=True, type=str, help=
                        'DB host to connect (must be valid IP address)')
    args = parser.parse_args()
    if not is_valid_ip_address(args.host):
        raise ValueError("Invaid IP address")
