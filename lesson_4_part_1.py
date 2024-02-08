import pandas as pd
import re

def parse_norm(norm_str):
    norm_str = norm_str.replace(',', '.').lower().strip()
    pattern = re.compile(r'([0-9]+\.?[0-9]*)')
    
    if 'не более' in norm_str:
        max_norm = float(pattern.findall(norm_str)[0])
        return None, max_norm
    elif 'в пределах' in norm_str or '-' in norm_str:
        numbers = pattern.findall(norm_str)
        if len(numbers) == 2:
            min_norm, max_norm = map(float, numbers)
            return min_norm, max_norm
        else:
            raise ValueError('Неверный формат диапазона норматива')
    else:
        raise ValueError('Неизвестный формат норматива')

def make_conclusion(row):
    try:
        min_norm, max_norm = parse_norm(row['Норматив'])
    except ValueError as e:
        return str(e)
    
    result_str = str(row['Результат анализа']).replace(',', '.').strip()
    pattern = re.compile(r'([0-9]+\.?[0-9]*)')
    
    if pattern.search(result_str) is None:
        result = 0.0
        if min_norm is None:
            if max_norm and result > max_norm:
                return 'выше нормы'
            return 'ниже нормы'
        return 'ниже нормы'
    else:
        try:
            result = float(pattern.findall(result_str)[0])
            if min_norm and result < min_norm:
                return 'ниже нормы'
            elif max_norm and result > max_norm:
                return 'выше нормы'
            return 'в норме'
        except ValueError:
            return 'Невозможно определить результат'

# Путь к файлу CSV
file_path = 'C:\\Users\\Roadmarshal\\Downloads\\файл.csv'

# Измените сепаратор если файл имеет другой формат
try:
    df = pd.read_csv(file_path, sep=';')
except Exception as e:
    print("Ошибка при чтении файла:", e)
    raise

expected_columns = ['Показатель', 'Результат анализа', 'Норматив']
if not all(col in df.columns for col in expected_columns):
    raise ValueError(f"Данные должны содержать следующие столбцы: {', '.join(expected_columns)}")

df['Вывод'] = df.apply(make_conclusion, axis=1)

print(df[['Показатель', 'Результат анализа', 'Норматив', 'Вывод']])