path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra os dois </script> consecutivos no final e remove um
for i in range(len(lines)-1, 0, -1):
    if lines[i].strip() == '</script>' and lines[i-1].strip() == '</script>':
        print(f'Removendo </script> duplicado na linha {i+1}')
        del lines[i]
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Total: {len(lines)} linhas')
print('Pronto! Ctrl+Shift+R.')
