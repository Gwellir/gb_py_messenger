# Задача 4.
# Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

words = ['разработка', 'администрирование', 'protocol', 'standard']
print(words)
print()

for word in words:
    bytes_ = word.encode(encoding='utf-8')
    print(bytes_, bytes_.decode(encoding='utf-8'))

