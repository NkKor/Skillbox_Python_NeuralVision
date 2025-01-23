import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def gorokh_prepare(path):
    df = pd.read_csv(path)
    
    df = df.rename(columns={
        'Месяц': 'month',
        'Квартал': 'quarter',
        'Год': 'year',
        'РФ, средняя цена': 'price'
    })
    
    df['price_date'] = df[['year', 'month']].apply(
        lambda row: datetime(row['year'], row['month'], 1),
        axis=1
    )
    
    return df[['month', 'quarter', 'year', 'price_date', 'price']]

# Путь к файлу
gorokh_path = './goroh.csv'

# Подготовка данных
data = gorokh_prepare(gorokh_path)

# Создание графика
plt.figure(figsize=(15, 10))

# Отображение всех значений
plt.plot(data['price_date'], data['price'], label="Цена гороха")

# Цвет для третьего квартала
color_3q = 'green'

# Функция для поиска и отображения экстремумов в каждом квартале каждого года
def plot_quarter_extremes(group, color):
    for year in group['year'].unique():
        year_group = group[group['year'] == year]
        for quarter in year_group['quarter'].unique():
            quarter_group = year_group[year_group['quarter'] == quarter]
            if len(quarter_group) > 0:  # Проверка на наличие данных
                min_price_index = quarter_group['price'].idxmin()
                max_price_index = quarter_group['price'].idxmax()
                
                plt.scatter(quarter_group.loc[min_price_index]['price_date'],
                            quarter_group.loc[min_price_index]['price'],
                            color=color if quarter == 3 else 'blue', 
                            marker='o', s=50,
                            label=f"Минимум Q{quarter}, {year}" if quarter == 3 else None)
                
                plt.scatter(quarter_group.loc[max_price_index]['price_date'],
                            quarter_group.loc[max_price_index]['price'],
                            color=color if quarter == 3 else 'red', 
                            marker='^', s=50,
                            label=f"Максимум Q{quarter}, {year}" if quarter == 3 else None)

# Применяем функцию к каждому кварталу
plot_quarter_extremes(data, color_3q)

# Добавляем заголовок и подписи к осям
plt.title("Цены на горох по РФ с экстремумами по кварталам")
plt.xlabel("Дата")
plt.ylabel("Средняя цена (руб.)")

# Легенда
plt.legend()

# Показываем график
plt.show()