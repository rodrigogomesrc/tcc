import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils import resample

# Carrega os dados do CSV
dados = pd.read_csv("./data/dados_fator_potencia.csv")

# Divide os dados em features (X) e labels (y)
# As features incluem todas as correntes e fatores de potência
X = dados[[f"corrente_{i+1}" for i in range(8)] +
          [f"fator_potencia_{i+1}" for i in range(8)] +
          ["corrente_central", "fator_potencia_central"]]
y = dados["classe"]


# Balanceamento dos dados para ter proporções iguais para todas as classes
dados_balanced = pd.DataFrame()

print("Quantidade por classes antes do balaceamento")
print(dados["classe"].value_counts())

for classe in y.unique():
    dados_classe = dados[dados["classe"] == classe]
    n_samples = dados["classe"].value_counts().min()  # Número mínimo de exemplos entre as classes
    dados_classe_balanced = resample(dados_classe, replace=False, n_samples=n_samples, random_state=1)
    dados_balanced = pd.concat([dados_balanced, dados_classe_balanced])

# Embaralha os dados balanceados
dados_balanced = dados_balanced.sample(frac=1, random_state=1)


print("Quantidade por classes APÓS balaceamento")
print(dados_balanced["classe"].value_counts())

# Divide os dados balanceados em features (X) e labels (y) novamente
X_balanced = dados_balanced[[f"corrente_{i+1}" for i in range(8)] +
                            [f"fator_potencia_{i+1}" for i in range(8)] +
                            ["corrente_central", "fator_potencia_central"]]
y_balanced = dados_balanced["classe"]

# Divide os dados em treino, validação e teste
X_train, X_temp, y_train, y_temp = train_test_split(X_balanced, y_balanced, test_size=0.4, random_state=1)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=1)

# Cria e treina o modelo de rede neural

modelo = MLPClassifier(hidden_layer_sizes=(27, 18), max_iter=1000, random_state=1)
modelo.fit(X_train, y_train)

# Avalia o modelo no conjunto de teste
y_test_pred = modelo.predict(X_test)
print("\nTESTE:")
print("============================================")
print(classification_report(y_test, y_test_pred))
print("Acurácia: %.2f" % accuracy_score(y_test, y_test_pred))

# Avalia o modelo no conjunto de validação
y_val_pred = modelo.predict(X_val)
print("\nVALIDAÇÃO:")
print("============================================")
print(classification_report(y_val, y_val_pred))
print("Acurácia: %.2f" % accuracy_score(y_val, y_val_pred))