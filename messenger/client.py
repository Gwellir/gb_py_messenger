import json
import sys
from datetime import datetime
from socket import SOCK_STREAM, socket

from messenger.common.constants import (Client, MIN_PORT_NUMBER, MAX_PORT_NUMBER, JIMFields)
from messenger.common.exceptions import NoAddressGivenError, PortOutOfRangeError
from messenger.common.utils import parse_cli_flags, send_message, receive_message


def check_settings(args):
    settings = parse_cli_flags(args)
    if not settings.address:
        print('Address should be the first argument.')
        raise NoAddressGivenError
    if settings.port < MIN_PORT_NUMBER or settings.port > MAX_PORT_NUMBER:
        print(f'Please use port number between {MIN_PORT_NUMBER} and {MAX_PORT_NUMBER} (got {settings.port})')
        raise PortOutOfRangeError

    return settings.address, settings.port


def form_auth_message(acc_name, acc_password):
    auth_obj = {
        JIMFields.ACTION: JIMFields.ActionData.AUTH,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.USER: {
            JIMFields.UserData.ACCOUNT_NAME: acc_name,
            JIMFields.UserData.PASSWORD: acc_password,
        }
    }

    return auth_obj


def form_presence_message(acc_name, status_message):
    presence_obj = {
        JIMFields.ACTION: JIMFields.ActionData.PRESENCE,
        JIMFields.TIME: int(datetime.timestamp(datetime.now())),
        JIMFields.TYPE: JIMFields.TypeData.STATUS,
        JIMFields.USER: {
            JIMFields.UserData.ACCOUNT_NAME: acc_name,
            JIMFields.UserData.STATUS: status_message,
        },
    }

    return presence_obj


def form_text_message(from_user, destination, content):
    message_obj = {
        JIMFields.ACTION: JIMFields.ActionData.MESSAGE,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.TO: destination,
        JIMFields.FROM: from_user,
        JIMFields.MESSAGE: content,
    }

    return message_obj


def form_join_message(from_user, chat):
    if chat[0] != '#':
        return None
    join_obj = {
        JIMFields.ACTION: JIMFields.ActionData.JOIN,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.ROOM: chat,
    }

    return join_obj


def parse_message(message_obj):
    """
    Message content parser.

    Placeholder for future logic
    """
    key_list = message_obj.keys()
    if JIMFields.TIME in key_list:
        msg_time = datetime.fromtimestamp(message_obj[JIMFields.TIME])
        if JIMFields.RESPONSE in key_list:
            if JIMFields.ERROR in key_list:
                print(f'<- {message_obj[JIMFields.ERROR]}')
                return f'Error: {message_obj[JIMFields.ERROR]}'
            elif JIMFields.ALERT in key_list:
                print(f'<- {message_obj[JIMFields.ALERT]}')
                return f'Alert: {message_obj[JIMFields.ALERT]}'
        elif JIMFields.ACTION in key_list:
            if message_obj[JIMFields.ACTION] == JIMFields.ActionData.PROBE:
                print('Probe received.')
                return f'Probe received at {msg_time}'
                # send_message(presence, conn)
            elif message_obj[JIMFields.ACTION] == JIMFields.ActionData.MESSAGE:
                print(message_obj[JIMFields.MESSAGE])
                return f'Message: {message_obj[JIMFields.MESSAGE]}'


if __name__ == '__main__':
    address, port = check_settings(sys.argv[1:])

    conn = socket(type=SOCK_STREAM)  # Создать сокет TCP
    print(f'Attempting connection to {address}:{port}')
    conn.connect((address, port))   # Соединиться с сервером

    print(f'Forming presence message for user "{Client.ACC_NAME}": "{Client.ACC_STATUS}"')
    presence = form_presence_message(str(Client.ACC_NAME), str(Client.ACC_STATUS))
    send_message(presence, conn)
    parse_message(receive_message(conn))
    send_message(form_auth_message(Client.ACC_NAME, Client.ACC_PASSWORD), conn)
    parse_message(receive_message(conn))
    send_message(form_join_message(Client.ACC_NAME, '#test'), conn)
    parse_message(receive_message(conn))
    send_message(form_text_message(Client.ACC_NAME, '#test', 'Привет!'), conn)
    parse_message(receive_message(conn))
    conn.close()
