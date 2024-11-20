import random
import matplotlib.pyplot as plt

def random_weighted(min_value: float, max_value: float) -> float:
    """
    Gera um valor aleatório com duas casas decimais entre min_value e max_value,
    com maior probabilidade de ser próximo ao max_value.
    """
    random_factor = random.random() ** (1/4)  # Aumenta a chance de ser próximo ao máximo
    weighted_value = min_value + random_factor * (max_value - min_value)
    return round(weighted_value, 2)

# Gerando mil números aleatórios
min_value = 10
max_value = 20
random_numbers = [random_weighted(min_value, max_value) for _ in range(10000)]

# Plotando o histograma
plt.hist(random_numbers, bins=30, edgecolor='black')
plt.title('Histograma dos Números Aleatórios')
plt.xlabel('Valor')
plt.ylabel('Frequência')
plt.show()
