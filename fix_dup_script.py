path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove linha 3681 (índice 3680) que é </script> duplicado
print(f'Linha 3681: {repr(lines[3680])}')
del lines[3680]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Total: {len(lines)}')
print('Pronto! Ctrl+Shift+R.')
