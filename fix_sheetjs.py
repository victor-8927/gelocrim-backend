path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3286 (índice 3285) tem o SheetJS no lugar errado
print('Antes:')
print(f'3285: {lines[3284].rstrip()}')
print(f'3286: {lines[3285].rstrip()}')
print(f'3287: {lines[3286].rstrip()}')

# Remove o SheetJS da linha 3286
lines[3285] = lines[3285].replace(
    '  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>\n',
    '\n'
)

print('\nDepois:')
print(f'3285: {lines[3284].rstrip()}')
print(f'3286: {lines[3285].rstrip()}')

# Adiciona SheetJS no lugar correto — antes do </head> principal
content = ''.join(lines)

# Verifica se já existe no lugar correto
if 'xlsx.full.min.js' in content:
    # Remove todas as ocorrências
    import re
    content = re.sub(r'\s*<script src="[^"]*xlsx[^"]*"></script>', '', content)
    print('SheetJS removido de todos os lugares!')

# Adiciona no lugar correto — antes do </head> principal (primeira ocorrência)
first_head_close = content.find('</head>')
if first_head_close != -1:
    content = content[:first_head_close] + \
        '  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>\n' + \
        content[first_head_close:]
    print(f'SheetJS adicionado no </head> correto (pos {first_head_close})')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nCorrigido! Ctrl+Shift+R.')
