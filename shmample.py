def count_chars_and_find_lines(filename, words):
  """
  Функция считает количество символов в файле и выводит строки, содержащие заданные слова.

  Args:
    filename: Имя текстового файла.
    words: Список слов для поиска.

  Returns:
    Кортеж, содержащий:
      - Количество символов в файле.
      - Список строк, содержащих заданные слова.
  """

  char_count = 0
  found_lines = []

  with open(filename, 'r') as file:
    for line in file:
      char_count += len(line)
      for word in words:
        if word in line:
          found_lines.append(line.strip())
          break  # Прекращаем проверку на слова в этой строке, если нашли хотя бы одно

  return char_count, found_lines

# Получаем имя файла и слова от пользователя
filename = input("Введите имя файла: ")
words = input("Введите слова через пробел: ").split()

# Вызываем функцию и получаем результаты
char_count, found_lines = count_chars_and_find_lines(filename, words)

# Выводим результаты
print(f"Количество символов в файле: {char_count}")
print("Строки, содержащие заданные слова:")
for line in found_lines:
  print(line)


