import argparse
import json
from datetime import datetime
from messenger.common.constants import SERVER_PORT, ENCODING, MAX_DATA_LENGTH


def parse_cli_flags(args_list):
    parser = argparse.ArgumentParser()
    parser.add_argument('address', nargs='?', type=str)
    parser.add_argument('port', nargs='?', type=int, default=SERVER_PORT)

    return parser.parse_args(args_list)


def send_message(message_obj, connection):
    message_str = json.dumps(message_obj, ensure_ascii=False)
    connection.send(message_str.encode(ENCODING))
    print(f'-> {datetime.now().strftime("%H:%M:%S")} Sent message to {connection}: '
          f'{message_obj}')


def receive_message(connection):
    data = connection.recv(MAX_DATA_LENGTH)
    message_str = data.decode(ENCODING)
    try:
        message_obj = json.loads(message_str)
    except json.JSONDecodeError:
        print(f'Error while decoding message at {datetime.now()}')
        return None

    return message_obj
