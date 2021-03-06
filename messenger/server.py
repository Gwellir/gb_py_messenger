import sys
from json import JSONDecodeError
from socket import SOCK_STREAM, socket
from datetime import datetime

from messenger.common.constants import (ServerCodes, SERVER_PORT, CODE_MESSAGES, JIMFields, MIN_PORT_NUMBER,
                                        MAX_PORT_NUMBER)
from messenger.common.utils import parse_cli_flags, send_message, receive_message
from messenger.common.exceptions import PortOutOfRangeError
from messenger.log.server_log_config import SERVER_LOG
from messenger.common.decorators import Log


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


@Log(raiseable=True)
def check_settings(args):
    settings = parse_cli_flags(args)
    if not settings.address:
        return '', SERVER_PORT
    if settings.port < MIN_PORT_NUMBER or settings.port > MAX_PORT_NUMBER:
        SERVER_LOG.error(f'Incorrect port number specified during launch: {settings.port}')
        raise PortOutOfRangeError

    return settings.address, settings.port


@Log()
def form_response(code=ServerCodes.OK):
    response_obj = {
        JIMFields.RESPONSE: code,
        JIMFields.TIME: int(datetime.now().timestamp()),
    }

    if code < 400:
        response_obj[JIMFields.ALERT] = CODE_MESSAGES[code]
    else:
        response_obj[JIMFields.ERROR] = CODE_MESSAGES[code]
    SERVER_LOG.debug(f'Formed response: {response_obj}')

    return response_obj


@Log()
def process_action(message_obj):
    if message_obj[JIMFields.ACTION] == JIMFields.ActionData.PRESENCE:
        code = ServerCodes.OK
    elif message_obj[JIMFields.ACTION] == JIMFields.ActionData.AUTH:
        code = ServerCodes.AUTH_CREDS
    elif message_obj[JIMFields.ACTION] == JIMFields.ActionData.JOIN:
        code = ServerCodes.AUTH_NOUSER
    elif message_obj[JIMFields.ACTION] == JIMFields.ActionData.MESSAGE:
        code = ServerCodes.USER_OFFLINE
    else:
        code = ServerCodes.SERVER_ERROR

    return code


@Log()
def send_response(message_obj, client, code=ServerCodes.OK, user=None):
    key_list = message_obj.keys()
    if JIMFields.TIME in key_list:
        msg_time = datetime.fromtimestamp(message_obj[JIMFields.TIME])
        if JIMFields.ACTION in key_list:
            code = process_action(message_obj)
            send_message(form_response(code), client, SERVER_LOG)


@Log(raiseable=True)
def check_presence(presence_obj):
    if not presence_obj:
        return False
    else:
        try:
            if presence_obj[JIMFields.ACTION] == JIMFields.ActionData.PRESENCE\
                    and presence_obj[JIMFields.TYPE] == JIMFields.TypeData.STATUS\
                    and presence_obj[JIMFields.USER][JIMFields.UserData.ACCOUNT_NAME]\
                    and presence_obj[JIMFields.USER][JIMFields.UserData.STATUS]:
                return True
        except KeyError as e:
            SERVER_LOG.error(f'Could not parse PRESENCE message: {presence_obj}')
            raise e
            # return False


@Log()
def terminate_connection(client, code):
    send_message(form_response(code), client, SERVER_LOG)
    client.close()
    # SERVER_LOG.info(f'Client {client.getpeername()} disconnected: {CODE_MESSAGES[code]}')


if __name__ == '__main__':
    address, port = check_settings(sys.argv[1:])
    conn = socket(type=SOCK_STREAM)
    conn.bind((address, port))
    conn.listen(1)
    SERVER_LOG.info(f'Listening on "{address}":{port}')
    # print(f'Listening on "{address}":{port}')

    while True:
        client, addr = conn.accept()
        try:
            presence_obj = receive_message(client, SERVER_LOG)
            if check_presence(presence_obj):
                user = User(client, addr, presence_obj[JIMFields.USER][JIMFields.UserData.ACCOUNT_NAME],
                            presence_obj[JIMFields.USER][JIMFields.UserData.STATUS],
                            datetime.fromtimestamp(presence_obj[JIMFields.TIME]))
                send_response(presence_obj, client)
                SERVER_LOG.info(f'New CLIENT: "{user.username}" from {user.address}')
                # print(f'Client connected: {user}')
            else:
                terminate_connection(client, ServerCodes.JSON_ERROR)
                continue
        except JSONDecodeError:
            terminate_connection(client, ServerCodes.JSON_ERROR)
            continue
        except ConnectionResetError:
            SERVER_LOG.error(f'Connection with {client.getpeername()} was reset')
            continue
        try:
            while True:
                message = receive_message(client, SERVER_LOG)
                if not message:
                    break
                send_response(message, client)
        except ConnectionResetError:
            SERVER_LOG.error(f'Connection with {client.getpeername()} was reset')
            continue
        finally:
            SERVER_LOG.info(f'Client "{user.username}" has disconnected')
            client.close()
