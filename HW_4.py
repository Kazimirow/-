import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

class RealEstateAnalyzer:
    def __init__(self, file_path):
        with open(file_path, 'rb') as file:
            self.full_df = pickle.load(file)
        self.processed_df = None
    
    def preprocess_data(self):
        self.full_df['Тип'] = self.full_df['photoRenderDTO'].apply(self._determine_type)
        self.processed_df = self.full_df.dropna(subset=['objPriceAvg'])
        
    def analyze_prices(self, property_type=None):
        df = self.processed_df
        if property_type:
            df = df[df['Тип'] == property_type]
        self._plot_average_prices_by_region(df, property_type)
        self._print_top_regions_by_price(df, property_type)
    
    def _plot_average_prices_by_region(self, df, property_type=''):
        title_prefix = f"{property_type} " if property_type else ""
        average_by_region = df.groupby('developer.regRegionDesc')['objPriceAvg'].mean()
        overall_average = average_by_region.mean()

        plt.figure(figsize=(20, 8))
        sns.barplot(x=average_by_region.index, y=average_by_region.values, palette="viridis")
        plt.axhline(overall_average, color='r', linestyle='--')
        plt.xticks(rotation=90)
        plt.ylabel('Средняя стоимость')
        plt.xlabel('Регион')
        plt.title(f'Средняя стоимость {title_prefix}недвижимости по регионам')
        plt.show()
    
    def _print_top_regions_by_price(self, df, property_type=''):
        title_prefix = f"{property_type} " if property_type else ""
        average_by_region = df.groupby('developer.regRegionDesc')['objPriceAvg'].mean()
        overall_average = average_by_region.mean()
        deviations = average_by_region - overall_average
        top_above = deviations.nlargest(5)
        top_below = deviations.nsmallest(5)
        
        print(f"\nТоп 5 регионов по средней стоимости выше среднего {title_prefix}недвижимости:")
        print(top_above)

        print(f"\nТоп 5 регионов по средней стоимости ниже среднего {title_prefix}недвижимости:")
        print(top_below)

    @staticmethod
    def _determine_type(item):
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

# Использование класса для анализа
file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf.pkl'
analyzer = RealEstateAnalyzer(file_path)
analyzer.preprocess_data()
analyzer.analyze_prices()
analyzer.analyze_prices('Жилое')
analyzer.analyze_prices('Нежилое')

class DataFrameHandler:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_pickle(self):
        with open(self.file_path, 'rb') as file:
            data = pickle.load(file)
        self.df = pd.DataFrame(data)
    
    def save_to_pickle(self, path):
        self.df.to_pickle(path)
    
    def save_to_excel(self, path, index=False):
        self.df.to_excel(path, index=index)
    
    def save_to_sqlite(self, db_path, table_name):
        conn = sqlite3.connect(db_path)
        self.df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

    def apply_to_df(self, func):
        self.df = self.df.applymap(func)

def list_to_string(x):
    if isinstance(x, list):
        return ', '.join(map(str, x))
    else:
        return x

# Определение путей файлов
pickle_file_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf.pkl'
pickle_save_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf_from_df.pkl'
excel_save_path = 'C:\\Users\\Roadmarshal\\Downloads\\df_nashdomrf_from_df1.xlsx'
sqlite_db_path = 'C:\\Users\\Roadmarshal\\Downloads\\data.db'

# Создание экземпляра класса DataFrameHandler и выполнение операций
df_handler = DataFrameHandler(pickle_file_path)
df_handler.load_pickle()
df_handler.apply_to_df(list_to_string)
df_handler.save_to_pickle(pickle_save_path)
df_handler.save_to_excel(excel_save_path)
df_handler.save_to_sqlite(sqlite_db_path, 'df_nashdomrf')