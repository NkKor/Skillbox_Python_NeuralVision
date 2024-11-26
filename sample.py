# файл: calculator.py

from loguru import logger
import re
from datetime import datetime

# Настройка логирования
logger.add("logs.log", format="{time} | {level} | {message}", level="ERROR")

# Операции
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Деление на ноль")
    return a / b

# Обработка строки выражения
def calculate_expression(expression):
    operators = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }

    # Очистка пробелов
    expression = re.sub(r'\s+', '', expression)

    # Парсинг выражения
    match = re.fullmatch(r'(-?\d*\.?\d+)([+\-*/])(-?\d*\.?\d+)', expression)
    if not match:
        raise ValueError(f"Некорректное выражение: '{expression}'")

    operand1, operator, operand2 = match.groups()
    operand1, operand2 = float(operand1), float(operand2)

    # Выполнение операции
    if operator in operators:
        return operators[operator](operand1, operand2)
    else:
        raise ValueError(f"Неизвестный оператор: '{operator}'")

def process_file(input_file, output_file):
    results = []
    error_lines = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    for i, line in enumerate(lines, 1):
        try:
            if not line.strip():
                raise ValueError("Пустая строка")
            result = calculate_expression(line.strip())
            results.append(f"{i} {result:.3f}")
        except Exception as e:
            logger.error(f"Line #{i}: {e}")
            error_lines.append((i, str(e)))

    # Запись результатов
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(results) + '\n')

# Основная программа
if __name__ == "__main__":
    input_file = "exprs.txt"
    output_file = "results.txt"
    
    # Обработка файла
    process_file(input_file, output_file)
    print(f"Результаты сохранены в {output_file}, ошибки записаны в logs.log")