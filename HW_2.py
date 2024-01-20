# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:31:27 2024

@author: Roadmarshal
"""

import pickle
import pandas as pd
import sqlite3

# Загрузка данных из файла .pkl
file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Преобразование данных в DataFrame
df = pd.DataFrame(data)

# Функция для преобразования значений в строку
def list_to_string(x):
    if isinstance(x, list):
        return ', '.join(map(str, x))
    else:
        return x

# Применение функции к каждому элементу DataFrame
df = df.applymap(list_to_string)

# Сохранение в файл pickle
pickle_file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf_from_df.pkl'
df.to_pickle(pickle_file_path)

# Сохранение в файл Excel
excel_file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf_from_df.xlsx'
df.to_excel(excel_file_path, index=False)

# Сохранение в базу данных SQLite
conn = sqlite3.connect('C:\\Users\\Roadmarshal\\Downloads\\data.db')
df.to_sql('df_nashdomrf', conn, if_exists='replace', index=False)
conn.close()
