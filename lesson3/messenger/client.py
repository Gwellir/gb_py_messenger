import json
from datetime import datetime
from socket import SOCK_STREAM, socket

from lesson3.messenger.constants import *


def form_auth_message(acc_name, acc_password):
    auth_obj = {
        'action': 'authenticate',
        'time': int(datetime.now().timestamp()),
        'user': {
            'account_name': acc_name,
            'password': acc_password,
        }
    }

    return auth_obj


def form_presence_message(acc_name, status_message):
    presence_obj = {
        'action': 'presence',
        'time': int(datetime.timestamp(datetime.now())),
        'type': 'status',
        'user': {
            'account_name': acc_name,
            'status': status_message,
        },
    }

    return presence_obj


def form_text_message(from_user, destination, content):
    message_obj = {
        'action': 'msg',
        'time': int(datetime.now().timestamp()),
        'to': destination,
        'from': from_user,
        'message': content,
    }

    return message_obj


def form_join_message(from_user, chat):
    join_obj = {
        'action': 'join',
        'time': int(datetime.now().timestamp()),
        'room': chat,
    }

    return join_obj


def send_message(message_obj, connection=None):
    if not connection:
        connection = conn
    message_str = json.dumps(message_obj, ensure_ascii=False)
    connection.send(message_str.encode(ENCODING))
    print(f'-> {datetime.now().strftime("%H:%M:%S")} Sent {message_obj["action"]} to the server: '
          f'{message_obj}')


def receive_message(connection):
    data = connection.recv(1024)

    return data.decode(ENCODING)


def parse_message(message_str):
    try:
        message_obj = json.loads(message_str)
    except json.JSONDecodeError:
        print(f'Error while decoding server message at {datetime.now()}')
        return None
    key_list = message_obj.keys()
    if 'time' in key_list:
        msg_time = datetime.fromtimestamp(message_obj['time'])
        if 'response' in key_list:
            if 'error' in key_list:
                print(f'<- {message_obj["error"]}')
            elif 'alert' in key_list:
                print(f'<- {message_obj["alert"]}')
        elif 'action' in key_list:
            if message_obj['action'] == 'probe':
                send_message(presence)
            elif message_obj['action'] == 'msg':
                print(message_obj['message'])

                
conn = socket(type=SOCK_STREAM)  # Создать сокет TCP
conn.connect((SERVER_ADDRESS, SERVER_PORT))   # Соединиться с сервером

print(f'Forming presence message for user "{Client.ACC_NAME}": "{Client.ACC_STATUS}"')
presence = form_presence_message(str(Client.ACC_NAME), str(Client.ACC_STATUS))
send_message(presence, conn)
parse_message(receive_message(conn))
send_message(form_auth_message(Client.ACC_NAME, Client.ACC_PASSWORD))
parse_message(receive_message(conn))
send_message(form_join_message(Client.ACC_NAME, '#test'))
parse_message(receive_message(conn))
send_message(form_text_message(Client.ACC_NAME, '#test', 'Привет!'))
parse_message(receive_message(conn))
# try:
#     while True:
#         parse_message(receive_message(conn))
# finally:
#     conn.close()

# msg = 'Привет, сервер'
# conn.send(msg.encode('utf-8'))
# data = conn.recv(1024)
# print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
# conn.close()