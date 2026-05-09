path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3658 (índice 3657)
print('Antes:', repr(lines[3657]))

lines[3657] = '        regs.map(r=>\'<option value="\'+r+\'">\'+r+\'</option>\').join(\'\');\n'

print('Depois:', repr(lines[3657]))

# Corrige também as outras linhas com backtick problemático
# Linha 2687, 2694, etc - verifica
for idx in [2686, 2693, 2804, 2809, 2966, 2996, 3001, 3008, 3362, 3370, 3372, 3693, 3704]:
    if idx < len(lines):
        line = lines[idx]
        if '`' in line:
            print(f'\nLinha {idx+1}: {repr(line[:100])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('\nSalvo! Ctrl+Shift+R.')
