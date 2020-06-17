# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

words = []

words.append(b'attribute')

# SyntaxError: bytes can only contain ASCII literal characters.
# words.append(b'класс')

# SyntaxError: bytes can only contain ASCII literal characters.
# words.append(b'функция')

words.append(b'type')

print(words)
