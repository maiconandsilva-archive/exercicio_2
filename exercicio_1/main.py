import csv
from collections import Counter

# Mapeamento dos campos do CSV para os campos da tabela
MAPEAMENTO = {
    'Nome Completo': 'nome',
    'Idade': 'idade',
    'Dept': 'departamento',
    'Salario': 'salario'
}

CSV_PATH = 'dataset.csv'
SQL_OUT_PATH = 'saida_inserts.sql'

# Função para ler o CSV e gerar comandos INSERT
with open(CSV_PATH, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    inserts = []
    dados = []
    for row in reader:
        valores = [f"'{row[csv_col]}'" if MAPEAMENTO[csv_col] != 'idade' and MAPEAMENTO[csv_col] != 'salario' else row[csv_col] for csv_col in MAPEAMENTO]
        insert = f"INSERT INTO funcionarios (nome, idade, departamento, salario) VALUES ({', '.join(valores)});"
        inserts.append(insert)
        dados.append(row)

with open(SQL_OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(inserts))

print(f"Arquivo de comandos INSERT gerado em {SQL_OUT_PATH}")
