import re

path = r'C:\gelocrim-motorista\android\app\src\main\AndroidManifest.xml'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Conteudo atual:')
print(content[:2000])

# Adiciona usesCleartextTraffic no application tag
old = '<application'
new = '<application\n      android:usesCleartextTraffic="true"'

if 'usesCleartextTraffic' not in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('\nusesCleartextTraffic adicionado!')
else:
    print('\nusesCleartextTraffic ja existe!')
