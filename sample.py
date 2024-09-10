import re

def calculate_expression(expression):
  """Вычисляет выражение, обрабатывая пробелы и поддерживая операции сложения, умножения, вычитания и деления.

  Args:
    expression: Строка, содержащая выражение.

  Returns:
    Результат вычисления выражения или None, если возникла ошибка.
  """
  try:
    # Удаляем лишние пробелы
    expression = re.sub(r'\s+', '', expression)
    # Используем eval для вычисления выражения
    result = eval(expression)
    return result
  except Exception as e:
    # Возвращаем None, если возникла ошибка
    return None, str(e)

def read_expressions(filename):
  """Читает выражения из файла.

  Args:
    filename: Имя файла, содержащего выражения.

  Returns:
    Список строк (выражений).
  """
  with open(filename, "r") as file:
    expressions = file.readlines()
  return expressions

def write_results(results):
  """Записывает результаты вычислений в файл.

  Args:
    results: Список кортежей, где каждый кортеж содержит номер строки и результат вычисления.
  """
  with open("results.txt", "w") as file:
    for i, result in results:
      file.write(f"{i} {result}\n")

def write_errors(errors):
  """Записывает ошибки в файл.

  Args:
    errors: Список кортежей, где каждый кортеж содержит номер строки и описание ошибки.
  """
  with open("errors.txt", "w") as file:
    file.write(f"Количество ошибок: {len(errors)}\n")
    for i, error in errors:
      file.write(f"{i} {error}\n")


expressions = read_expressions("exprs.txt")
results = []
errors = []

for i, expression in enumerate(expressions, 1):
  expression = expression.strip()
  result, error = calculate_expression(expression)
  if result is not None:
    results.append((i, result))
  else:
    errors.append((i, error))
write_results(results)
write_errors(errors)