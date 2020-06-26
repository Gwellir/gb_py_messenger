from enum import Enum

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 7777
ENCODING = 'utf-8'


class Status:
    ONLINE = 'online'
    AFK = 'away'


class ServerCodes:
    OK = 200
    JSON_ERROR = 400
    AUTH_REQUIRED = 401
    AUTH_CREDS = 402
    AUTH_NOUSER = 404
    AUTH_DUPL = 409
    USER_OFFLINE = 410
    SERVER_ERROR = 500


CODE_MESSAGES = {
    ServerCodes.OK: 'OK',
    ServerCodes.JSON_ERROR: 'Incorrect request',
    ServerCodes.AUTH_REQUIRED: 'Authorization required',
    ServerCodes.AUTH_CREDS: 'Wrong password',
    ServerCodes.AUTH_NOUSER: 'User or chat doesn`t exist',
    ServerCodes.AUTH_DUPL: 'This user is already connected',
    ServerCodes.USER_OFFLINE: 'Target user is offline',
    ServerCodes.SERVER_ERROR: 'Server error',
}


class JIMField:
    TIME = 'time'
    RESPONSE = 'response'
    ERROR = 'error'
    ALERT = 'alert'
    ACTION = 'action'


class Client:
    ACC_NAME = 'test'
    ACC_PASSWORD = '12345678'
    ACC_STATUS = Status.ONLINE
