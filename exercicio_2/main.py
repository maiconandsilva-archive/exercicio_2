import csv
import matplotlib.pyplot as plt
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

# --- Análise das dimensões de qualidade ---
def analisar_completude(dados):
    total = len(dados)
    completos = sum(all(row.get(c, '').strip() for c in MAPEAMENTO) for row in dados)
    return completos, total-completos

def analisar_unicidade(dados):
    nomes = [row.get('Nome Completo', '').strip() for row in dados]
    contagem = Counter(nomes)
    duplicados = sum(count > 1 for count in contagem.values())
    return len(nomes)-duplicados, duplicados

def analisar_temporalidade(dados):
    pontuais = sum(row.get('Idade', '').isdigit() and 18 <= int(row['Idade']) <= 65 for row in dados)
    return pontuais, len(dados)-pontuais

def analisar_validade(dados):
    validos = sum(row.get('Idade', '').isdigit() and float(row.get('Salario', '0')) > 0 for row in dados)
    return validos, len(dados)-validos

def analisar_consistencia(dados):
    departamentos_validos = {'TI', 'Financeiro', 'Recursos Humanos'}
    consistentes = sum(row.get('Dept', '') in departamentos_validos for row in dados)
    return consistentes, len(dados)-consistentes

dimensoes = {
    'Completude': analisar_completude,
    'Unicidade': analisar_unicidade,
    'Temporalidade': analisar_temporalidade,
    'Validade': analisar_validade,
    'Consistência': analisar_consistencia
}

resultados = {}
for nome, func in dimensoes.items():
    ok, nok = func(dados)
    resultados[nome] = {'OK': ok, 'NOK': nok}

# --- Geração dos gráficos ---
for nome, res in resultados.items():
    plt.figure()
    plt.bar(['OK', 'NOK'], [res['OK'], res['NOK']], color=['green', 'red'])
    plt.title(f'Dimensão: {nome}')
    plt.ylabel('Quantidade de registros')
    plt.savefig(f'grafico_{nome.lower()}.png')
    plt.close()
    print(f'Gráfico gerado: grafico_{nome.lower()}.png')

# --- Considerações Ética e Privacidade ---
print('Considerações: Os dados utilizados são fictícios e não contêm informações sensíveis. Para produção, recomenda-se anonimização e controle de acesso.')
