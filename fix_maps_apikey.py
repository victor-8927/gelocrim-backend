path = r'C:\gelocrim-motorista\android\app\src\main\AndroidManifest.xml'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

api_key_tag = '<meta-data android:name="com.google.android.geo.API_KEY" android:value="AIzaSyB47DpEZW4qbU74LxcG1ZD76cYLRlJw88M"/>'

if 'com.google.android.geo.API_KEY' not in content:
    # Adiciona logo apos o <application tag
    content = content.replace(
        '<meta-data android:name="expo.modules.updates.ENABLED"',
        api_key_tag + '\n    <meta-data android:name="expo.modules.updates.ENABLED"'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('API Key do Google Maps adicionada!')
else:
    print('API Key ja existe!')

print('Recompile o APK!')
