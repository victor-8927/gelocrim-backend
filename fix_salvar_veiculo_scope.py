path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 1624 é o botão que chama salvarVeiculoCompleto
print(f'Linha 1624: {repr(lines[1623][:100])}')
print(f'Linha 1623: {repr(lines[1622][:100])}')
print(f'Linha 1625: {repr(lines[1624][:100])}')
