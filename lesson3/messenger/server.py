from json import JSONDecodeError
from socket import SOCK_STREAM, socket
from datetime import datetime
import json
from lesson3.messenger.constants import *


class User:
    def __init__(self, client, address, username, status, last_online):
        self.client = client
        self.address = address
        self.username = username
        self.status = status
        self.last_online = last_online

    def __repr__(self):
        return f'"{self.username}"' \
               f'\nconnected from: {self.address}' \
               f'\nlast online: {self.last_online.strftime("%H:%M:%S")} with status "{self.status}"'


def form_response(connection, code=ServerCodes.OK):
    response_obj = {
        'response': code,
        'time': int(datetime.now().timestamp()),
    }

    if code < 400:
        response_obj['alert'] = CODE_MESSAGES[code]
    else:
        response_obj['error'] = CODE_MESSAGES[code]

    return response_obj


def send_message(message_obj, connection=None):
    if not connection:
        connection = client
    message_str = json.dumps(message_obj, ensure_ascii=False)
    connection.send(message_str.encode(ENCODING))
    print(f'-> {datetime.now().strftime("%H:%M:%S")} Sent {message_obj["response"]} to the client: '
          f'{message_obj}')


def receive_message(connection):
    data = connection.recv(1024)

    return data.decode(ENCODING)


def process_action(message_obj):
    if message_obj['action'] == 'presence':
        code = ServerCodes.OK
    elif message_obj['action'] == 'authenticate':
        code = ServerCodes.AUTH_CREDS
    elif message_obj['action'] == 'join':
        code = ServerCodes.AUTH_NOUSER
    elif message_obj['action'] == 'msg':
        code = ServerCodes.USER_OFFLINE
    else:
        code = ServerCodes.SERVER_ERROR

    return code


def parse_message(message_str, user=None):
    try:
        message_obj = json.loads(message_str)
    except json.JSONDecodeError:
        print(f'Error while decoding client message at {datetime.now()}')
        return None
    key_list = message_obj.keys()
    if 'time' in key_list:
        msg_time = datetime.fromtimestamp(message_obj['time'])
        if 'action' in key_list:
            print(f'<- Client sent us "{message_obj["action"]}": {message_obj}')
            code = process_action(message_obj)
            send_message(form_response(client, code))

    return message_obj


conn = socket(type=SOCK_STREAM)
conn.bind((SERVER_ADDRESS, SERVER_PORT))
conn.listen(1)
print(f'Listening on {SERVER_ADDRESS}:{SERVER_PORT}')

while True:
    client, addr = conn.accept()
    try:
        presence = parse_message(receive_message(client))
        if 'user' in presence.keys() and 'type' in presence.keys() and \
                'account_name' in presence['user'].keys() and 'status' in presence['user'].keys():
            user = User(client, addr, presence['user']['account_name'], presence['user']['status'],
                        datetime.fromtimestamp(presence['time']))
            print(f'Client connected: {user}')
        else:
            send_message(form_response(client, ServerCodes.JSON_ERROR))
            client.close()
            continue
    except JSONDecodeError:
        send_message(form_response(client, ServerCodes.JSON_ERROR))
        client.close()
        continue
    except ConnectionResetError:
        continue

    try:
        while True:
            data = receive_message(client)
            if not data:
                break
            parse_message(data)
    except ConnectionResetError:
        continue
    finally:
        print(f'Client disconnected: {user}')
        client.close()
