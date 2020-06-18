"""
Задача 1.
Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
"""

import glob
import csv
import re
import chardet

REQUIRED_FIELDS = [
    'Изготовитель системы',
    'Название ОС',
    'Код продукта',
    'Тип системы',
]
CSV_FILE_NAME = 'data/extracted_values.csv'


def print_lists(data_lists):
    print()
    for field in data_lists.keys():
        print(f'values for "{field}": ', end='')
        print(', '.join(data_lists[field]))


def read_file(name):
    try:
        with open(name, 'rb') as datafile:
            b_content = datafile.read()
    except IOError as err:
        print(f'Error opening file "{name}": {err}')
        return None
    res = chardet.detect(b_content)
    if res['confidence'] < 0.8:
        print('Encoding may not be detected correctly!')
    content = b_content.decode(res['encoding'])

    return content


def get_data(file_names):
    # os_prod_list = os_name_list = os_code_list = os_type_list = []
    # Вместо отдельных списков сформировал словарь списков.
    # Вообще формулировка пункта 1.а страннейшая - списки эти там, например,
    # потом не используются, а main_data называется то списком, то файлом

    data_lists = {}
    for field in REQUIRED_FIELDS:
        data_lists[field] = []

    main_data = [REQUIRED_FIELDS]
    catcher = re.compile(r'^(\w[\w\d\s\\p{Punct}]*?):[ \t]+(.*?)$', re.M)
    print('Processing files:')
    for name in file_names:
        print(name)
        content = read_file(name)
        if not content:
            continue
        matches = catcher.findall(content)
        match_dict = {match[0]: match[1].strip() for match in matches}
        data_summary = []
        for field in REQUIRED_FIELDS:
            if field in match_dict.keys():
                value = match_dict[field]
            else:
                value = 'n/a'
            data_lists[field].append(value)
            data_summary.append(value)
        main_data.append(data_summary)

    print_lists(data_lists)

    return main_data


def write_to_csv(out_file):
    file_names_list = glob.glob('data/info*.txt', recursive=False)

    data_to_store = get_data(file_names_list)
    with open(out_file, 'w', newline='', encoding='utf-8') as out:
        out_writer = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_to_store:
            out_writer.writerow(row)


write_to_csv(CSV_FILE_NAME)

print('\nResults:')
with open(CSV_FILE_NAME, encoding='utf-8') as f_n:
    print(f_n.read())
