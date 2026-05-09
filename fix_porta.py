path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('localhost:8001', 'localhost:8000')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Porta atualizada para 8000!')
