path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total: {len(lines)}')

# Mostra linhas ao redor do </script> que fecha o script principal
for i, line in enumerate(lines):
    if '</script>' in line and i > 2500 and i < 3500:
        print(f'\n</script> na linha {i+1}')
        for j in range(max(0,i-5), min(len(lines),i+3)):
            print(f'  {j+1}: {repr(lines[j][:100])}')

# Mostra onde o segundo script começa
for i, line in enumerate(lines):
    if '<script>' in line and i > 3400:
        print(f'\n<script> na linha {i+1}')
        for j in range(i, min(len(lines),i+4)):
            print(f'  {j+1}: {repr(lines[j][:100])}')
        break
