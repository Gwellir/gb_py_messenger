# Задача 5.
# Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
# на кириллице.

import subprocess
import chardet

ADDRESSES = ['yandex.ru', 'youtube.com']

for address in ADDRESSES:
    args = ['ping', address]
    PINGER = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in PINGER.stdout:
        result = chardet.detect(line)
        data = line.decode(result['encoding']).encode('utf-8')
        print(data.decode('utf-8'))
