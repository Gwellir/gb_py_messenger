"""
Задача 3.
Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
"""

import yaml

DATA_TO_WRITE = {
    'item1': [1, 2, 3, 4, 5],
    'item2': 10,
    # выражение "значение каждого ключа — это целое число с юникод-символом"
    # получает премию "two zero two four"
    'item3': {
        1: '€',
        2: 'µ',
        3: '♭',
    }
}
YAML_FILE_NAME = 'data/file.yaml'


def write_yaml_data(out_file, data):
    with open(out_file, 'w', encoding='utf-8') as o_f:
        yaml.dump(data, o_f, default_flow_style=False, allow_unicode=True)


def read_yaml_data(in_file):
    with open(in_file, 'r', encoding='utf-8') as i_f:
        data = yaml.load(i_f, Loader=yaml.SafeLoader)
    return data


write_yaml_data(YAML_FILE_NAME, DATA_TO_WRITE)

with open(YAML_FILE_NAME, 'r', encoding='utf-8') as i_f:
    print(i_f.read())

assert DATA_TO_WRITE == read_yaml_data(YAML_FILE_NAME),\
    'Data got corrupted in the process'
