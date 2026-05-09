path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# FIX 1: linha 3395 — remove a barra invertida antes do backtick
# '    </div>\\`;\n'  →  '    </div>`;\n'
if '\\`' in lines[3394]:
    lines[3394] = lines[3394].replace('\\`', '`')
    print(f'Fix 1 aplicado: {repr(lines[3394])}')

# FIX 2: linha 3736 — aspas quebradas no toggleOrderChk
# Substitui a linha inteira por versão correta
old_linha = lines[3735]
print(f'Linha 3736 atual: {repr(old_linha[:100])}')

# Substitui por versão limpa sem aspas duplas aninhadas problemáticas
lines[3735] = "      '<td><input type=\"checkbox\" class=\"order-chk\" data-id=\"'+o.id+'\" onchange=\"toggleOrderChk(\\\"'+o.id+'\\\",this.checked)\"></td>' +\n"
print(f'Fix 2 aplicado: {repr(lines[3735][:100])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'\nTotal: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
