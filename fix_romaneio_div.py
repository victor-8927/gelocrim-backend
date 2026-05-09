path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3395 (idx 3394): '    </div>`;\n'  <- tem </div> extra antes do backtick
# Linha 3394 (idx 3393): '    </div>\n'    <- fecha o div correto

# Remove o </div> da linha 3395, mantendo só o `;\n
print(f'Antes 3394: {repr(lines[3393])}')
print(f'Antes 3395: {repr(lines[3394])}')

lines[3394] = '  `;\n'

print(f'Depois 3395: {repr(lines[3394])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Pronto! Ctrl+Shift+R.')
