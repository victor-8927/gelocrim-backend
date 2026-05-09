path = r'C:\fleet-cloud\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total linhas: {len(lines)}')
for i, l in enumerate(lines[55:75], start=56):
    print(f'{i}: {repr(l)}')
