import sys
from datetime import datetime
from socket import SOCK_STREAM, socket

from messenger.common.constants import (Client, MIN_PORT_NUMBER, MAX_PORT_NUMBER, JIMFields)
from messenger.common.exceptions import NoAddressGivenError, PortOutOfRangeError
from messenger.common.utils import parse_cli_flags, send_message, receive_message
from messenger.log.client_log_config import CLIENT_LOG
from messenger.common.decorators import Log


@Log(raiseable=True)
def check_settings(args):
    settings = parse_cli_flags(args)
    if not settings.address:
        CLIENT_LOG.error('Address should be the first argument.')
        raise NoAddressGivenError
    if settings.port < MIN_PORT_NUMBER or settings.port > MAX_PORT_NUMBER:
        CLIENT_LOG.error(f'Please use port number between {MIN_PORT_NUMBER} and {MAX_PORT_NUMBER} '
                         f'(got {settings.port})')
        raise PortOutOfRangeError

    return settings.address, settings.port


@Log()
def form_auth_message(acc_name, acc_password):
    auth_obj = {
        JIMFields.ACTION: JIMFields.ActionData.AUTH,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.USER: {
            JIMFields.UserData.ACCOUNT_NAME: acc_name,
            JIMFields.UserData.PASSWORD: acc_password,
        }
    }

    CLIENT_LOG.debug(f'Formed AUTH for user "{acc_name}"')
    return auth_obj


@Log()
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

    CLIENT_LOG.debug(f'Formed PRESENCE for user "{acc_name}": "{status_message}"')
    return presence_obj


@Log()
def form_text_message(from_user, destination, content):
    message_obj = {
        JIMFields.ACTION: JIMFields.ActionData.MESSAGE,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.TO: destination,
        JIMFields.FROM: from_user,
        JIMFields.MESSAGE: content,
    }

    CLIENT_LOG.debug(f'Formed MESSAGE from user "{from_user}" to "{destination}": "{content}"')
    return message_obj


@Log()
def form_join_message(from_user, chat):
    if chat[0] != '#':
        return None
    join_obj = {
        JIMFields.ACTION: JIMFields.ActionData.JOIN,
        JIMFields.TIME: int(datetime.now().timestamp()),
        JIMFields.ROOM: chat,
    }

    CLIENT_LOG.debug(f'Formed JOIN for user "{from_user}" to chat "{chat}"')
    return join_obj


@Log()
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
                CLIENT_LOG.error(f'Got ERROR from server: "{message_obj[JIMFields.ERROR]}"')
                return f'Error: {message_obj[JIMFields.ERROR]}'
            elif JIMFields.ALERT in key_list:
                CLIENT_LOG.info(f'Got ALERT from server: "{message_obj[JIMFields.ALERT]}"')
                return f'Alert: {message_obj[JIMFields.ALERT]}'
        elif JIMFields.ACTION in key_list:
            if message_obj[JIMFields.ACTION] == JIMFields.ActionData.PROBE:
                CLIENT_LOG.info(f'Got PROBE from server at {msg_time}"')
                return f'Probe received at {msg_time}'
                # send_message(presence, conn, CLIENT_LOG)
            elif message_obj[JIMFields.ACTION] == JIMFields.ActionData.MESSAGE:
                CLIENT_LOG.info(f'Got MESSAGE from server: "{message_obj[JIMFields.MESSAGE]}"')
                return f'Message: {message_obj[JIMFields.MESSAGE]}'


if __name__ == '__main__':
    address, port = check_settings(sys.argv[1:])

    conn = socket(type=SOCK_STREAM)
    CLIENT_LOG.info(f'CONNECTING to server: {address}:{port}')
    conn.connect((address, port))

    presence = form_presence_message(str(Client.ACC_NAME), str(Client.ACC_STATUS))
    send_message(presence, conn, CLIENT_LOG)
    parse_message(receive_message(conn, CLIENT_LOG))
    send_message(form_auth_message(Client.ACC_NAME, Client.ACC_PASSWORD), conn, CLIENT_LOG)
    parse_message(receive_message(conn, CLIENT_LOG))
    send_message(form_join_message(Client.ACC_NAME, '#test'), conn, CLIENT_LOG)
    parse_message(receive_message(conn, CLIENT_LOG))
    send_message(form_text_message(Client.ACC_NAME, '#test', 'Привет!'), conn, CLIENT_LOG)
    parse_message(receive_message(conn, CLIENT_LOG))
    conn.close()
