# файл: sports_complex_pandas.py

import pandas as pd
from loguru import logger

# Настройка логирования
logger.add("logs.log", format="{time} | {level} | {message}", level="DEBUG", retention="10 days")

def process_activity(file_path):
    """Обрабатывает файл активности спортсменов с использованием pandas."""
    try:
        # Загрузка данных
        df = pd.read_csv(file_path)

        # Преобразование столбца даты в datetime с учетом формата DD/MM/YYYY HH:mm:ss
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        if df['Date'].isnull().any():
            logger.debug("Обнаружены некорректные значения в столбце Date")
            df = df.dropna(subset=['Date'])  # Удаляем строки с некорректным временем

        # Сортировка данных
        df = df.sort_values(by=['Athlete ID', 'Location', 'Date'])

        # Результаты
        results = []

        # Группировка данных по Athlete ID и Location
        grouped = df.groupby(['Athlete ID', 'Location'])

        for (athlete_id, location), group in grouped:
            enter_time = None

            for _, row in group.iterrows():
                action = row['Type']
                timestamp = row['Date']

                if action == 'In':
                    if enter_time is not None:
                        logger.debug(f"Дублированный вход для атлета {athlete_id} в {location}")
                    enter_time = timestamp
                elif action == 'Out':
                    if enter_time is None:
                        logger.debug(f"Не зафиксировано время входа атлета {athlete_id} в {location}")
                        continue
                    # Вычисляем время пребывания
                    duration = (timestamp - enter_time).total_seconds() / 60
                    results.append(f"Атлет {athlete_id} провёл в {location}: {int(duration)} мин.")
                    enter_time = None  # Сбрасываем время входа

            # Если выход не зафиксирован
            if enter_time is not None:
                logger.debug(f"Не зафиксировано время выхода атлета {athlete_id} из {location}")

        return results

    except Exception as e:
        logger.error(f"Ошибка обработки файла: {e}")
        return []

def save_results(results, output_file):
    """Сохраняет результаты в файл."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(results) + '\n')

# Основная программа
if __name__ == "__main__":
    input_file = "activity.csv"  # Файл с активностями
    output_file = "results.txt"  # Файл для записи результатов

    # Обработка файла активности
    results = process_activity(input_file)
    save_results(results, output_file)

    print(f"Результаты сохранены в {output_file}, ошибки записаны в logs.log")
