import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample

import pickle
from fogml.generators import GeneratorFactory

# Carrega os dados do CSV
dados = pd.read_csv("./data/dados_corrente.csv")

print(len(dados))

print(dados.columns)
print(dados.head())

# Divide os dados em features (X) e labels (y)
X = dados[["fase1", "fase2", "fase3"]]
y = dados["label"]

# Balanceamento dos dados para ter quantidades iguais de True e False
dados_true = dados[dados["label"] == "True"]
dados_false = dados[dados["label"] == "False"]

print("Número de exemplos True:", len(dados_true))
print("Número de exemplos False:", len(dados_false))

# Garante que ambos os grupos tenham o mesmo tamanho (número mínimo entre True e False)
min_count = min(len(dados_true), len(dados_false))

# Amostra aleatoriamente para balancear as classes
dados_true_balanced = resample(dados_true, replace=False, n_samples=min_count, random_state=1)
dados_false_balanced = resample(dados_false, replace=False, n_samples=min_count, random_state=1)

print("APÓS BALANCEAMENTO:")
print("Número de exemplos True:", len(dados_true_balanced))
print("Número de exemplos False:", len(dados_false_balanced))

print("")

# Junta os dados balanceados e embaralha
dados_balanced = pd.concat([dados_true_balanced, dados_false_balanced]).sample(frac=1, random_state=1)

# Divide os dados balanceados em features (X) e labels (y) novamente
X_balanced = dados_balanced[["fase1", "fase2", "fase3"]]
y_balanced = dados_balanced["label"]

# Divide os dados em treino, validação e teste
X_train, X_temp, y_train, y_temp = train_test_split(X_balanced, y_balanced, test_size=0.4, random_state=1)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=1)

# Cria e treina o modelo de rede neural
modelo = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000, random_state=1)


# FogML
factory = GeneratorFactory()
generator = factory.get_generator(modelo)


modelo.fit(X_train, y_train)

# Avalia o modelo no conjunto de teste
y_test_pred = modelo.predict(X_test)
print("\nTESTE:")
print("============================================")
print(classification_report(y_test, y_test_pred))
print("Acurácia: %.2f" %(accuracy_score(y_test, y_test_pred)))


# Avalia o modelo no conjunto de validação
y_val_pred = modelo.predict(X_val)
print("\nVALIDAÇÃO:")
print("============================================")
print(classification_report(y_val, y_val_pred))
print("Acurácia: %.2f" %(accuracy_score(y_val, y_val_pred)))



dumped = pickle.dumps(modelo)
print("SIZE: " + str(len(dumped)))

generator.generate()