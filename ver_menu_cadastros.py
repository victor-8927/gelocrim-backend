path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Busca o menu de cadastros
idx = content.find('Cadastros')
print(content[idx:idx+800])
