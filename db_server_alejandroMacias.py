import pandas
import argparse
import socket
import threading
import time
import json
from common import is_valid_ip_address, PAYLOAD_BUFFER_SIZE_BYTES
LOCK_RESOURCE = threading.Lock()
def insert_to_log(log_file: str, payload):
    """
    Inserts actions to log file
    """
    query_type = payload.get("query_type")
    transaction_time = payload.get("timestamp")
    data = payload.get("payload")
    with LOCK_RESOURCE:
        with open(log_file, "a") as file:
            file.write(f"{transaction_time};{query_type};{data}")
def decode_payload(encoded_payload):
    """
    Decodes the encoded json payload
    """
    return json.loads(encoded_payload.decode('utf-8'))
def add_student(payload, columns, csv_file, log_file) -> str:
    data = payload.get("payload")
    with LOCK_RESOURCE:
        df = pandas.DataFrame([data], columns=columns)
        df.to_csv(csv_file, mode='a', header=False, index=False)
    insert_to_log(log_file, payload)
    response = {
        "status": "Created",
        "response": "Student created"
    }
    return response
def search_student(payload, csv_file, log_file) -> str:
    argument = payload.get("payload").get("argument")
    value = payload.get("payload").get("value")
    with LOCK_RESOURCE:
        df = pandas.read_csv(csv_file)
        if argument not in df.columns:
            raise Exception("Column not found")
        results = df[df[argument] == value]
        response = results.to_json(orient='records')
        insert_to_log(log_file, payload)
        return response
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "DS Simple Database server")
    parser.add_argument('--address', default='127.0.0.1', nargs='?', type=str, help=
                        'IP address for serving the database (default 127.0.0.1)')
    parser.add_argument('--port', default=3000, nargs='?', type=int, help=
                        'Port number to use (default 3000)')
    parser.add_argument('--followreqs', action="store_true", default=False,
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
    csv_file = args.dbfile
    IP_ADDRESS: str = args.address
    PORT_NUMBER: int = args.port
    log_file = "db.log"
    if not is_valid_ip_address(IP_ADDRESS):
        raise argparse.ArgumentTypeError("Invalid IP address")
    server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
    )
    def handle_client(client_socket, client_address, log_file):
        connection_log = {
            "query_type": "login",
            "timestamp": float(time.time()),
            "payload": "client_address"
        }
        insert_to_log(log_file, connection_log)
        len_bytes = client_socket.recv(PAYLOAD_BUFFER_SIZE_BYTES)
        payload_len = int.from_bytes(len_bytes, 'big')
        encoded_payload = client_socket.recv(payload_len)
        payload = decode_payload(encoded_payload)
        payload = dict(payload)
        query_type = payload.get("query_type")
        if query_type == "insert":
            response = json.dumps(add_student(payload, csv_columns, csv_file, log_file))
        elif query_type == "search":
            response = json.dumps(search_student(payload, csv_file, log_file))
        client_socket.sendall(response.encode('utf-8'))
    server_socket.bind((IP_ADDRESS, PORT_NUMBER))
    server_socket.listen(5)
    print("Hearing connections")
    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address, log_file))
        client_handler.start()
