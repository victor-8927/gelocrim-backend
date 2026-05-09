path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra a seção de roteirização
start = None
end = None
for i, line in enumerate(lines):
    if 'page-roteirizacao' in line and start is None:
        start = i
    if start and i > start + 5 and ('class="page"' in line or "<!-- ══" in line):
        end = i
        break

print(f'=== ROTEIRIZAÇÃO (linhas {start+1} a {end+1}) ===')
for i in range(start, min(end or start+150, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')
