import pandas as pd
import re

caminho_entrada = 'Base_Teste.csv'
caminho_saida = 'Base_Tratada.csv'

df = pd.read_csv(
    caminho_entrada,
    sep=';',
    decimal=',',
    low_memory=False
)

print(f'Quantidade de linhas: {len(df)}')

# ==========================================================
# 1. TRATAMENTO DA COLUNA PRODUTO
# ==========================================================

def padronizar_produto(produto):

    if pd.isna(produto):  
        return pd.NA  


    produto = str(produto).strip()  


    padrao = r"^Ar-Condicionado\s+(\d+(?:[.,]\d+)?)\s*(BTUS?|TR)$"


    resultado = re.match(  

        padrao,  

        produto,  

        flags=re.IGNORECASE  
    )


    if resultado is None:  
        return pd.NA  


    capacidade = resultado.group(1)  

    unidade = resultado.group(2).upper()  


    if unidade == 'TR':  

        capacidade = capacidade.replace(',', '.')  

        capacidade = float(capacidade)  

        capacidade_btu = capacidade * 12000  


    else:  

        capacidade = capacidade.replace('.', '')  

        capacidade_btu = float(capacidade)  


    capacidade_btu = round(capacidade_btu)  


    capacidade_formatada = f'{capacidade_btu:,}'.replace(',', '.')  


    return f'Ar-Condicionado {capacidade_formatada} BTUs'  



linhas_antes_produto = len(df)  


df['Produto'] = df['Produto'].apply(padronizar_produto)  


df = df.dropna(subset=['Produto'])  


linhas_depois_produto = len(df)  


print(f'Linhas removidas por Produto: {linhas_antes_produto - linhas_depois_produto}')  

print(f'Linhas após Produto: {len(df)}')  



# ==========================================================
# 2. TRATAMENTO DA COLUNA STATUS
# ==========================================================

linhas_antes_status = len(df)  


df = df.dropna(subset=['Status'])  


df['Status'] = (  

    df['Status']  

    .astype('string')  

    .str.strip()  

    .str.upper()  
)


df = df[df['Status'] != '']  


linhas_depois_status = len(df)  


print(f'Linhas removidas por Status: {linhas_antes_status - linhas_depois_status}')  

print(f'Linhas após Status: {len(df)}') 



# ==========================================================
# 3. TRATAMENTO DA COLUNA VENDEDOR
# ==========================================================

linhas_antes_vendedor = len(df)  


sem_vendedor = (  

    df['Vendedor'].isna()  

    |

    df['Vendedor'] 

    .astype('string')  

    .str.strip()  

    .str.upper()  

    .eq('SEM VENDEDOR')  

    |

    df['Vendedor']  
    .astype('string')  
    .str.strip()  
    .eq('')  
)


df = df[~sem_vendedor] 


linhas_depois_vendedor = len(df)


print(f'Linhas removidas por Vendedor: {linhas_antes_vendedor - linhas_depois_vendedor}')

print(f'Linhas após Vendedor: {len(df)}')  



# ==========================================================
# 4. PADRONIZAÇÃO DAS DATAS
# ==========================================================

df['Data NF'] = pd.to_datetime(  
    df['Data NF'],  
    format='%d/%m/%Y',  

    errors='coerce' 
)


df['DataEntrega'] = pd.to_datetime(  

    df['DataEntrega'],

    format='%Y-%m-%d %H:%M:%S.%f', 

    errors='coerce'  
)



# ==========================================================
# 5. PADRONIZAÇÃO DE CAMPOS DE TEXTO
# ==========================================================

df['Cidade'] = (  

    df['Cidade']  

    .astype('string')  

    .str.strip()  

    .str.upper()  
)


df['UF'] = (  

    df['UF']  

    .astype('string')  

    .str.strip()  

    .str.upper() 
)


df['Vendedor'] = (  

    df['Vendedor'] 

    .astype('string')

    .str.strip() 
)



# ==========================================================
# 6. VALIDAÇÃO FINAL
# ==========================================================

print('\n' + '=' * 50)

print('RESULTADO FINAL DO TRATAMENTO')

print('=' * 50) 


print(f'Quantidade final de linhas: {len(df)}')

print(f'Quantidade de colunas: {len(df.columns)}')


print('\nTipos das colunas após tratamento:')  

for coluna, tipo in df.dtypes.items():  

    print(f'- {coluna}: {tipo}')  



# ==========================================================
# 7. EXPORTAÇÃO DA BASE TRATADA
# ==========================================================

df.to_csv( 

    caminho_saida,  #

    sep=';',  

    decimal=',',  

    index=False,  

    encoding='utf-8-sig'  
)


print(f'\nArquivo gerado com sucesso: {caminho_saida}')