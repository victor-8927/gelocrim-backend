import pandas as pd 
df = pd.read_excel('Gelocrim_Importacao_Dados.xlsx', header=None, nrows=5) 
for i, row in df.iterrows(): 
    print(f'Linha {i}:', list(row)) 
