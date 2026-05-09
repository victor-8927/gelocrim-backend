path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 3650-3665 ===')
for i in range(3649, min(3665, len(lines))):
    print(f'{i+1}: {repr(lines[i][:120])}')

# Encontra TODAS as linhas com backtick problemático fora de template literals válidos
# O problema são template literals truncados por quebra de linha
import re
problemas = []
for i, line in enumerate(lines):
    # Conta backticks na linha
    ticks = line.count('`')
    if ticks % 2 == 1:  # número ímpar = template literal quebrado
        problemas.append(i+1)

print(f'\nLinhas com backtick ímpar (possível problema): {problemas[:20]}')
