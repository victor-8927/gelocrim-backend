path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Localiza editarVeiculo e mostra completo
idx = content.find('async function editarVeiculo(id){')
depth = 0
i = idx
while i < len(content):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
    i += 1

print('=== editarVeiculo atual ===')
print(content[idx:end])
