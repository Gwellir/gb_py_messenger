import logging
import sys

SERVER_LOG = logging.getLogger('server')

CONSOLE_LOGGER = logging.StreamHandler(sys.stderr)
FORMATTER = logging.Formatter("%(levelname)-8s %(asctime)s %(message)s")
CONSOLE_LOGGER.setFormatter(FORMATTER)
CONSOLE_LOGGER.setLevel(logging.ERROR)
SERVER_LOG.addHandler(CONSOLE_LOGGER)

FILE_LOGGER = logging.FileHandler('log/server.log', encoding='utf-8')
FILE_LOGGER.setFormatter(FORMATTER)
FILE_LOGGER.setLevel(logging.DEBUG)
SERVER_LOG.addHandler(FILE_LOGGER)

SERVER_LOG.setLevel(logging.DEBUG)
