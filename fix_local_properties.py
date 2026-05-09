import os

path = r'C:\gelocrim-motorista\android\local.properties'

sdk_path = r'C:\Users\victor.mosqueira\AppData\Local\Android\Sdk'
# Converte barras invertidas para barras normais (formato Java)
sdk_path_java = sdk_path.replace('\\', '\\\\')

with open(path, 'w', encoding='utf-8') as f:
    f.write(f'sdk.dir={sdk_path_java}\n')

print(f'local.properties criado com:')
print(f'sdk.dir={sdk_path_java}')

# Verifica se o SDK existe
if os.path.exists(sdk_path):
    print('SDK encontrado!')
else:
    print('SDK NAO encontrado neste caminho!')
