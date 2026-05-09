path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Mostra os últimos 200 caracteres para ver o padrão exato
print('=== ÚLTIMOS 300 CHARS ===')
print(repr(content[-300:]))
