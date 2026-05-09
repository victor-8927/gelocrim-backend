path = r'C:\gelocrim-motorista\screens\RotaScreen.js'

NGROK_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Tenta varios padroes
replacements = [
    ("const API_URL   = 'http://11.0.1.72:8000/api/v1';", f"const API_URL   = '{NGROK_URL}';"),
    ("const API_URL  = 'http://11.0.1.72:8000/api/v1';",  f"const API_URL  = '{NGROK_URL}';"),
    ("const API_URL = 'http://11.0.1.72:8000/api/v1';",   f"const API_URL = '{NGROK_URL}';"),
    ("http://11.0.1.72:8000/api/v1", NGROK_URL),
]

found = False
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'Substituido: {old[:50]}...')
        found = True
        break

if not found:
    print('URL nao encontrada! Verificando...')
    import re
    urls = re.findall(r'http://[\d.:]+/api/v1', content)
    print(f'URLs encontradas: {urls}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Pronto! Recompile o APK.')
