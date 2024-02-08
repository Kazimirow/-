import random
from collections import Counter

# Установим количество испытаний для моделирования
n_trials = 1000000  # 1 миллион испытаний для надежной оценки

# Опишем состав ящика
box = ['апельсин'] * 5 + ['яблоко'] * 4  # 5 апельсинов и 4 яблока

# Переменная для подсчета успешных исходов
successful_outcomes = 0

for _ in range(n_trials):
    # Выберем 3 фрукта наудачу
    chosen_fruits = random.sample(box, 3)
    # Если все выбранные фрукты - апельсины, увеличим счетчик успешных исходов
    if Counter(chosen_fruits)['апельсин'] == 3:
        successful_outcomes += 1

# Рассчитаем экспериментальную вероятность
experimental_probability = successful_outcomes / n_trials

print(f"Экспериментально полученная вероятность: {experimental_probability:.3f}")
# Сверим с аналитически рассчитанным ответом
print(f"Аналитический ответ: 0.119")
print(f"Разница: {abs(experimental_probability - 0.119):.3f}")