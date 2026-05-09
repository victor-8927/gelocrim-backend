path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linhas 3396-3400 (índices 3395-3399) são duplicatas do fechamento do gerarRomaneio
# Linha 3394: '    </div>\n'
# Linha 3395: '    </div>`;\n'   <- fechamento do template literal
# Linha 3396: "  const w = ..."  <- duplicata
# Linha 3397: '  if(w){...'      <- duplicata  
# Linha 3398: '}\n'              <- duplicata
# Linha 3399: "  const w = ..."  <- duplicata
# Linha 3400: '}\n'              <- duplicata extra

# Remove linhas 3396-3400 (índices 3395-3399)
print('Removendo:')
for i in range(3395, 3400):
    print(f'  {i+1}: {repr(lines[i][:80])}')

del lines[3395:3400]
print(f'\nTotal após: {len(lines)}')

# Verifica resultado
print('\n=== LINHAS 3393-3403 ===')
for i in range(3392, min(3403, len(lines))):
    print(f'{i+1}: {repr(lines[i][:100])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('\nPronto! Ctrl+Shift+R.')
