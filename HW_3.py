import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных из файла .pkl
file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf.pkl'
with open(file_path, 'rb') as file:
    start_df = pickle.load(file)

# Функция для определения "Жилое" или "Нежилое"
def determine_type(item):
    if isinstance(item, dict):
        text = str(item) 
    elif isinstance(item, list):
        text = str(item)
    elif isinstance(item, str):
        text = item
    else:
        return "Неопределено"

    if 'Жилое' in text:
        return 'Жилое'
    elif 'Нежилое' in text:
        return 'Нежилое'
    return 'Неопределено'

# Добавление нового столбца 'Тип' в DataFrame
start_df['Тип'] = start_df['photoRenderDTO'].apply(determine_type)

# Удаление строк где в 'objPriceAvg' пустые значения
Viborka_itog = start_df.dropna(subset=['objPriceAvg'])

# Функция для построения графиков и расчета данных
def analyze_prices(df, title_prefix=''):
    # Посчитаем среднее значение по регионам
    средние_по_регионам = df.groupby('developer.regRegionDesc')['objPriceAvg'].mean()

    # Среднее значение по всем регионам
    общее_среднее = средние_по_регионам.mean()
    
    # Вывод графика
    plt.figure(figsize=(20, 8))
    sns.barplot(x=средние_по_регионам.index, y=средние_по_регионам.values, palette="viridis")
    plt.axhline(общее_среднее, color='r', linestyle='--')
    plt.xticks(rotation=90)
    plt.ylabel('Средняя стоимость')
    plt.xlabel('Регион')
    plt.title(f'Средняя стоимость {title_prefix}недвижимости по регионам')
    plt.show()
    
    # Рассчитаем отклонения от общего среднего для каждого региона
    средние_по_регионам = средние_по_регионам.to_frame(name='Средняя цена за м2')
    средние_по_регионам['Отклонение'] = средние_по_регионам['Средняя цена за м2'] - общее_среднее

    # Находим топ 5 регионов с отклонениями выше и ниже среднего
    top_above_average = средние_по_регионам.nlargest(5, 'Отклонение')
    top_below_average = средние_по_регионам.nsmallest(5, 'Отклонение')
    
    # Вывод топ 5 регионов с отклонениями
    print(f"\nТоп 5 регионов по средней стоимости выше среднего {title_prefix}недвижимости:")
    print(top_above_average)
    
    print(f"\nТоп 5 регионов по средней стоимости ниже среднего {title_prefix}недвижимости:")
    print(top_below_average)

# Анализ цен для всех объектов недвижимости
analyze_prices(Viborka_itog, title_prefix='всей ')

# Анализ цен для жилой недвижимости
жилая_недвижимость = Viborka_itog[Viborka_itog['Тип'] == 'Жилое']
analyze_prices(жилая_недвижимость, title_prefix='жилой ')

# Анализ цен для нежилой недвижимости
нежилая_недвижимость = Viborka_itog[Viborka_itog['Тип'] == 'Нежилое']
analyze_prices(нежилая_недвижимость, title_prefix='нежилой ')

# Разница между средней стоимостью жилой и нежилой недвижимости в среднем по всем регионам
общее_среднее_жилая = жилая_недвижимость['objPriceAvg'].mean()
общее_среднее_нежилая = нежилая_недвижимость['objPriceAvg'].mean()
разница_в_среднем = общее_среднее_жилая - общее_среднее_нежилая
print(f"\nРазница в средней стоимости между жилой и нежилой недвижимостью в среднем по всем регионам: {разница_в_среднем:.2f} руб/м²")