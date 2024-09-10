def find_lines_with_word(file_path, word):
    lines_with_word = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if word in line:
                    lines_with_word.append(line.strip())
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    return lines_with_word

# Пример использования:
file_path = r'C:\Users\Z0rg3\OneDrive\Документы\VSCode\Skillbox_Python_NeuralVision\PythonForInginiers\war_and_peace.txt'  # Укажите путь к вашему файлу
word = 'Андрей'  # Замените на слово, которое хотите найти
found_lines = find_lines_with_word(file_path, word)

print("Найденные строки:")
for line in found_lines:
    print(line)


