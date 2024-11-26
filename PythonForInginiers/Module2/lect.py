import pandas as pd

def read_activity_file(file_path):
    try:
        activity_df = pd.read_csv(file_path, sep='\t')
        return activity_df
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Файл {file_path} пуст.")
        return None

# Вычисление времени, проведенного в бассейне
def calculate_pool_time(activity_df):
    activity_df['pool_time'] = pd.to_datetime(activity_df['exit_time']) - pd.to_datetime(activity_df['entry_time'])
    return activity_df

# Вычисление времени, проведенного в комплексе
def calculate_complex_time(activity_df):
    activity_df['complex_time'] = pd.to_datetime(activity_df['exit_time']) - pd.to_datetime(activity_df['entry_time'])
    return activity_df

# Логирование ошибок и неточностей
def log_errors(activity_df):
    error_log = []
    for index, row in activity_df.iterrows():
        if pd.isnull(row['exit_time']):
            error_log.append(f"Отсутствует время выхода для записи {index}")
        elif pd.isnull(row['entry_time']):
            error_log.append(f"Отсутствует время входа для записи {index}")
        elif row['exit_time'] < row['entry_time']:
            error_log.append(f"Противоречие в записи {index}: время выхода раньше времени входа")
    return error_log

file_path = r'C:\Users\Z0rg3\OneDrive\Документы\VSCode\Skillbox_Python_NeuralVision\PythonForInginiers\Module2\activity.csv'
activity_df = read_activity_file(file_path)
if activity_df is not None:
    activity_df = calculate_pool_time(activity_df)
    activity_df = calculate_complex_time(activity_df)
    error_log = log_errors(activity_df)
    if error_log:
        with open('error_log.txt', 'w') as f:
            for error in error_log:
                f.write(error + '\n')
        print("Лог ошибок записан в файл error_log.txt")
    else:
        print("Ошибок и неточностей не обнаружено.")
