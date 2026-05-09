path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ver o que tem entre script 3 e script 4
# Script 3 linha 2543, Script 4 linha 3943
print('=== FIM DO SCRIPT 3 (linhas 3935-3945) ===')
for i in range(3934, 3945):
    print(f'{i+1}: {repr(lines[i])}')

print('\n=== INÍCIO DO SCRIPT 4 (linhas 3943-3950) ===')
for i in range(3942, 3952):
    print(f'{i+1}: {repr(lines[i])}')

# Ver onde está o goTo
content = ''.join(lines)
idx = content.find('function goTo(')
ln = content[:idx].count('\n')+1
print(f'\ngoTo está na linha {ln}')
print(f'Script 3 começa na linha 2543, Script 4 na linha 3943')
print(f'goTo está no script {"3" if ln < 3943 else "4"}')
