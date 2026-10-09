import pandas as pd
import re
caminho = ('Base_Teste.csv')

df = pd.read_csv(
    caminho,
    sep=';',
    decimal=',',
    low_memory=False
)

print(f'Quantidade de linhas: {len(df)}')
print(f'Quantidade de colunas: {len(df.columns)}')
print('\nNomes das colunas:')
print('\n'.join(f'- {coluna}' for coluna in df.columns))

print('\nPrimeiras linhas:')
print(df.head(5).T.to_string(header=False))

print('\nTipos das colunas:')
for coluna, tipo in df.dtypes.items():
    print(f'- {coluna}: {tipo}')


print('\n' + '=' * 40)
print('PRODUTOS ENCONTRADOS')
print('=' * 40)
print('\nProdutos encontrados:')  
for produto, quantidade in df['Produto'].value_counts(dropna=False).items():  
    print(f'- {produto}: {quantidade}')