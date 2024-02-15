import random

# Количество деталей и нестандартных среди них
total_parts = 10
non_standard_parts = 3

# Количество испытаний для симуляции
n_trials = 1000000

# Счетчик случаев, когда нужно было проверить ровно две детали
two_checks_count = 0

for _ in range(n_trials):
    # Создаем упорядоченный список деталей, где 1 обозначает стандартную, 0 -- нестандартную
    parts = [1] * (total_parts - non_standard_parts) + [0] * non_standard_parts
    # Тщательно перемешиваем детали перед каждым испытанием
    random.shuffle(parts)
    
    # Если первая деталь нестандартная, и вторая -- стандартная, увеличиваем счетчик
    if parts[0] == 0 and parts[1] == 1:
        two_checks_count += 1

# Вычисляем экспериментальную вероятность
experimental_probability = two_checks_count / n_trials

print(f"Экспериментально полученная вероятность: {experimental_probability:.5f}")
print(f"Аналитический ответ: 7/30 ≈ {7/30:.5f}")
print(f"Разница: {abs(experimental_probability - 7/30):.5f}")