path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra onde editId é lido no salvarVeiculoCompleto
for i in range(4130, 4160):
    print(f'{i+1}: {repr(lines[i][:100])}')
