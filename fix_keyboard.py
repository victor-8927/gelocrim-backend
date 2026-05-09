path = r'C:\gelocrim-motorista\android\app\src\main\AndroidManifest.xml'

with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Troca adjustResize por adjustPan
if 'adjustResize' in c:
    c = c.replace('adjustResize', 'adjustPan')
    print('adjustResize -> adjustPan')
elif 'adjustPan' in c:
    print('adjustPan ja existe')
else:
    # Adiciona na MainActivity
    c = c.replace('android:name=".MainActivity"', 'android:name=".MainActivity"\n        android:windowSoftInputMode="adjustPan"')
    print('adjustPan adicionado na MainActivity')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Pronto!')
