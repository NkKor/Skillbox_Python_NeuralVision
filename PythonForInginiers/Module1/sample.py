def calculate_expression(expression):
    try:
        return eval(expression)
    except SyntaxError as e:
        raise SyntaxError(f"Синтаксическая ошибка в выражении: {e}")
    except NameError as e:
        raise NameError(f"Некорректное имя переменной: {e}")

def read_expressions():
    with open("exprs.txt", "r") as file:
        expressions = file.readlines()
    return [expression.strip() for expression in expressions]

def write_results(results):
    with open("results.txt", "w") as file:
        for line_number, result in results:
            file.write(f"{line_number} {result}\n")

def write_errors(errors):
    with open("errors.txt", "w") as file:
        for line_number, error_message in errors:
            file.write(f"{line_number} {error_message}\n")

expressions = read_expressions()
results = []
errors = []
    
for line_number, expression in enumerate(expressions, 1):
    try:
        result = calculate_expression(expression)
        results.append((line_number, result))
    except (SyntaxError, NameError) as e:
        errors.append((line_number, str(e)))
    
write_results(results)
write_errors(errors)


