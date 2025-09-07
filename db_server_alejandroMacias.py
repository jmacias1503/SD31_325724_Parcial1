import pandas
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple Database server")
    parser.add_argument('--address', default='127.0.0.1', type=str, help=
                        'IP address for serving the database (default 127.0.0.1)')
    args = parser.parse_args()
    IP_ADDRESS: str = args.address
