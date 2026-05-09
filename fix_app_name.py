import os

# 1. Atualiza o nome do app em strings.xml
strings_path = r'C:\gelocrim-motorista\android\app\src\main\res\values\strings.xml'

strings_content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Gelocrim OPS</string>
</resources>
'''

os.makedirs(os.path.dirname(strings_path), exist_ok=True)
with open(strings_path, 'w', encoding='utf-8') as f:
    f.write(strings_content)
print('Nome "Gelocrim OPS" configurado!')

# 2. Verifica o AndroidManifest para confirmar que usa @string/app_name
manifest_path = r'C:\gelocrim-motorista\android\app\src\main\AndroidManifest.xml'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = f.read()

if 'android:label="@string/app_name"' in manifest:
    print('AndroidManifest ja usa @string/app_name - OK!')
else:
    print('ATENCAO: AndroidManifest pode precisar de ajuste no label!')
    print('Procurando label atual...')
    import re
    labels = re.findall(r'android:label="[^"]*"', manifest)
    for l in labels:
        print(f'  {l}')

print('\nPronto! Recompile o APK para aplicar o novo nome.')
