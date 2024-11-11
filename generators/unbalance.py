import csv
import random

def gerar_dados(num_linhas):
    dados = []
    for _ in range(num_linhas):
        fase1 = round(random.uniform(0, 15), 2)
        fase2 = round(random.uniform(0, 15), 2)
        fase3 = round(random.uniform(0, 15), 2)

        diff_12 = abs(fase1 - fase2) / max(fase1, fase2) if max(fase1, fase2) != 0 else 0
        diff_13 = abs(fase1 - fase3) / max(fase1, fase3) if max(fase1, fase3) != 0 else 0
        diff_23 = abs(fase2 - fase3) / max(fase2, fase3) if max(fase2, fase3) != 0 else 0

        label = diff_12 > 0.3 or diff_13 > 0.3 or diff_23 > 0.3

        dados.append([fase1, fase2, fase3, label])

    return dados

def salvar_csv(dados, nome_arquivo="dados_corrente.csv"):
    cabecalhos = ["fase1", "fase2", "fase3", "label"]

    with open(nome_arquivo, mode="a", newline="") as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(cabecalhos)  # Escreve os cabeçalhos
        # Formata cada valor de fase com 2 casas decimais ao salvar
        for linha in dados:
            fase1, fase2, fase3, label = linha
            escritor_csv.writerow([f"{fase1:.2f}", f"{fase2:.2f}", f"{fase3:.2f}", label])

num_linhas = int(input("Digite o número de linhas de dados a serem geradas: "))
dados = gerar_dados(num_linhas)

salvar_csv(dados)
print(f"{num_linhas} linhas de dados foram salvas no arquivo 'dados_corrente.csv'")
