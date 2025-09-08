import pandas
import argparse
import socket
import threading
import time
import json
from common import is_valid_ip_address
LOCK_RESOURCE = threading.lock()
def insert_to_log(log_file: str, payload):
    """
    Inserts actions to log file
    """
    query_type = payload.get("query_type")
    transaction_time = payload.get("timestamp")
    data = payload.get("payload")
    with LOCK_RESOURCE:
        with open(log_file, "a") as file:
            file.write(f"[{time.time()}];{query_type};{data}")
def decode_payload(encoded_payload):
    """
    Decodes the encoded json payload
    """
    return json.loads(encoded_payload.decode('utf-8'))
def add_student(payload, columns, csv_file, log_file):
    data = payload.get("data")
    with LOCK_RESOURCE:
        df = pandas.DataFrame([data], columns=columns)
        df.to_csv(csv_file, mode='a', header=False, index=False)
    insert_to_log(payload, log_file)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple Database server")
    parser.add_argument('--address', default='127.0.0.1', nargs='?', type=str, help=
                        'IP address for serving the database (default 127.0.0.1)')
    parser.add_argument('--port', default=3000, nargs='?', type=int, help=
                        'Port number to use (default 3000)')
    parser.add_argument('--followreqs', action="store_true", nargs='?', default=False,
                        help='Follow csv requirements')
    parser.add_argument('--dbfile', default='DB.csv', nargs='?', type=str, help=
                        'Database file to use (default DB.csv)')
    args = parser.parse_args()
    is_csv_file = args.dbfile.split('.')[1] == 'csv'
    if not is_csv_file:
        raise argparse.ArgumentTypeError("Invalid file")
    if args.followreqs:
        csv_columns = ("nombre", "password", "genero", "edad", "email", "carrera")
    else:
        csv_columns = ("name", "password", "gender", "age", "email", "major")
    IP_ADDRESS: str = args.address
    PORT_NUMBER: int = args.port
    if not is_valid_ip_address(IP_ADDRESS):
        raise argparse.ArgumentTypeError("Invalid IP address")
    server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
    )
    server_socket.bind((IP_ADDRESS, PORT_NUMBER))
