import pandas as pd 
df = pd.read_excel('Gelocrim_Importacao_Dados.xlsx', sheet_name='Clientes TGFPAR', header=1, dtype=str) 
print('Colunas:', list(df.columns)) 
print('Linha 0:', list(df.iloc[0])) 
