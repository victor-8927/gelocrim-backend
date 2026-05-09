path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'page-ocorrencias' in line or 'ocorrencia' in line.lower():
        print(f'{i+1}: {line.rstrip()}')
        if 'page-ocorrencias' in line:
            for j in range(i, min(i+40, len(lines))):
                print(f'  {j+1}: {lines[j].rstrip()}')
            break
