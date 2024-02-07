import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import math

# Генерация примеров из косинусного распределения
cosine_rv = sts.cosine()
sample = cosine_rv.rvs(100)

# Вычисление среднего и дисперсии
sample_mean = np.mean(sample)
sample_var = np.var(sample)

# Настоящее среднее и дисперсия случайной величины
real_mean = cosine_rv.mean()
real_var = cosine_rv.var()

# Вывод результатов
print('Выборочное среднее:', sample_mean)
print('Выборочная дисперсия:', sample_var)
print('Настоящее среднее:', real_mean)
print('Настоящая дисперсия:', real_var)
plt.hist(sample, density=True)
x = np.linspace(-4,4,100)
pdf = cosine_rv.pdf(x)
plt.plot(x, pdf, label='теоретическая плотность', alpha=0.5)
plt.legend()
sample_mean = sample.mean() # выборочное среднее
print(sample_mean)
sample_var = sample.var() # выборочная дисперсия
print(sample_var)
n_values = [5, 10, 50, 100]  # Размеры выборок
num_of_samples = 1000  # Количество выборок

plt.figure(figsize=(15, 10))

for i, n in enumerate(n_values):
    means = [np.mean(cosine_rv.rvs(n)) for _ in range(num_of_samples)]
    plt.subplot(2, 2, i+1)
    plt.hist(means, density=True, bins=30, alpha=0.6, label='Sample means histogram')
    
    # Теоретическое распределение выборочных средних по ЦПТ
    norm_mean = real_mean
    norm_std = math.sqrt(real_var / n)
    x = np.linspace(-4, 4, 100)
    norm_rv = sts.norm(norm_mean, norm_std)
    pdf = norm_rv.pdf(x)
    plt.plot(x, pdf, label='CLT', alpha=0.6)
    plt.title('Sample size = ' + str(n))
    plt.legend()

plt.show()