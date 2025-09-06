import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple database client")
    parser.add_argument('host', metavar = '-H', required=True, type=str, help=
                        'DB host to connect (must be valid IP address)')
    args = parser.parse_args()
