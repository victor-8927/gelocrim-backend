path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Corrige linhas 4842-4843: join com newline literal
# Linha 4842 (idx 4841): "  const csv = rows.map(r=>r.join(';')).join('"
# Linha 4843 (idx 4842): "');"
# Une as duas em uma linha correta

if lines[4841].rstrip().endswith("join('") and lines[4842].strip() == "');":
    lines[4841] = "  const csv = rows.map(r=>r.join(';')).join('\\n');\n"
    lines.pop(4842)
    print('Corrigido! Linha unida.')
else:
    print(f'Linha 4842: {repr(lines[4841])}')
    print(f'Linha 4843: {repr(lines[4842])}')
    print('Padrao diferente, corrigindo por conteudo...')
    # Corrige por conteudo
    for i in range(len(lines)-1):
        if "join('" in lines[i] and lines[i].rstrip().endswith("join('") and lines[i+1].strip() == "');":
            lines[i] = lines[i].rstrip().replace("join('", "join('\\n');\n")
            lines[i+1] = ''
            print(f'Corrigido na linha {i+1}!')
            break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Salvo! Ctrl+Shift+R.')
