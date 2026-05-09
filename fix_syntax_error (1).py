path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# O problema é que o join ficou com newline literal dentro de string simples
# Substitui a versão quebrada pela correta
old_csv = "  const csv = rows.map(r=>r.join(';')).join('\n');"
new_csv = "  const csv = rows.map(r=>r.join(';')).join('\\n');"

# Tenta encontrar o padrão com newline literal
if old_csv in content:
    content = content.replace(old_csv, new_csv)
    print('Corrigido com padrão simples!')
else:
    # Busca pela quebra literal (newline dentro de aspas simples)
    import re
    # Substitui qualquer join com newline literal
    content = re.sub(
        r"\.join\('[\r\n]+'\)",
        ".join('\\\\n')",
        content
    )
    print('Corrigido com regex!')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verifica
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Linha 4842: {repr(lines[4841])}')
print('Ctrl+Shift+R!')
