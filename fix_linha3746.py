path = r'C:\fleet-cloud\gelocrim_v1.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Linha 3746 (índice 3745) — corrige verDetalhePedido
print(f'Antes: {repr(lines[3745][:120])}')
lines[3745] = '      \'<td><button class="btn btn-sm btn-secondary" onclick="verDetalhePedido(&quot;\'+o.id+\'&quot;)">👁</button></td>\' +\n'
print(f'Depois: {repr(lines[3745][:120])}')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Pronto! Ctrl+Shift+R.')
