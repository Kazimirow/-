import pandas as pd
from scipy.stats import norm
from statsmodels.stats.weightstats import _zconfint_generic
import numpy as np

# Создание фрейма данных
data = {
    "total day calls": [150, 160, 170, 180, 190, 160, 155, 165, 175, 185, 155, 145],
    "churn": ["False", "True", "False", "True", "False", "True", "False", "False", "True", "True", "False", "False"]
}

# Создание фрейма данных
df = pd.DataFrame(data)
print(df.head())

# Разделение данных на ушедших и не ушедших по оттоку
churned = df[df['churn'] == 'True']
not_churned = df[df['churn'] == 'False']

# Функция для расчета доверительных интервалов по z-интервалу
def mean_confidence_interval(data, alpha=0.05):
    mean = data.mean()
    std_err = data.std(ddof=1) / np.sqrt(len(data))
    z = norm.ppf(1 - alpha / 2)
    margin_of_error = z * std_err
    return mean - margin_of_error, mean + margin_of_error

alpha = 0.05  # уровень значимости
# Расчет доверительных интервалов с использованием явной формулы для z-интервала
conf_int_churned_explicit = mean_confidence_interval(churned['total day calls'], alpha)
conf_int_not_churned_explicit = mean_confidence_interval(not_churned['total day calls'], alpha)

print("Доверительный интервал (явная формула) для среднего значения total day calls (ушедшие):", 
      f"({conf_int_churned_explicit[0]:.2f}, {conf_int_churned_explicit[1]:.2f})")
print("Доверительный интервал (явная формула) для среднего значения total day calls (не ушедшие):", 
      f"({conf_int_not_churned_explicit[0]:.2f}, {conf_int_not_churned_explicit[1]:.2f})")

# Расчет доверительных интервалов с использованием функций statsmodels.stats.weightstats._zconfint_generic
ci_churned = _zconfint_generic(churned['total day calls'].mean(), churned['total day calls'].std(ddof=1) / np.sqrt(len(churned)), 
                               norm.ppf(1 - alpha / 2), 'two-sided')
ci_not_churned = _zconfint_generic(not_churned['total day calls'].mean(), not_churned['total day calls'].std(ddof=1) / np.sqrt(len(not_churned)), 
                                   norm.ppf(1 - alpha / 2), 'two-sided')

print("Доверительный интервал (с использованием функций statsmodels) для среднего значения total day calls (ушедшие):", 
       f"({ci_churned[1]:.2f}, {ci_churned[0]:.2f})")
print("Доверительный интервал (с использованием функций statsmodels) для среднего значения total day calls (не ушедшие):", 
       f"({ci_not_churned[1]:.2f}, {ci_not_churned[0]:.2f})")