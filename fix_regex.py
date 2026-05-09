path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linhas 3807-3809 (índices 3806-3808) precisam ser juntadas em uma só
print(f'3807: {repr(lines[3806])}')
print(f'3808: {repr(lines[3807])}')
print(f'3809: {repr(lines[3808])}')

# Substitui as 3 linhas por uma linha correta
lines[3806] = "      var linhas = text.split('\\n').filter(function(l){return l.trim();});\n"
del lines[3807]  # remove linha 3808
del lines[3807]  # remove linha 3809 (agora no índice 3807)

print(f'\nCorrigido: {repr(lines[3806])}')
print(f'Total: {len(lines)}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Pronto! Ctrl+Shift+R.')
