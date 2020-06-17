# Задача 6.
# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.

import chardet

file_name = 'test_file.txt'

with open(file_name, 'w') as test_file:
    test_file.write('сетевое программирование\nсокет\nдекоратор')
    test_file.close()

with open(file_name, 'rb') as test_file:
    content = test_file.read()
    res = chardet.detect(content)
    print(res['encoding'], f'{res["confidence"]:.2f}')

# as opening with 'utf-8' encoding fails...
with open(file_name, 'rb') as test_file:
    content = test_file.read()
    str_repr = content.decode('utf-8', 'replace')
    print(str_repr)
