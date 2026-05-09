import pandas as pd 
xl = pd.ExcelFile('Gelocrim_Importacao_Dados.xlsx') 
print('Abas:', xl.sheet_names) 
for aba in xl.sheet_names: 
    df = pd.read_excel('Gelocrim_Importacao_Dados.xlsx', sheet_name=aba, header=None, nrows=8) 
    print(f'\n=== ABA: {aba} ===') 
    for i, row in df.iterrows(): 
        print(f'  L{i}:', list(row)) 
